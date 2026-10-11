import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('actor_packet',Path(__file__).resolve().parents[1]/'scripts/actor_packet.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

class ActorPacketTests(unittest.TestCase):
    def test_isolated_actor_allowlist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'repo';root.mkdir()
            def put(name,data='source'):
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data)
            for n in a.COMMON|{'harness/PROPOSER.md','harness/CHALLENGER.md','harness/VERIFIER.md','domains/D01/README.md','domains/D01/brief.json','domains/D02/brief.json','private/secret'}:put(n)
            put('config/agents.json',json.dumps({'actors':[{'actor_id':'Codex-P01-ARCH','platform':'OpenAI Codex','role':'proposer','domain_ids':['D01'],'model_requested':'gpt-6-astra','reasoning_requested':'max'}]}))
            put('config/agents-deepseek.json',json.dumps({'actors':[{'actor_id':'DeepSeek-C01-ARCH','platform':'DeepSeek','role':'challenger','domain_ids':['D01'],'model_requested':'deepseek-flash','reasoning_requested':'medium'}]}))
            put('config/agents-claude.json',json.dumps({'actors':[{'actor_id':'Claude-V01-DIGITAL','platform':'Claude','role':'verifier','domain_ids':['D01'],'model_requested':'claude-family:lightweight-exposed','reasoning_requested':'medium'}]}))
            put('config/launch-release.json',json.dumps({'released_actors':['Codex-P01-ARCH','DeepSeek-C01-ARCH','Claude-V01-DIGITAL'],
                                                         'first_wave':['Codex-P01-ARCH'],
                                                         'topic_containers':{'D01':'EDA-0001'},
                                                         'assignments':{'EDA-0001':{'domain':'D01','proposer':'Codex-P01-ARCH','challenger':'DeepSeek-C01-ARCH','verifier':'Claude-V01-DIGITAL'}}}))
            put('candidates/EDA-0001/proposal.md','proposal')
            put('candidates/EDA-0001/challenges.md','withheld challenge')
            put('candidates/EDA-0001/dossier.json',json.dumps({'status':'draft','proposer_session':None,'challenger_session':None}))
            def git(*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL)
            git('init');git('add','.');git('-c','user.name=test','-c','user.email=test@example.com','commit','-m','fixture')
            ref=git('rev-parse','HEAD').decode().strip()
            out=Path(tmp)/'packet'
            result=a.make_packet(root,'Codex-P01-ARCH',ref,out,Path(tmp)/'Codex-P01-ARCH')
            manifest=json.loads((out/'PACKET.json').read_text())
            self.assertIn('harness/PROPOSER.md',manifest['files'])
            self.assertNotIn('harness/CHALLENGER.md',manifest['files'])
            self.assertNotIn('domains/D02/brief.json',manifest['files'])
            self.assertNotIn('private/secret',manifest['files'])
            self.assertNotIn('config/agents.json',manifest['files'])
            self.assertEqual(result['input_commit'],ref)
            self.assertEqual(len(result['packet_sha256']),64)
            research=Path(tmp)/'research-packet'
            research_result=a.make_packet(root,'Codex-P01-ARCH',ref,research,Path(tmp)/'research-outbox'/'Codex-P01-ARCH',
                                          phase='research',topic='EDA-0001')
            research_manifest=json.loads((research/'PACKET.json').read_text())
            self.assertEqual(research_result['input_commit'],ref)
            self.assertIn('candidates/EDA-0001/proposal.md',research_manifest['files'])
            self.assertNotIn('candidates/EDA-0001/challenges.md',research_manifest['files'])
            self.assertEqual(json.loads((research/'ASSIGNMENT.json').read_text())['topic'],'EDA-0001')
            with self.assertRaises(ValueError):a.make_packet(root,'Codex-P01-ARCH',ref,out,Path(tmp)/'Codex-P01-ARCH')
            with self.assertRaises(ValueError):a.make_packet(root,'Codex-P01-ARCH','HEAD',Path(tmp)/'bad',Path(tmp)/'Codex-P01-ARCH')
            with self.assertRaises(ValueError):a.make_packet(root,'Codex-P01-ARCH',ref,Path(tmp)/'wrong-topic',
                                                             Path(tmp)/'outbox2'/'Codex-P01-ARCH',phase='research',topic='EDA-9999')
            with self.assertRaises(ValueError):a.make_packet(root,'Codex-P01-ARCH',ref,Path(tmp)/'bad-outbox-packet',
                                                             root/'candidates/EDA-0001',phase='research',topic='EDA-0001')
            with self.assertRaises(ValueError):a.make_packet(root,'DeepSeek-C01-ARCH',ref,Path(tmp)/'early-challenger',
                                                             Path(tmp)/'out'/'DeepSeek-C01-ARCH',phase='research',topic='EDA-0001')
            put('candidates/EDA-0001/dossier.json',json.dumps({'status':'submitted','proposer_session':'p','challenger_session':None}))
            git('add','.');git('-c','user.name=test','-c','user.email=test@example.com','commit','-m','submit proposal')
            submitted=git('rev-parse','HEAD').decode().strip()
            challenger=Path(tmp)/'challenger-initial'
            c_result=a.make_packet(root,'DeepSeek-C01-ARCH',submitted,challenger,
                                   Path(tmp)/'challenge-out'/'DeepSeek-C01-ARCH',phase='research',topic='EDA-0001')
            self.assertEqual(json.loads((challenger/'PACKET.json').read_text())['registry'],'config/agents-deepseek.json')
            self.assertEqual(c_result['input_commit'],submitted)
            with self.assertRaises(ValueError):a.make_packet(root,'DeepSeek-C01-ARCH',submitted,Path(tmp)/'early-full',
                                                             Path(tmp)/'full-out'/'DeepSeek-C01-ARCH',phase='research',topic='EDA-0001',stage='full')
            put('candidates/EDA-0001/dossier.json',json.dumps({'status':'submitted','proposer_session':'p','challenger_session':'c'}))
            put('candidates/EDA-0001/challenges.md','# Challenges\n\n## Independent estimate before forecast exposure\n\nIndependent estimate recorded.\n')
            git('add','.');git('-c','user.name=test','-c','user.email=test@example.com','commit','-m','freeze challenge')
            challenged=git('rev-parse','HEAD').decode().strip()
            verifier=Path(tmp)/'verifier-full'
            v_result=a.make_packet(root,'Claude-V01-DIGITAL',challenged,verifier,
                                   Path(tmp)/'verify-out'/'Claude-V01-DIGITAL',phase='research',topic='EDA-0001',stage='full')
            self.assertEqual(json.loads((verifier/'PACKET.json').read_text())['registry'],'config/agents-claude.json')
            self.assertEqual(v_result['input_commit'],challenged)
