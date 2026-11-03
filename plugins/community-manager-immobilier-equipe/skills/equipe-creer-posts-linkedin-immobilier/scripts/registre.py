#!/usr/bin/env python3
"""Validate or summarize a local copy; never read/write the remote registry."""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

STATUSES = {'prepared', 'incomplete', 'approved', 'published', 'rejected'}
REQUIRED = ('id', 'created_at', 'pillar', 'subject', 'scene', 'thesis',
            'takeaway', 'hook', 'text', 'status', 'scope', 'visual', 'versions', 'version')

def normalize(value):
    value = unicodedata.normalize('NFKD', value).casefold()
    return re.sub(r'\W+', ' ', ''.join(c for c in value if not unicodedata.combining(c))).strip()

def fingerprint(entry):
    return hashlib.sha256(normalize(entry['text']).encode()).hexdigest()

def validate(data):
    assert data.get('schema_version') == 1, 'Unsupported schema_version'
    assert isinstance(data.get('profile_id'), str) and bool(data['profile_id'].strip()) and data.get('registry_key') == 'linkedin-' + data['profile_id'] + '', 'Wrong registry'
    assert isinstance(data.get('entries'), list), 'entries must be a list'
    assert isinstance(data.get('preferences'), list), 'preferences must be a list'
    ids, seen_texts, warnings = set(), {}, []
    for e in data['entries']:
        assert isinstance(e, dict), 'entry must be an object'
        assert all(k in e for k in REQUIRED), 'Missing required entry fields'
        assert all(isinstance(e[k], str) and e[k].strip() for k in REQUIRED
                   if k not in {'visual', 'versions', 'version'}), 'Empty or invalid string'
        assert type(e['version']) is int and e['version'] >= 1, 'Invalid version'
        assert e['id'] not in ids, 'Duplicate entry id: ' + e['id']
        ids.add(e['id'])
        stamp = datetime.fromisoformat(e['created_at'].replace('Z', '+00:00'))
        assert stamp.tzinfo is not None, 'created_at must have a timezone'
        assert e['status'] in STATUSES, 'Invalid status'
        assert e['scope'] in {'full', 'text_only', 'brief'}, 'Invalid scope'
        assert isinstance(e['visual'], dict), 'visual must be an object'
        assert e['visual'].get('state') in {'created', 'missing', 'not_requested'}, 'Invalid visual state'
        assert isinstance(e['versions'], list), 'versions must be a list'
        missing_index = [k for k in ('angle', 'ideas_developed') if k not in e]
        if missing_index:
            warnings.append({'type': 'ideas_not_indexed', 'id': e['id'],
                             'fields': missing_index})
        if 'angle' in e:
            assert isinstance(e['angle'], str) and e['angle'].strip(), 'Invalid angle'
        if 'ideas_developed' in e:
            ideas = e['ideas_developed']
            assert isinstance(ideas, list) and ideas, 'ideas_developed must be a nonempty list'
            for idea in ideas:
                assert isinstance(idea, dict), 'Developed idea must be an object'
                assert isinstance(idea.get('idea'), str) and idea['idea'].strip(), 'Invalid developed idea'
                assert idea.get('role') in {'central', 'supporting', 'conclusion'}, 'Invalid idea role'
        if e['status'] in {'approved', 'published'}:
            assert e.get('user_confirmation'), 'User confirmation required'
        if e['status'] == 'published':
            assert e.get('publication_evidence'), 'Publication evidence required'
        if e['scope'] == 'full' and e['status'] in {'prepared', 'approved', 'published'}:
            assert e['visual'].get('state') == 'created', 'Final image required'
        if e['status'] in {'prepared', 'approved', 'published'}:
            assert e.get('review'), 'Review required for complete outputs'
        fp = fingerprint(e)
        if fp in seen_texts:
            warnings.append({'type': 'same_normalized_text', 'ids': [seen_texts[fp], e['id']]})
        seen_texts[fp] = e['id']
    return warnings

def context(data, limit=20, offset=0, query=None, entry_ids=None, coaching=False):
    if not 1 <= limit <= 50 or offset < 0:
        raise ValueError('limit must be 1..50 and offset nonnegative')
    entries = sorted(data['entries'], key=lambda e: datetime.fromisoformat(
        e['created_at'].replace('Z', '+00:00')))
    window = {}
    if coaching:
        entries = entries[-365:]
        window = {'coaching_window': {
            'max_entries': 365, 'available_entries': len(entries),
            'order': 'created_at_desc',
            'oldest_created_at': entries[0]['created_at'] if entries else None,
            'newest_created_at': entries[-1]['created_at'] if entries else None,
        }}
    if entry_ids:
        if len(entry_ids) > 20:
            raise ValueError('At most 20 exact entries per request')
        by_id = {e['id']: e for e in entries}
        missing = set(entry_ids) - by_id.keys()
        if missing:
            raise ValueError('Unknown entry ids: ' + ', '.join(sorted(missing)))
        return {'entries': [by_id[i] for i in entry_ids], 'mode': 'exact_entries', **window}
    matches = list(reversed(entries))
    if query:
        terms = normalize(query).split()
        if not terms:
            raise ValueError('query must contain searchable terms')
        search_fields = ('pillar', 'subject', 'scene', 'thesis', 'takeaway',
                         'angle', 'ideas_developed', 'hook', 'text')
        if coaching:
            search_fields += ('feedback', 'audience_review')
        def score(entry):
            haystack = normalize(json.dumps(
                {k: entry.get(k) for k in search_fields}, ensure_ascii=False))
            return sum(term in haystack for term in terms)
        matches = sorted((e for e in matches if score(e)), key=score, reverse=True)
    selected = matches[offset:offset + limit]
    fields = ('id', 'created_at', 'status', 'pillar', 'subject', 'scene',
              'thesis', 'takeaway', 'angle', 'ideas_developed', 'hook',
              'published_at', 'publication_url', 'feedback')
    def compact(entry):
        row, truncated = {}, []
        for k in fields:
            if k not in entry:
                continue
            value = entry[k]
            rendered = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
            budget = 1200 if k == 'ideas_developed' else 600 if k == 'feedback' else 300
            if len(rendered) > budget:
                value = rendered[:budget] + '… [extrait tronqué]'
                truncated.append(k)
            row[k] = value
        review = entry.get('audience_review')
        if isinstance(review, dict):
            row['audience_review_state'] = review.get('state')
            row['audience_review_observed_at'] = review.get('observed_at')
            row['audience_review_applied_revision'] = review.get('applied_to_memory_revision')
            if coaching:
                review_fields = ('state', 'observed_at', 'source', 'coverage',
                                 'post_age_days', 'metrics', 'summary', 'hypotheses')
                review_excerpt = {k: review[k] for k in review_fields if k in review}
                rendered = json.dumps(review_excerpt, ensure_ascii=False)
                if len(rendered) > 2400:
                    review_excerpt = rendered[:2400] + '… [extrait tronqué]'
                    truncated.append('audience_review')
                row['audience_review'] = review_excerpt
        if truncated:
            row['truncated_fields'] = truncated
        return row
    return {'coverage': data.get('coverage'), 'preferences': data['preferences'],
            'assets': data.get('reference_assets', []),
            'last_12_pillars': dict(Counter(e['pillar'] for e in entries[-12:])),
            'total_entries': len(data['entries']), 'total_matches': len(matches), **window,
            'offset': offset, 'limit': limit,
            'next_offset': offset + limit if offset + limit < len(matches) else None,
            'entries': [compact(e) for e in selected],
            'note': ('Coaching history window; read relevant texts and reviews with --ids. '
                    'Traverse all pages only when the requested analysis calls for it.' if coaching else
                    'Bounded lexical index, not a semantic novelty check. '
                    'Read close entries in full with --ids; no automatic full-history traversal.')}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['validate', 'context', 'coach-context'])
    parser.add_argument('path', type=Path)
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--query')
    parser.add_argument('--ids', nargs='+')
    args = parser.parse_args()
    data = json.loads(args.path.read_text(encoding='utf-8'))
    warnings = validate(data)
    result = {'valid': True, 'entries': len(data['entries']), 'warnings': warnings}
    if args.action in {'context', 'coach-context'}:
        result['warnings'] = warnings[:20]
        result['warnings_total'] = len(warnings)
        result['context'] = context(data, args.limit, args.offset, args.query, args.ids,
                                    coaching=args.action == 'coach-context')
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        main()
    except (AssertionError, ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
