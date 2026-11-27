export const Chess = (() => {
  const P = 1, N = 2, B = 3, R = 4, Q = 5, K = 6, DBL = 1, EP = 2, CASTLE = 3;
  const VAL = [0, 100, 320, 330, 500, 900, 0];
  const KN = [[1,2],[2,1],[-1,2],[-2,1],[1,-2],[2,-1],[-1,-2],[-2,-1]], DI = [[1,1],[1,-1],[-1,1],[-1,-1]], OR = [[1,0],[-1,0],[0,1],[0,-1]], KG = DI.concat(OR);
  /* piece-square tables, drawn from White's side with rank 8 at the top */
  const T = s => s.trim().split(/[\s,]+/).map(Number);
  const PST = [null,
    T(`0 0 0 0 0 0 0 0 50 50 50 50 50 50 50 50 10 10 20 30 30 20 10 10 5 5 10 25 25 10 5 5 0 0 0 20 20 0 0 0 5 -5 -10 0 0 -10 -5 5 5 10 10 -20 -20 10 10 5 0 0 0 0 0 0 0 0`),
    T(`-50 -40 -30 -30 -30 -30 -40 -50 -40 -20 0 0 0 0 -20 -40 -30 0 10 15 15 10 0 -30 -30 5 15 20 20 15 5 -30 -30 0 15 20 20 15 0 -30 -30 5 10 15 15 10 5 -30 -40 -20 0 5 5 0 -20 -40 -50 -40 -30 -30 -30 -30 -40 -50`),
    T(`-20 -10 -10 -10 -10 -10 -10 -20 -10 0 0 0 0 0 0 -10 -10 0 5 10 10 5 0 -10 -10 5 5 10 10 5 5 -10 -10 0 10 10 10 10 0 -10 -10 10 10 10 10 10 10 -10 -10 5 0 0 0 0 5 -10 -20 -10 -10 -10 -10 -10 -10 -20`),
    T(`0 0 0 0 0 0 0 0 5 10 10 10 10 10 10 5 -5 0 0 0 0 0 0 -5 -5 0 0 0 0 0 0 -5 -5 0 0 0 0 0 0 -5 -5 0 0 0 0 0 0 -5 -5 0 0 0 0 0 0 -5 0 0 0 5 5 0 0 0`),
    T(`-20 -10 -10 -5 -5 -10 -10 -20 -10 0 0 0 0 0 0 -10 -10 0 5 5 5 5 0 -10 -5 0 5 5 5 5 0 -5 0 0 5 5 5 5 0 -5 -10 5 5 5 5 5 0 -10 -10 0 5 0 0 0 0 -10 -20 -10 -10 -5 -5 -10 -10 -20`),
    T(`-30 -40 -40 -50 -50 -40 -40 -30 -30 -40 -40 -50 -50 -40 -40 -30 -30 -40 -40 -50 -50 -40 -40 -30 -30 -40 -40 -50 -50 -40 -40 -30 -20 -30 -30 -40 -40 -30 -30 -20 -10 -20 -20 -20 -20 -20 -20 -10 20 20 0 0 0 0 20 20 20 30 10 0 0 10 30 20`)];
  const KEND = T(`-50 -40 -30 -20 -20 -30 -40 -50 -30 -20 -10 0 0 -10 -20 -30 -30 -10 20 30 30 20 -10 -30 -30 -10 30 40 40 30 -10 -30 -30 -10 30 40 40 30 -10 -30 -30 -10 20 30 30 20 -10 -30 -30 -30 0 0 0 0 -30 -30 -50 -30 -30 -30 -30 -30 -30 -50`);
  const on = (r, f) => r >= 0 && r < 8 && f >= 0 && f < 8;
  function start(){
    const b = new Int8Array(64), back = [R, N, B, Q, K, B, N, R];
    for (let f = 0; f < 8; f++){ b[f] = back[f]; b[8 + f] = P; b[48 + f] = P | 8; b[56 + f] = back[f] | 8; }
    return { b, side:0, castle:15, ep:-1, half:0, full:1 };
  }
  function attacked(b, sq, by){
    const r = sq >> 3, f = sq & 7, pr = by ? r + 1 : r - 1;
    if (pr >= 0 && pr < 8) for (const df of [-1, 1]) if (on(pr, f + df) && b[pr * 8 + f + df] === (P | by)) return true;
    for (const [dr, df] of KN) if (on(r + dr, f + df) && b[(r + dr) * 8 + f + df] === (N | by)) return true;
    for (const [dr, df] of KG) if (on(r + dr, f + df) && b[(r + dr) * 8 + f + df] === (K | by)) return true;
    for (const [dirs, a, c] of [[DI, B, Q], [OR, R, Q]]) for (const [dr, df] of dirs){
      let rr = r + dr, ff = f + df;
      while (on(rr, ff)){ const pc = b[rr * 8 + ff]; if (pc){ if (pc === (a | by) || pc === (c | by)) return true; break; } rr += dr; ff += df; }
    }
    return false;
  }
  const kingSq = (b, side) => b.indexOf(K | side);
  const inCheck = s => attacked(s.b, kingSq(s.b, s.side), s.side ^ 8);
  function pseudo(s, capsOnly){
    const b = s.b, me = s.side, them = me ^ 8, out = [];
    const add = (from, to, flag = 0, promo = 0) => out.push({ from, to, flag, promo, cap:flag === EP ? (P | them) : b[to] });
    for (let sq = 0; sq < 64; sq++){
      const pc = b[sq]; if (!pc || (pc & 8) !== me) continue;
      const t = pc & 7, r = sq >> 3, f = sq & 7;
      if (t === P){
        const dir = me ? -1 : 1, r1 = r + dir, last = me ? 0 : 7;
        if (r1 < 0 || r1 > 7) continue;
        const to = r1 * 8 + f;
        if (!b[to]){
          if (r1 === last) add(sq, to, 0, Q);
          else if (!capsOnly){ add(sq, to); const to2 = (r + 2 * dir) * 8 + f; if (r === (me ? 6 : 1) && !b[to2]) add(sq, to2, DBL); }
        }
        for (const df of [-1, 1]){
          if (!on(r1, f + df)) continue; const t2 = r1 * 8 + f + df;
          if (b[t2] && (b[t2] & 8) === them) add(sq, t2, 0, r1 === last ? Q : 0);
          else if (t2 === s.ep) add(sq, t2, EP);
        }
      } else if (t === N || t === K){
        for (const [dr, df] of t === N ? KN : KG){
          if (!on(r + dr, f + df)) continue; const to = (r + dr) * 8 + f + df, c = b[to];
          if (!c){ if (!capsOnly) add(sq, to); } else if ((c & 8) === them) add(sq, to);
        }
        if (t === K && !capsOnly){
          const base = me ? 56 : 0, ks = me ? 4 : 1, qs = me ? 8 : 2;
          if (sq === base + 4 && !attacked(b, sq, them)){
            if (s.castle & ks && !b[base + 5] && !b[base + 6] && b[base + 7] === (R | me) && !attacked(b, base + 5, them) && !attacked(b, base + 6, them)) add(sq, base + 6, CASTLE);
            if (s.castle & qs && !b[base + 3] && !b[base + 2] && !b[base + 1] && b[base] === (R | me) && !attacked(b, base + 3, them) && !attacked(b, base + 2, them)) add(sq, base + 2, CASTLE);
          }
        }
      } else {
        for (const [dr, df] of t === B ? DI : t === R ? OR : KG){
          let rr = r + dr, ff = f + df;
          while (on(rr, ff)){
            const to = rr * 8 + ff, c = b[to];
            if (!c){ if (!capsOnly) add(sq, to); } else { if ((c & 8) === them) add(sq, to); break; }
            rr += dr; ff += df;
          }
        }
      }
    }
    return out;
  }
  function make(s, m){
    const b = s.b.slice(), pc = b[m.from], t = pc & 7, me = s.side;
    b[m.to] = m.promo ? (m.promo | me) : pc; b[m.from] = 0;
    if (m.flag === EP) b[m.to + (me ? 8 : -8)] = 0;
    if (m.flag === CASTLE){ if (m.to > m.from){ b[m.from + 1] = b[m.from + 3]; b[m.from + 3] = 0; } else { b[m.from - 1] = b[m.from - 4]; b[m.from - 4] = 0; } }
    let c = s.castle; if (t === K) c &= me ? ~12 : ~3;
    for (const sq of [m.from, m.to]){ if (sq === 0) c &= ~2; if (sq === 7) c &= ~1; if (sq === 56) c &= ~8; if (sq === 63) c &= ~4; }
    return { b, side:me ^ 8, castle:c, ep:m.flag === DBL ? (m.from + m.to) >> 1 : -1, half:(t === P || m.cap) ? 0 : s.half + 1, full:s.full + (me ? 1 : 0) };
  }
  const legalAfter = (s, m) => { const n = make(s, m); return attacked(n.b, kingSq(n.b, s.side), n.side) ? null : n; };
  const legal = s => pseudo(s).filter(m => legalAfter(s, m));
  function evaluate(s){
    const b = s.b; let np = 0, sc = 0;
    for (let i = 0; i < 64; i++){ const t = b[i] & 7; if (t && t !== P && t !== K) np += VAL[t]; }
    const end = np <= 2600;
    for (let i = 0; i < 64; i++){
      const pc = b[i]; if (!pc) continue; const t = pc & 7, white = !(pc & 8);
      const idx = white ? (7 - (i >> 3)) * 8 + (i & 7) : i;
      const v = VAL[t] + (t === K && end ? KEND[idx] : PST[t][idx]);
      sc += white ? v : -v;
    }
    return s.side ? -sc : sc;
  }
  const order = ms => ms.sort((a, b) => ((b.cap ? VAL[b.cap & 7] * 10 : 0) + (b.promo ? 800 : 0)) - ((a.cap ? VAL[a.cap & 7] * 10 : 0) + (a.promo ? 800 : 0)));
  let nodes = 0;
  function qs(s, a, b, d){
    nodes++; const stand = evaluate(s); if (stand >= b) return b; if (stand > a) a = stand; if (d <= 0) return a;
    for (const m of order(pseudo(s, true))){ const n = legalAfter(s, m); if (!n) continue; const v = -qs(n, -b, -a, d - 1); if (v >= b) return b; if (v > a) a = v; }
    return a;
  }
  function nm(s, depth, a, b, ply){
    if (s.half >= 100) return 0;
    if (depth <= 0) return qs(s, a, b, 4);
    nodes++; let any = false;
    for (const m of order(pseudo(s))){
      const n = legalAfter(s, m); if (!n) continue; any = true;
      const v = -nm(n, depth - 1, -b, -a, ply + 1); if (v >= b) return b; if (v > a) a = v;
    }
    if (!any) return inCheck(s) ? -100000 + ply : 0;
    return a;
  }
  function best(s, depth = 3){
    nodes = 0; let bestM = null, bestV = -Infinity;
    const ms = order(legal(s));
    for (const m of ms){
      const v = -nm(make(s, m), depth - 1, -Infinity, -bestV + 12, 1) + Math.random() * 12;
      if (v > bestV){ bestV = v; bestM = m; }
    }
    return bestM;
  }
  const sqName = sq => 'abcdefgh'[sq & 7] + ((sq >> 3) + 1);
  const uci = m => sqName(m.from) + sqName(m.to) + (m.promo ? 'q' : '');
  function san(s, m){
    const t = s.b[m.from] & 7, n = make(s, m);
    let out;
    if (m.flag === CASTLE) out = m.to > m.from ? 'O-O' : 'O-O-O';
    else {
      const cap = m.cap ? 'x' : '';
      if (t === P) out = (cap ? 'abcdefgh'[m.from & 7] : '') + cap + sqName(m.to) + (m.promo ? '=Q' : '');
      else {
        const twins = legal(s).filter(o => o.to === m.to && o.from !== m.from && (s.b[o.from] & 7) === t);
        let dis = ''; if (twins.length) dis = twins.some(o => (o.from & 7) === (m.from & 7)) ? String((m.from >> 3) + 1) : 'abcdefgh'[m.from & 7];
        out = ' PNBRQK'[t] + dis + cap + sqName(m.to);
      }
    }
    if (inCheck(n)) out += legal(n).length ? '+' : '#';
    return out;
  }
  function fen(s){
    let o = '';
    for (let r = 7; r >= 0; r--){
      let run = 0;
      for (let f = 0; f < 8; f++){ const pc = s.b[r * 8 + f]; if (!pc){ run++; continue; } if (run){ o += run; run = 0; } const ch = ' pnbrqk'[pc & 7]; o += pc & 8 ? ch : ch.toUpperCase(); }
      if (run) o += run; if (r) o += '/';
    }
    const c = (s.castle & 1 ? 'K' : '') + (s.castle & 2 ? 'Q' : '') + (s.castle & 4 ? 'k' : '') + (s.castle & 8 ? 'q' : '');
    return `${o} ${s.side ? 'b' : 'w'} ${c || '-'} ${s.ep >= 0 ? sqName(s.ep) : '-'} ${s.half} ${s.full}`;
  }
  function status(s){
    if (!legal(s).length) return inCheck(s) ? 'mate' : 'stalemate';
    if (s.half >= 100) return 'fifty';
    const rest = [...s.b].filter(pc => pc && (pc & 7) !== K);
    if (!rest.length || (rest.length === 1 && [N, B].includes(rest[0] & 7))) return 'material';
    return null;
  }
  return { start, legal, make, best, san, uci, fen, sqName, status, inCheck, VAL, P, N, B, R, Q, K, EP, CASTLE, get nodes(){ return nodes; } };
})();
