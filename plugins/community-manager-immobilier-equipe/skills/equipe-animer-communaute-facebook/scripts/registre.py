#!/usr/bin/env python3
"""Validate and read a local Facebook registry; no network calls or writes."""
import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime, date
from pathlib import Path

STATUSES = {'planned', 'draft', 'incomplete', 'ready', 'approved', 'scheduled', 'published', 'rejected', 'cancelled'}
ACTION_STATUSES = {'proposed', 'approved', 'completed', 'blocked', 'cancelled'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def stamp(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(parsed.tzinfo is not None, 'Timestamp must include a timezone')
    return parsed


def validate(data):
    require(isinstance(data, dict), 'Registry must be an object')
    require(data.get('schema_version') == 1, 'Unsupported schema')
    require(isinstance(data.get('profile_id'), str) and bool(data['profile_id'].strip()) and data.get('registry_key') == 'facebook-' + data['profile_id'] + '', 'Wrong registry')
    require(type(data.get('revision')) is int and data['revision'] > 0, 'Invalid revision')
    date.fromisoformat(data['updated_on'])
    require(isinstance(data.get('account'), dict), 'Missing account configuration')
    require(isinstance(data.get('editorial_plan'), dict), 'Missing editorial plan')
    for group in ('entries', 'actions', 'preferences'):
        require(isinstance(data.get(group), list), 'Missing list: ' + group)
    seen = set()
    for entry in data['entries']:
        require(isinstance(entry, dict), 'Invalid post entry')
        require(nonempty(entry.get('id')) and entry['id'] not in seen, 'Missing or duplicate post id')
        seen.add(entry['id'])
        stamp(entry['created_at'])
        require(entry.get('status') in STATUSES, 'Invalid post status')
        require(entry.get('scope') in {'full', 'text_only', 'idea', 'brief'}, 'Invalid post scope')
        require(nonempty(entry.get('subject')), 'Missing subject')
        require(type(entry.get('version')) is int and entry['version'] > 0, 'Invalid post version')
        require(isinstance(entry.get('text'), str), 'Missing text (empty allowed before drafting)')
        media = entry.get('media')
        require(isinstance(media, list) and len(media) <= 1, 'At most one final medium per post')
        for item in media:
            require(isinstance(item, dict) and item.get('type') in {'image', 'video'}, 'Invalid medium')
            require(nonempty(item.get('ref')), 'Missing actual media reference')
        if entry['status'] in {'ready', 'approved', 'scheduled', 'published'}:
            require(nonempty(entry['text']), 'A ready post needs text')
            if entry['scope'] == 'full':
                require(len(media) == 1 and media[0].get('verified') is True, 'A full post needs one verified final medium')
        if entry['status'] in {'approved', 'scheduled', 'published'}:
            require(entry.get('user_confirmation'), 'Missing instruction or approval reference')
        require(entry.get('channel') in {None, 'page', 'profile'}, 'Invalid channel')
        if entry['status'] in {'scheduled', 'published'}:
            confirmation = entry.get('publication_confirmation') or {}
            manual = entry['status'] == 'published' and entry.get('channel') == 'profile' and confirmation.get('source') == 'user_report'
            if manual:
                require(nonempty(confirmation.get('statement')), 'Missing manual statement')
                stamp(confirmation['reported_at'])
                if entry.get('published_at'):
                    stamp(entry['published_at'])
                if entry.get('published_on'):
                    date.fromisoformat(entry['published_on'])
            else:
                require(nonempty(entry.get('target_id')), 'Missing verified target id')
                require(entry.get('provider_result'), 'Missing provider confirmation')
                if entry['status'] == 'scheduled':
                    stamp(entry['scheduled_at'])
                elif entry.get('published_at'):
                    stamp(entry['published_at'])
                else:
                    require(confirmation.get('source') == 'provider_receipt', 'Missing publication date or explicit receipt')
                    stamp(entry['publication_confirmed_at'])
        review = entry.get('audience_review')
        if review is not None:
            require(isinstance(review, dict), 'Invalid audience observation')
            require(nonempty(review.get('observation_id')), 'Missing observation identity')
            stamp(review['observed_at'])
            require(review.get('state') in {'observed', 'partial', 'blocked', 'insufficient'}, 'Invalid observation state')
    seen_actions = set()
    for action in data['actions']:
        require(isinstance(action, dict), 'Invalid action')
        require(nonempty(action.get('id')) and action['id'] not in seen_actions, 'Missing or duplicate action id')
        seen_actions.add(action['id'])
        require(nonempty(action.get('kind')) and nonempty(action.get('description')), 'Missing action purpose')
        require(action.get('status') in ACTION_STATUSES, 'Invalid action status')
        require(type(action.get('external')) is bool, 'Action must say whether it acts externally')
        if action.get('due_at') is not None:
            stamp(action['due_at'])
        if action['status'] == 'approved':
            require(action.get('instruction_ref'), 'Missing accepted action instruction')
        if action['status'] == 'completed':
            require(action.get('result'), 'Missing action result')
            if action['external']:
                require(action.get('instruction_ref') and action.get('target_ref'), 'Missing external action authority or target')
    return {'valid': True, 'entries': len(data['entries']), 'actions': len(data['actions']), 'revision': data['revision']}


def normalize(value):
    decomposed = unicodedata.normalize('NFKD', value).casefold()
    return re.sub(r'\W+', ' ', ''.join(c for c in decomposed if not unicodedata.combining(c))).strip()


def compact(entry, coaching):
    fields = ['id', 'channel', 'target_id', 'delivered_at', 'delivery_date', 'manual_publication_state', 'publication_attempt', 'published_on', 'publication_confirmation', 'created_at', 'status', 'subject', 'objective', 'pillar', 'angle',
              'audience_primary', 'audience_need', 'ideas_developed', 'editorial_fingerprint',
              'participation', 'feedback', 'published_at', 'publication_url']
    if coaching:
        fields.append('audience_review')
    row, truncated = {}, []
    for key in fields:
        if key not in entry:
            continue
        value = entry[key]
        if key == 'audience_review' and isinstance(value, dict):
            value = {k: value[k] for k in ('state', 'observed_at', 'source', 'coverage', 'post_age_days',
                                          'metrics', 'summary', 'hypotheses') if k in value}
        rendered = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        budget = 2400 if key == 'audience_review' else 1200 if key in {'ideas_developed', 'editorial_fingerprint'} else 600
        if len(rendered) > budget:
            value = rendered[:budget] + '… [extrait tronqué]'
            truncated.append(key)
        row[key] = value
    if truncated:
        row['truncated_fields'] = truncated
    return row


def context(data, limit=20, offset=0, query=None, ids=None, coaching=False, channel=None):
    require(1 <= limit <= 50 and offset >= 0, 'limit 1..50 and offset >= 0 required')
    entries = sorted(data['entries'], key=lambda e: stamp(e['created_at']), reverse=True)
    if coaching:
        entries = entries[:365]
    if channel:
        require(channel in {'page', 'profile'}, 'Invalid channel filter')
        entries = [e for e in entries if e.get('channel') == channel]
    coverage = {'channel': channel, 'total_entries': len(data['entries']), 'window_entries': len(entries),
                'window_limit': 365 if coaching else None, 'order': 'created_at_desc'}
    if ids:
        require(len(ids) <= 20, 'At most 20 complete entries per call')
        by_id = {e['id']: e for e in entries}
        require(all(i in by_id for i in ids), 'An id is absent from this history window')
        return {**coverage, 'mode': 'exact_entries', 'entries': [by_id[i] for i in ids]}
    if query:
        terms = normalize(query).split()
        require(bool(terms), 'Query must contain searchable terms')
        fields = ('subject', 'objective', 'pillar', 'angle', 'audience_primary', 'audience_need',
                  'ideas_developed', 'editorial_fingerprint', 'text', 'participation', 'feedback')
        if coaching:
            fields += ('audience_review',)
        def score(entry):
            haystack = normalize(json.dumps({k: entry.get(k) for k in fields}, ensure_ascii=False))
            return sum(term in haystack for term in terms)
        entries = sorted((e for e in entries if score(e)), key=score, reverse=True)
    return {**coverage, 'total_matches': len(entries), 'offset': offset, 'limit': limit,
            'next_offset': offset + limit if offset + limit < len(entries) else None,
            'entries': [compact(e, coaching) for e in entries[offset:offset + limit]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['validate', 'context', 'coach-context', 'actions'])
    parser.add_argument('path', type=Path)
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--query')
    parser.add_argument('--channel', choices=['page', 'profile'])
    parser.add_argument('--ids', nargs='+')
    parser.add_argument('--all', action='store_true', help='Include completed and cancelled actions')
    args = parser.parse_args()
    data = json.loads(args.path.read_text(encoding='utf-8'))
    result = validate(data)
    if args.action in {'context', 'coach-context'}:
        result['context'] = context(data, args.limit, args.offset, args.query, args.ids,
                                    coaching=args.action == 'coach-context', channel=args.channel)
    elif args.action == 'actions':
        require(1 <= args.limit <= 50 and args.offset >= 0, 'Invalid pagination')
        actions = [a for a in data['actions'] if args.all or a['status'] not in {'completed', 'cancelled'}]
        result['total_matches'] = len(actions)
        result['actions'] = actions[args.offset:args.offset + args.limit]
        result['next_offset'] = args.offset + args.limit if args.offset + args.limit < len(actions) else None
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, AttributeError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
