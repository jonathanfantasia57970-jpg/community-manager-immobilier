#!/usr/bin/env python3
"""Initialize or validate business memory. No network and no external effects.

This checks structure and selected invariants, not truth, permissions, locking,
or financial/commercial validity. Unknown information must stay unknown.
"""
import argparse
import json
import math
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

COLLECTIONS = ('assets', 'tools', 'metrics', 'actions', 'experiments',
               'decisions', 'lessons', 'automations')
APPEND_ONLY = ('metrics', 'decisions', 'lessons')
STAGES = {'discovery', 'validation', 'launch', 'operation', 'growth', 'paused', 'closed'}
ACTION_STATES = {'proposed', 'planned', 'draft', 'running', 'blocked',
                 'completed', 'verified', 'cancelled'}
NATURES = {'observed', 'declared', 'estimated', 'unknown'}
VERDICTS = {'grow', 'maintain', 'correct', 'pivot', 'pause', 'stop', 'insufficient_data'}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def timestamp(value):
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return parsed if parsed.tzinfo is not None else None
    except (AttributeError, TypeError, ValueError):
        return None


def validate(state, previous=None):
    errors = []
    if not isinstance(state, dict):
        return ['state: expected object']
    if type(state.get('schema_version')) is not int or state['schema_version'] != 1:
        errors.append('schema_version: unsupported; explicit migration required')
    if type(state.get('version')) is not int or state['version'] < 1:
        errors.append('version: expected positive integer')
    bid = state.get('business_id')
    if not isinstance(bid, str) or not re.fullmatch(r'biz-[a-z0-9-]{8,64}', bid):
        errors.append('business_id: invalid stable identifier')
    if not nonempty(state.get('name')):
        errors.append('name: required')
    if timestamp(state.get('updated_at')) is None:
        errors.append('updated_at: expected ISO datetime with timezone')
    if not isinstance(state.get('stage'), str) or state['stage'] not in STAGES:
        errors.append('stage: invalid')
    for key in ('brief', 'mandate', 'drive', 'last_review', 'extensions'):
        if not isinstance(state.get(key), dict):
            errors.append(f'{key}: expected object')

    mandate = state.get('mandate')
    if isinstance(mandate, dict):
        permissions = mandate.get('permissions')
        limits = mandate.get('spending_limits')
        if not isinstance(permissions, list) or not all(nonempty(x) for x in permissions):
            errors.append('mandate.permissions: expected list of strings')
        if not isinstance(limits, list):
            errors.append('mandate.spending_limits: expected list')
        else:
            for i, limit in enumerate(limits):
                if not isinstance(limit, dict):
                    errors.append(f'mandate.spending_limits[{i}]: expected object')
                    continue
                if not number(limit.get('amount')) or limit['amount'] < 0:
                    errors.append(f'mandate.spending_limits[{i}].amount: invalid')
                for key in ('currency', 'period', 'account_id', 'source'):
                    if not nonempty(limit.get(key)):
                        errors.append(f'mandate.spending_limits[{i}].{key}: required')
        if (permissions or limits) and not nonempty(mandate.get('source')):
            errors.append('mandate.source: required for permissions or budgets')

    review = state.get('last_review')
    if isinstance(review, dict):
        if not isinstance(review.get('verdict'), str) or review['verdict'] not in VERDICTS:
            errors.append('last_review.verdict: invalid')
        if review.get('at') is not None and timestamp(review['at']) is None:
            errors.append('last_review.at: invalid timestamp')

    maps = {}
    for collection in COLLECTIONS:
        records = state.get(collection)
        if not isinstance(records, list):
            errors.append(f'{collection}: expected list')
            continue
        found = {}
        for index, record in enumerate(records):
            loc = f'{collection}[{index}]'
            if not isinstance(record, dict):
                errors.append(f'{loc}: expected object')
                continue
            rid = record.get('id')
            if not nonempty(rid):
                errors.append(f'{loc}.id: required')
            elif rid in found:
                errors.append(f'{loc}.id: duplicate')
            else:
                found[rid] = record
            if record.get('business_id') != bid:
                errors.append(f'{loc}.business_id: cross-business or missing')
            if collection == 'metrics':
                nature = record.get('nature')
                if not isinstance(nature, str) or nature not in NATURES:
                    errors.append(f'{loc}.nature: invalid')
                value = record.get('value')
                if nature == 'unknown':
                    if value is not None:
                        errors.append(f'{loc}.value: unknown must be null')
                elif not number(value):
                    errors.append(f'{loc}.value: expected finite number')
                for key in ('name', 'unit', 'period', 'scope'):
                    if not nonempty(record.get(key)):
                        errors.append(f'{loc}.{key}: required')
                if timestamp(record.get('collected_at')) is None:
                    errors.append(f'{loc}.collected_at: invalid timestamp')
                if nature != 'unknown' and not nonempty(record.get('source')):
                    errors.append(f'{loc}.source: required')
            if collection == 'actions':
                if not isinstance(record.get('status'), str) or record['status'] not in ACTION_STATES:
                    errors.append(f'{loc}.status: invalid')
                for key in ('title', 'owner', 'success_criterion'):
                    if not nonempty(record.get(key)):
                        errors.append(f'{loc}.{key}: required')
                evidence = record.get('evidence')
                if not isinstance(evidence, list) or not all(nonempty(x) for x in evidence):
                    errors.append(f'{loc}.evidence: expected list of references')
                elif record.get('status') == 'verified' and not evidence:
                    errors.append(f'{loc}.evidence: verified requires evidence')
        maps[collection] = found

    if previous is not None:
        previous_errors = validate(previous)
        if previous_errors:
            errors.append('previous: invalid; do not silently repair or overwrite')
            return errors
        if bid != previous['business_id']:
            errors.append('business_id: cannot change existing business identity')
        for key in previous:
            if key not in state:
                errors.append(f'{key}: existing field removed; preserve unknown fields')
        if type(state.get('version')) is int and state['version'] != previous['version'] + 1:
            errors.append('version: must increment by exactly one')
        now = timestamp(state.get('updated_at'))
        before = timestamp(previous.get('updated_at'))
        if now and before and now < before:
            errors.append('updated_at: cannot move backwards')
        for collection in COLLECTIONS:
            current = maps.get(collection, {})
            for old in previous[collection]:
                rid = old['id']
                if rid not in current:
                    errors.append(f'{collection}: historical record removed; archive instead')
                elif collection in APPEND_ONLY and current[rid] != old:
                    errors.append(f'{collection}: historical record modified; append superseding record')
        if isinstance(mandate, dict) and mandate != previous['mandate']:
            if not nonempty(mandate.get('source')) or mandate.get('source') == previous['mandate'].get('source'):
                errors.append('mandate: changed permissions need a new explicit instruction reference')
    return errors


def initialize(name):
    path = Path(__file__).resolve().parents[1] / 'assets' / 'business-template.json'
    state = json.loads(path.read_text(encoding='utf-8'))
    state.update(name=name, business_id='biz-' + uuid.uuid4().hex,
                 updated_at=datetime.now(timezone.utc).isoformat())
    return state


def load(path):
    def reject_constant(value):
        raise ValueError('Non-finite JSON number is not allowed')
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON object key is not allowed')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      parse_constant=reject_constant, object_pairs_hook=unique_keys)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--name', required=True)
    init.add_argument('--output', required=True)
    check = sub.add_parser('validate')
    check.add_argument('state')
    check.add_argument('--previous')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            state = initialize(args.name)
            errors = validate(state)
            if not errors:
                with Path(args.output).open('x', encoding='utf-8') as stream:
                    json.dump(state, stream, ensure_ascii=False, indent=2, allow_nan=False)
                    stream.write('\n')
        else:
            state = load(args.state)
            errors = validate(state, load(args.previous) if args.previous else None)
        if errors:
            print(json.dumps({'valid': False, 'errors': errors}, ensure_ascii=False, indent=2))
            return 1
        print(json.dumps({'valid': True, 'business_id': state['business_id'], 'version': state['version']}))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
