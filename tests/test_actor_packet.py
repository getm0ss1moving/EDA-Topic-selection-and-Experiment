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
            for n in a.COMMON|{'harness/PROPOSER.md','harness/CHALLENGER.md','domains/D01/README.md','domains/D01/brief.json','domains/D02/brief.json','private/secret'}:put(n)
            put('config/agents.json',json.dumps({'actors':[{'actor_id':'Codex-P01-ARCH','platform':'OpenAI Codex','role':'proposer','domain_ids':['D01'],'model_requested':'gpt-6-astra','reasoning_requested':'max'}]}))
            def git(*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL)
            git('init');git('add','.');git('-c','user.name=test','-c','user.email=test@example.com','commit','-m','fixture')
            ref=git('rev-parse','HEAD').decode().strip()
            out=Path(tmp)/'packet'
            result=a.make_packet(root,'Codex-P01-ARCH',ref,out,Path(tmp)/'outbox')
            manifest=json.loads((out/'PACKET.json').read_text())
            self.assertIn('harness/PROPOSER.md',manifest['files'])
            self.assertNotIn('harness/CHALLENGER.md',manifest['files'])
            self.assertNotIn('domains/D02/brief.json',manifest['files'])
            self.assertNotIn('private/secret',manifest['files'])
            self.assertNotIn('config/agents.json',manifest['files'])
            self.assertEqual(result['input_commit'],ref)
            self.assertEqual(len(result['packet_sha256']),64)
            with self.assertRaises(ValueError):a.make_packet(root,'Codex-P01-ARCH',ref,out,Path(tmp)/'outbox')
            with self.assertRaises(ValueError):a.make_packet(root,'Codex-P01-ARCH','HEAD',Path(tmp)/'bad',Path(tmp)/'outbox')
