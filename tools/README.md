# tools/

Build-only scripts. Nothing in this folder is deployed: the site is `public/` only.

- `split_index.py`: turns a monolithic `index.html` (the old single-file layout) into `public/index.html` + `public/src/*`, and rewrites asset paths to `assets/`. Mechanical, no logic changes. Use it to bring an old-layout `index.html` across: `python3 tools/split_index.py path/to/index.html`.
- The rest (`glb.py`, `cut_head.py`, `merge_anims.py`, `retex.py`, `project.py`, `face.py`, `prof.py`, `islands.py`, `glb2obj.py`) built the dog models in `public/assets/dog_*.glb.b64.txt`: inspecting GLBs, cutting the head, merging animations, retexturing. They need `numpy` and `Pillow`.
