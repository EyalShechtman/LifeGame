# LifeGame

A 3D card room in the browser (Three.js). You walk in as the dog, take the empty seat, and each player at the table pitches one project. Fold, call, raise or go all in.

Around the room: a bar with a bartender (Guinness or Super Bock), a library of essays next to the fireplace, a chess table where EyalBot plays you, the soccer wall and TV, and the Music Corner with a grand piano you can play.

First-time visitors get a short welcome tour (the `#tour` sheet) and then a step-by-step guide with a marker in the room. The contact bar at the top opens the Recruiter view (the `#quick` sheet): everything on one page.

Live at https://lifegame-88o.pages.dev, moving to https://eyalshechtman.com.

## Run it

It is a static site with no build step. Serve `public/` and open it:

```bash
python3 -m http.server 8765 -d public
```

Then go to http://localhost:8765.

Controls: WASD to move, mouse to look, Shift to run, E to interact, V for the dog's eyes, M for music.

## Deploy

A push to `main` deploys `public/` to the Cloudflare Pages project `lifegame` (`.github/workflows/deploy.yml`). Only `public/` is published; `tools/` and the docs are not.

## Files

```
public/                    everything the site serves (deployed as-is)
  index.html               the HTML: title screen, HUD, sheets, importmap for three.js
  src/
    styles.css             all the CSS
    main.js                the game: renderer, room, characters, input, stations, loop
    content.js             the players (projects), their looks, and the chapter cards
    chess-engine.js        chess rules and the fallback engine (no DOM, no three.js)
  assets/
    dog_rigged.glb.b64.txt the rigged, animated body (base64 GLB)
    dog_head.glb.b64.txt   the high-detail head (base64 GLB)
    dog.webp               title-screen picture
    autumn-leaves.mp3      the background track; if it can't load, the room plays generated lounge jazz
    chess/                 EyalBot's model (bot.onnx) and its move list
    soccer/                album photos and the TV crests (crest.jpg for Bellevue Athletic, highschool.png for the high school TV)
    essays/                the essays in the library (Markdown, listed in essays/index.json)
tools/                     build-only Python scripts, not deployed (see tools/README.md)
```

## Working in parallel

Several agents edit this site at once. Edit the file that owns what you are changing:

- Project text, player looks, the chapter cards (flag, soccer, contact): `public/src/content.js`.
- Styles for any HUD, sheet or menu: `public/src/styles.css`.
- Markup (title screen, contact bar, Recruiter view, tour, menus): `public/index.html`.
- Chess rules or the fallback engine: `public/src/chess-engine.js`.
- Everything else is in `public/src/main.js`, in sections marked by banners like `/* ---------------- the bar: ... ---------------- */`. The main ones: room and decor, poker table, the music corner (piano build, then "sit at the grand and play it"), characters, input, music, contact bar / recruiter view / tour, first-visit guide, interactions, soccer corner, stations (bar, library, chess), minimap, loop. Keep edits inside the section you own.
- New files the site loads go in `public/assets/` and are referenced as `assets/...`.

`main.js` stays one module on purpose: its sections share mutable state (`mode`, `yaw`, `pitch`, `pov`, `speed`, …) and call each other in both directions, so splitting it further would mean changing logic.

If you have an old single-file `index.html` (the layout before `public/`), don't hand-merge it: run `python3 tools/split_index.py path/to/index.html` and it writes the split files.

## Adding an essay to the library

Each essay is a book on the shelf by the fireplace.

1. Write it in Markdown and save it in `public/assets/essays/`, for example `why-i-build.md`. Use `#` for the title and `##` for section headings.
2. Add a line for it to `public/assets/essays/index.json`:

```json
[
  { "file": "why-i-build.md", "title": "Why I Build", "sub": "2026" }
]
```

3. Push to `main`. The site redeploys and the book appears on the shelf. The "Essays · Coming soon" placeholder disappears once there is at least one essay.

## The chess bot

EyalBot is the Maia-2 model fine-tuned on Eyal's chess.com games in `~/Documents/projects/chess-bot`. It was exported to ONNX with int8 weights (`public/assets/chess/bot.onnx`, about 22 MB) and runs in the visitor's browser with onnxruntime-web, so there is no server. It predicts the move Eyal would play and does not search ahead; it samples a little warmer than the model so games vary. If the model can't load, a small built-in engine plays instead.

To update the bot after retraining, re-export `models/my_bot.pt` to ONNX the same way (inputs `boards` [1,18,8,8], `elo_self`, `elo_oppo`; output `logits` [1,1880]) and replace `public/assets/chess/bot.onnx`. `CHESS_BOT_URL` in `public/src/main.js` is an optional override for a bot served over HTTP: it receives `POST { "fen", "moves" }` and returns `{ "move" }`.
