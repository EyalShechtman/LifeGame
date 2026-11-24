# LifeGame

A 3D card room in the browser (Three.js). You walk in as the dog, take the empty seat, and each player at the table pitches one project. Fold, call, raise or go all in.

Around the room: a bar with a bartender (Guinness or Super Bock), a library of essays next to the fireplace, a chess table where EyalBot plays you, and the soccer corner.

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
- `essays/`: the essays shown in the library (Markdown, listed in `essays/index.json`).
- `tools/`: the Python scripts used to build the models and textures.

## Adding an essay to the library

Each essay is a book on the shelf by the fireplace.

1. Write it in Markdown and save it in `essays/`, for example `essays/why-i-build.md`. Use `#` for the title and `##` for section headings.
2. Add a line for it to `essays/index.json`:

```json
[
  { "file": "why-i-build.md", "title": "Why I Build", "sub": "2026" }
]
```

3. Push to `main`. The site redeploys and the book appears on the shelf. The "Essays · Coming soon" placeholder disappears once there is at least one essay.

## Connecting the chess bot

The chess table plays a small built-in engine until the real bot is ready. To use the Maia-2 model from `~/Documents/projects/chess-bot`, serve it over HTTP and set `CHESS_BOT_URL` near the top of the chess section in `index.html`. The page sends `POST { "fen": "...", "moves": ["e2e4", ...] }` and expects `{ "move": "e7e5" }` back. If the server does not answer within 8 seconds, the built-in engine moves instead.
