# 2026-10-06 — .gitignore

Extended the existing `.gitignore` with: `dataset/`, `runs/`, `yolo12n.pt` (YOLO training
artifacts / auto-downloaded base weights), `*.zip`, `.ipynb_checkpoints/`,
`.claude/settings.local.json`.

Kept tracked on purpose: `beacon_yolo.pt` (shipped model, bundled by main.spec),
`main.spec`, `installer.iss`, `.claude/completions/`.

Not done: already-committed `node_modules/`, `__pycache__/`, `yolo12n.pt`,
`performance_log.csv`, `release.zip` remain in the index until removed with
`git rm -r --cached`.
