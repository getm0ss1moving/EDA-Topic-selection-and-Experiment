"""Reimplementation of the repository's length-framed dossier digest (read-only check)."""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
h = hashlib.sha256()
for p in sorted(root.rglob('*')):
    if p.is_file() and p.name not in {'verification.json', 'verification.md'}:
        name = p.relative_to(root).as_posix().encode()
        body = p.read_bytes()
        h.update(len(name).to_bytes(8, 'big') + name + len(body).to_bytes(8, 'big') + body)
print(h.hexdigest())
