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
- `autumn-leaves.mp3`: the background track. If it can't load, the room plays generated lounge jazz.
- `chess/`: EyalBot's model (`bot.onnx`) and its move list.
- `soccer/`: album photos and the TV crests (`crest.jpg` for Bellevue Athletic, `highschool.png` for the high school TV).
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

## The chess bot

EyalBot is the Maia-2 model fine-tuned on Eyal's chess.com games in `~/Documents/projects/chess-bot`. It was exported to ONNX with int8 weights (`chess/bot.onnx`, about 22 MB) and runs in the visitor's browser with onnxruntime-web, so there is no server. It predicts the move Eyal would play and does not search ahead; it samples a little warmer than the model so games vary. If the model can't load, a small built-in engine plays instead.

To update the bot after retraining, re-export `models/my_bot.pt` to ONNX the same way (inputs `boards` [1,18,8,8], `elo_self`, `elo_oppo`; output `logits` [1,1880]) and replace `chess/bot.onnx`. `CHESS_BOT_URL` in `index.html` is an optional override for a bot served over HTTP: it receives `POST { "fen", "moves" }` and returns `{ "move" }`.
