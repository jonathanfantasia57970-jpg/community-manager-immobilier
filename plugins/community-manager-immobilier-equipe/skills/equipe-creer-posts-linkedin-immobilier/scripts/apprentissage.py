#!/usr/bin/env python3
"""Validate the bounded learning memory locally; never collect or mutate data."""
import argparse
import json
from datetime import date
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def words(value):
    if isinstance(value, str):
        return len(value.split())
    if isinstance(value, list):
        return sum(words(item) for item in value)
    if isinstance(value, dict):
        return sum(words(item) for item in value.values())
    return 0


def validate(data):
    require(isinstance(data, dict), 'Memory must be an object')
    require(data.get('schema_version') == 1, 'Unsupported schema_version')
    require(isinstance(data.get('profile_id'), str) and bool(data['profile_id'].strip()) and data.get('memory_key') == 'linkedin-' + data['profile_id'] + '-learning', 'Wrong memory')
    require(type(data.get('revision')) is int and data['revision'] >= 1, 'Invalid revision')
    date.fromisoformat(data['updated_on'])
    require(data.get('status') in {'awaiting_requested_collection', 'has_observations'}, 'Invalid status')
    require(isinstance(data.get('coverage'), str), 'Missing coverage')
    insights, experiments = data.get('insights'), data.get('experiments')
    require(isinstance(insights, list) and len(insights) <= 12, 'At most 12 insights')
    require(isinstance(experiments, list) and len(experiments) <= 3, 'At most 3 experiments')
    seen = set()
    for entry in insights + experiments:
        require(isinstance(entry, dict), 'Invalid learning entry')
        key = entry.get('id')
        require(isinstance(key, str) and bool(key.strip()), 'Missing learning id')
        require(key not in seen, 'Duplicate learning id')
        seen.add(key)
    for entry in insights:
        for field in ('statement', 'scope', 'limits', 'updated_on'):
            require(isinstance(entry.get(field), str) and bool(entry[field].strip()), 'Missing insight ' + field)
        date.fromisoformat(entry['updated_on'])
        require(entry.get('confidence') in {'low', 'moderate', 'high'}, 'Invalid confidence')
        require(entry.get('status') in {'hypothesis', 'supported', 'contested'}, 'Invalid insight status')
        require(isinstance(entry.get('evidence'), dict), 'Missing evidence')
        evidence = entry['evidence']
        for field in ('period', 'note'):
            require(isinstance(evidence.get(field), str) and bool(evidence[field].strip()), 'Missing evidence ' + field)
        require('distinct_posts' in evidence, 'Missing distinct_posts (null if unknown)')
        count = evidence['distinct_posts']
        require(count is None or (type(count) is int and count >= 0), 'Invalid distinct_posts')
        refs = evidence.get('refs')
        require(isinstance(refs, list) and len(refs) <= 5, 'At most 5 representative references')
        require(all(isinstance(ref, str) and ref.strip() for ref in refs), 'Invalid reference')
        require(len(refs) == len(set(refs)), 'Duplicate reference')
    for entry in experiments:
        for field in ('proposal', 'basis', 'objective', 'evaluation', 'status'):
            require(isinstance(entry.get(field), str) and bool(entry[field].strip()), 'Missing experiment ' + field)
        require(entry['status'] in {'proposed', 'accepted', 'completed', 'declined'}, 'Invalid coaching status')
        if entry['status'] in {'accepted', 'completed', 'declined'}:
            require(isinstance(entry.get('user_confirmation'), str) and entry['user_confirmation'].strip(),
                    'A coaching decision requires user_confirmation')
        if entry['status'] in {'accepted', 'completed'}:
            require(isinstance(entry.get('scope'), str) and entry['scope'].strip(),
                    'An accepted coaching action requires scope')
    require('last_batch' in data, 'Missing last_batch')
    batch = data['last_batch']
    if batch is not None:
        require(isinstance(batch, dict), 'Invalid last_batch')
        require(isinstance(batch.get('id'), str) and batch['id'].strip(), 'Missing batch id')
        require(isinstance(batch.get('applied_observations'), list), 'Missing batch observations')
        require(len(batch['applied_observations']) <= 20, 'At most 20 observations per saved sub-batch')
        keys = []
        for item in batch['applied_observations']:
            require(isinstance(item, dict), 'Invalid batch observation')
            require(all(isinstance(item.get(k), str) and item[k].strip()
                        for k in ('entry_id', 'observation_id')), 'Invalid observation identity')
            keys.append((item['entry_id'], item['observation_id']))
        require(len(keys) == len(set(keys)), 'Duplicate batch observation')
    if data['status'] == 'awaiting_requested_collection':
        require(not insights and batch is None, 'Uncollected memory cannot contain audience results')
    count = words(data)
    require(count <= 800, f'Memory exceeds 800 words ({count})')
    return {'valid': True, 'words': count, 'insights': len(insights),
            'experiments': len(experiments), 'revision': data['revision']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.path.read_text(encoding='utf-8')))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
