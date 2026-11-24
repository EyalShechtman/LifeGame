# LifeGame

A 3D card room in the browser (Three.js). You walk in as the dog, take the empty seat, and each player at the table pitches one project. Fold, call, raise or go all in.

## Run it

It is a static site. Serve the folder and open it:

```bash
python3 -m http.server 8765
```

Then go to http://localhost:8765.

Controls: WASD to move, mouse to look, Shift to run, E to interact, V for the dog's eyes, M for music.

## Files

- `index.html`: the whole game.
- `dog_rigged.glb.b64.txt`: the rigged, animated body (base64 GLB).
- `dog_head.glb.b64.txt`: the high-detail head (base64 GLB).
- `dog.webp`: title-screen picture.
- `autumn-leaves.mp3` (not in the repo): optional background track. Without it the room plays generated lounge jazz.
- `tools/`: the Python scripts used to build the models and textures.
