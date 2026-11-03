import copy
import json
from pathlib import Path
import unittest
from resoudre_skill import resolve,ROOT
from verifier_relecture import check

class RoutingTests(unittest.TestCase):
    def test_all_sixteen_routes_resolve(self):
        routes=json.loads((ROOT/'references/skills-map.json').read_text())['skills']
        self.assertEqual(len(routes),16)
        for name in routes:self.assertTrue(Path(resolve(name)['skill_file']).is_file())
    def test_reference_resolves_under_own_skill(self):
        self.assertTrue(Path(resolve('equipe-exploiter-bibliotheque-creative','references/banque-accroches.md')['reference_file']).is_file())
    def test_unknown_or_escape_refused(self):
        for name,ref in [('equipe-inconnu',None),('equipe-configurer-espace','../../plugin.json'),('equipe-configurer-espace','/etc/passwd')]:
            with self.assertRaises(ValueError):resolve(name,ref)
    def test_resource_has_fifty_original_mechanisms(self):
        p=ROOT/'skills/equipe-exploiter-bibliotheque-creative/references/banque-accroches.md'
        lines=[line for line in p.read_text().splitlines() if line.startswith('| ') and line[2:4].isdigit()]
        self.assertEqual([line[2:4] for line in lines],[f'{i:02}' for i in range(1,51)])
        catalogue=json.loads((ROOT/'assets/catalogue.json').read_text())
        self.assertEqual(len([r for r in catalogue if r['Identifiant']=='R001']),1)

class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.data={'author_id':'assistant','artifact_sha256':'a'*64,'revision':2,'destination':'canal-test','required_domains':['fond','lecture','media'],'media_type':'video','review_mode':'human','reviews':[{'reviewer_id':'conseiller-test','reviewer_type':'human','evidence_ref':'avis-test','artifact_sha256':'a'*64,'revision':2,'destination':'canal-test','domains':['fond','lecture','media'],'media_inspected':True,'continuous_viewing':True,'audio_listened':True,'decision':'accepted'}]}
    def test_actual_human_record_can_close_quality_but_not_publish(self):
        result=check(self.data);self.assertTrue(result['quality_gate_passed']);self.assertFalse(result['publication_authorized'])
    def test_self_review_does_not_close_quality(self):
        self.data['review_mode']='self_review';self.assertFalse(check(self.data)['quality_gate_passed'])
    def test_stale_version_wrong_destination_or_missing_evidence_refused(self):
        for key,value in [('revision',1),('artifact_sha256','b'*64),('destination','other'),('evidence_ref',None),('reviewer_id','assistant')]:
            d=copy.deepcopy(self.data);d['reviews'][0][key]=value;self.assertFalse(check(d)['quality_gate_passed'])
    def test_video_requires_real_viewing_and_audio(self):
        for key in ['media_inspected','continuous_viewing','audio_listened']:
            d=copy.deepcopy(self.data);d['reviews'][0][key]=False;self.assertFalse(check(d)['quality_gate_passed'])
    def test_blocker_prevents_release(self):
        self.data['open_blockers']=['fait à vérifier'];self.assertFalse(check(self.data)['quality_gate_passed'])
    def test_independent_arbitration_must_be_distinct(self):
        d=copy.deepcopy(self.data);d['review_mode']='independent_agents';d['reviews'][0]['reviewer_type']='agent'
        self.assertFalse(check(d)['quality_gate_passed'])
        d['independent_decision']={k:v for k,v in d['reviews'][0].items() if k in ['reviewer_id','evidence_ref','artifact_sha256','revision','destination','decision']}
        self.assertFalse(check(d)['quality_gate_passed'])
        d['independent_decision']['reviewer_id']='arbitre-test';self.assertFalse(check(d)['quality_gate_passed'])
        d['reviews']=[dict(d['reviews'][0],reviewer_id='critique-'+domain,domains=[domain]) for domain in ['fond','lecture','media']]
        self.assertTrue(check(d)['quality_gate_passed'])

if __name__=='__main__':unittest.main()
