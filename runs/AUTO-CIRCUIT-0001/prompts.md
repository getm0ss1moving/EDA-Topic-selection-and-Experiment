# Operator prompts for AUTO-CIRCUIT-0001

Send each prompt verbatim into the role's own session. Both are coordinator transport notices,
not scientific instructions.

## Proposer (`Claude-P05-TIMING`, already running; no restart)

> Coordinator notice, transport only: policy amendment CLD-P05-AMEND-0002 is in your round inbox at `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/rounds/EDA-0002/Claude-P05-TIMING/COORDINATOR-AMENDMENT-0002`. The SHA-256 of its `AMENDMENT.json` must be `d85b344a78650ef3d596f5614366016716bc2f08a165c12cf3cfaf527697644d`. Verify it and every listed file, read `CHANGES.md` and the files it cites, and write the receipt it specifies. Then do the bootstrap in rule 2 (freeze R1b unchanged and send it), start the new background wait with this bundle's tools, and end the turn. From then on, work automatically as `CHANGES.md` describes.

## Verifier (`DeepSeek-V02-PHYSICAL`)

1. Exit the session that is still running from the pre-#31 launcher.
2. In Terminal.app, run `runs/DSK-C04C05-LAUNCH-0001/launch.sh --actor DeepSeek-V02-PHYSICAL --check-resume`
   from a checkout that contains #31's launcher, then repeat with `--resume` instead of
   `--check-resume`.
3. Send:

> Coordinator notice, transport only. Two amendments are in your round inbox `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/rounds/EDA-0002/DeepSeek-V02-PHYSICAL`: `COORDINATOR-REAL-ROLE-INBOX-0001` (`AMENDMENT.json` SHA-256 `48e391fbb4bd62624d668527e38b15f622c0b5565a330f62448164e2d316f5c4`) and `COORDINATOR-AUTO-CIRCUIT-0001` (`d48ab6d0f36a3408d3291242100e696807f1458a1bfa536b92c1fa9fcf1084e4`). Verify both and every listed file. Read the first bundle's `INSTRUCTIONS.md` and the second's `CHANGES.md`; where they differ, the second applies. Write both receipts in your outbox. Then follow `CHANGES.md`: freeze and send your round-0 ruling as the bootstrap round, start the background wait, and from then on work automatically. Never claim acceptance or authorize experiments.
