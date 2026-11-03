#!/usr/bin/env python3
"""Check review record consistency; never attests that a human actually read it."""
import argparse
import json
import re
from itertools import product

def check(data):
    required = set(data.get('required_domains', []))
    if not required or not required <= {'fond','lecture','media'}:
        raise ValueError('Domaines de contrôle manquants ou invalides.')
    if not isinstance(data.get('artifact_sha256'),str) or not re.fullmatch(r'[0-9a-f]{64}',data['artifact_sha256']):
        raise ValueError('Empreinte du livrable requise.')
    if type(data.get('revision')) is not int or data['revision']<1:
        raise ValueError('Révision positive requise.')
    if not data.get('destination') or not data.get('author_id'):
        raise ValueError('Auteur et destination requis.')
    if data.get('open_blockers') or data.get('essential_checks_missing'):
        return {'quality_gate_passed':False,'state':'blocked_on_essential_check'}
    mode = data.get('review_mode')
    if mode not in {'human','independent_agents','self_review'}:
        raise ValueError('Mode de relecture inconnu.')
    if mode=='self_review':
        return {'quality_gate_passed':False,'state':'self_review_only'}
    covered=set();reviewers=set();by_domain={domain:set() for domain in required}
    for record in data.get('reviews',[]):
        same=all(record.get(key)==data[key] for key in ['artifact_sha256','revision','destination'])
        distinct=record.get('reviewer_id') and record['reviewer_id']!=data['author_id']
        proven=record.get('evidence_ref') and record.get('decision')=='accepted'
        if not (same and distinct and proven):continue
        if record.get('reviewer_type')!=('human' if mode=='human' else 'agent'):continue
        domains=set(record.get('domains',[]))
        if 'media' in domains and not record.get('media_inspected'):domains.remove('media')
        if data.get('media_type')=='video' and 'media' in domains and not (record.get('continuous_viewing') and record.get('audio_listened')):domains.remove('media')
        covered.update(domains);reviewers.add(record['reviewer_id'])
        for domain in domains & required: by_domain[domain].add(record['reviewer_id'])
    missing=required-covered
    if missing:return {'quality_gate_passed':False,'state':'awaiting_human_review' if mode=='human' else 'independent_review_incomplete','missing_domains':sorted(missing)}
    if mode=='independent_agents':
        assignments=product(*(by_domain[domain] for domain in sorted(required)))
        if not any(len(set(choice))==len(required) for choice in assignments):
            return {'quality_gate_passed':False,'state':'independent_roles_not_distinct'}
        decision=data.get('independent_decision',{})
        valid=decision.get('reviewer_id') and decision['reviewer_id'] not in reviewers|{data['author_id']} and decision.get('evidence_ref') and decision.get('decision')=='accepted' and all(decision.get(k)==data[k] for k in ['artifact_sha256','revision','destination'])
        if not valid:return {'quality_gate_passed':False,'state':'independent_decision_missing'}
    return {'quality_gate_passed':True,'state':'human_review_complete' if mode=='human' else 'independent_review_complete','publication_authorized':False,'note':'Contrôle documentaire seulement ; vérifier séparément les avis réels et le mandat de diffusion.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('record')
    args=parser.parse_args()
    try:
        with open(args.record,encoding='utf-8') as f:result=check(json.load(f))
        print(json.dumps(result,ensure_ascii=False));raise SystemExit(0 if result['quality_gate_passed'] else 1)
    except (OSError,ValueError,TypeError,KeyError) as exc:parser.exit(2,str(exc)+'\n')
