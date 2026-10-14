"""Coordinator-only export of immutable role-specific operational amendments."""
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
cfg = json.loads((root/'config/round-transport.json').read_text())
source = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
records = []
for role in ('challenger','verifier'):
    actor = cfg['topics']['EDA-0002']['roles'][role]
    dest = Path(actor['inbox'])/'COORDINATOR-REAL-ROLE-INBOX-0001'
    if dest.exists():
        raise SystemExit(f'Refusing to overwrite {dest}')
    dest.mkdir(parents=True)
    names = ['scripts/round_transmit.py','scripts/role_submission.py','scripts/project.py',
             'config/round-transport.json','docs/AUTO-ROUND.md','docs/SELF-SUBMISSION.md',
             'docs/CHARTER.md','docs/WORKFLOW.md','docs/EVIDENCE.md','docs/ISOLATION.md',
             f'harness/{role.upper()}.md']
    for name in names:
        target=dest/name; target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((root/name).read_bytes())
    instruction = f'''# Operational amendment\n\nActor: {actor['actor_id']}\nSession: {actor['session_id']}\nSource commit: {source}\n\nVerify AMENDMENT.json hashes and record receipt in your own outbox. Keep original input packet provenance. Read only your own harness and inbox, assigned frozen packets and accessible external research sources. Do not read foreign inboxes, private notes, transcripts or memories. No per-source approval is needed for external research.\n\nUse bundled scripts/round_transmit.py and config/round-transport.json. Freeze your own completed outputs, then send. Store processed-deliveries.json in your own outbox, never in an inbox. Acknowledge a delivery only after processing it. Use at most one waiter; a returned wait does not establish model wake-up. Never change governance or use GitHub credentials.\n\n'''
    if role=='challenger':
        instruction += 'Operational scope only: transmit the existing frozen R1b challenge to the verifier, record the delivery ID and receipt, then stop. Do not start a new scientific revision. Codex access restrictions are policy-scoped, not an OS sandbox.\n'
    else:
        instruction += 'Restart the registered session using the reviewed V02 launcher before applying these permissions. Record receipt, then wait for a matching released proposal and challenge pair. The original R0 packet is historical; do not apply its scientific content to the R1b challenge. Missing proposal provenance blocks adjudication. Report a compact claim/evidence/verdict/reason table and machine-readable verdict when a complete pair is available. Do not claim acceptance or authorize experiments.\n'
    (dest/'INSTRUCTIONS.md').write_text(instruction)
    manifest={'actor_id':actor['actor_id'],'session_id':actor['session_id'],'source_commit':source,'files':{str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.rglob('*')) if p.is_file()}}
    (dest/'AMENDMENT.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for p in dest.rglob('*'): p.chmod(0o555 if p.is_dir() else 0o444)
    dest.chmod(0o555)
    records.append({'actor_id':actor['actor_id'],'path':str(dest),'manifest_sha256':hashlib.sha256((dest/'AMENDMENT.json').read_bytes()).hexdigest()})
(root/'runs/REAL-ROLE-INBOX-0001/deployment.json').write_text(json.dumps(records,indent=2)+'\n')
