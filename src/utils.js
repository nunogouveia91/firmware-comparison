// utils.js — Funções puras extraídas de comparador.html
// Carregado via <script src="utils.js"> antes do bloco principal.
// Sem dependências externas. Compatível com browser e Vitest (globals: true).

function isTs(h) {
  const l = h.toLowerCase();
  return l.includes('timestamp') || l === 'time' || l === 'date';
}

function isEpochMs(v) {
  const n = Number(v);
  return !isNaN(n) && n > 9e11 && n < 5e12;
}

// Parse any timestamp value to epoch ms — handles epoch numbers, ISO strings,
// and PT locale format "DD/MM/YYYY, HH:MM" produced by Kibana exports.
function parseTs(v) {
  if (v == null || v === '') return NaN;
  const n = Number(v);
  if (!isNaN(n) && n > 9e11 && n < 5e12) return n;
  // Try native Date parse (works for ISO 8601 and many locale-neutral formats)
  const d = Date.parse(v);
  if (!isNaN(d)) return d;
  // DD/MM/YYYY[, ]HH:MM[:SS] — PT/Kibana locale
  const m = String(v).match(/^(\d{2})\/(\d{2})\/(\d{4})[,\s]+(\d{2}):(\d{2})/);
  if (m) return Date.parse(`${m[3]}-${m[2]}-${m[1]}T${m[4]}:${m[5]}`);
  return NaN;
}

// Returns the timestamp column for a file — by name first, then by content (epoch ms detection).
// Caches the result on the file object to avoid repeated scans.
function getTsCol(f) {
  if (f._tsColCache !== undefined) return f._tsColCache;
  const byName = f.headers.find(h => isTs(h));
  if (byName) { f._tsColCache = byName; return byName; }
  // Content fallback: column where ≥70% of non-null values are epoch ms
  for (const h of f.headers) {
    const vals = f.rows.map(r => r[h]).filter(v => v != null && v !== '');
    if (vals.length === 0) continue;
    const epochCount = vals.filter(v => isEpochMs(v)).length;
    if (epochCount / vals.length >= 0.7) { f._tsColCache = h; return h; }
  }
  f._tsColCache = null;
  return null;
}

function esc(s) {
  if (s === null || s === undefined) return '';
  return String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// Delta percentual entre dois valores.
// Positivo = a1 pior que a2 (FW-B pior que FW-A).
// Devolve sentinel 999999/-999999 quando baseline (a2) é 0.
function computeDelta(a1, a2) {
  if (a1 === null && a2 === null) return null;
  if (a1 === null) return null;
  if (a2 === null) return null;
  if (a2 === 0 && a1 === 0) return 0;
  if (a2 === 0) return a1 > 0 ? 999999 : -999999;
  return ((a1 - a2) / Math.abs(a2)) * 100;
}

// Expõe as funções como globais em ambientes não-browser (ex: Vitest/Node).
// Em browser, <script src> já coloca top-level functions no scope global (window).
if (typeof window === 'undefined') {
  Object.assign(globalThis, { isTs, isEpochMs, parseTs, getTsCol, esc, computeDelta });
}
