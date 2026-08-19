#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
INCLUDE=['00_START_HERE.md','README.md','CHANGELOG.md','CLAUDE.md','CLAUDE_CODE_EXECUTION_INTAKE.md','.gitignore','pyproject.toml','requirements-test.txt','requirements-tools.txt','content','public','src','scripts','tests','docs','.github']
EX={'MANIFEST.json','SHA256SUMS.txt','__pycache__','.pytest_cache'}
files=[]
for rel in INCLUDE:
 p=ROOT/rel
 if p.is_file(): files.append(p)
 elif p.is_dir(): files += [x for x in p.rglob('*') if x.is_file() and not any(part in EX for part in x.parts) and x.name not in EX]
files=sorted(set(files),key=lambda p:p.relative_to(ROOT).as_posix())
rows=[]
for p in files:
 b=p.read_bytes();rows.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(b).hexdigest(),'size':len(b)})
fp=hashlib.sha256(''.join(f"{r['path']}\0{r['sha256']}\n" for r in rows).encode()).hexdigest()
out={'candidate':'The Black Bird Field v08.2','fingerprint':fp,'material_file_count':len(rows),'files':rows}
print(json.dumps(out,indent=2) if '--json' in __import__('sys').argv else fp)
