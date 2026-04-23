import { describe, it, expect } from 'vitest';

// ─── isTs ────────────────────────────────────────────────────────────────────
describe('isTs', () => {
  it('detects "timestamp" column', () => expect(isTs('timestamp')).toBe(true));
  it('detects "Timestamp" (case-insensitive)', () => expect(isTs('Timestamp')).toBe(true));
  it('detects "time" column', () => expect(isTs('time')).toBe(true));
  it('detects "date" column', () => expect(isTs('date')).toBe(true));
  it('rejects unrelated column', () => expect(isTs('value')).toBe(false));
  it('rejects "datetime" (not exact match for time/date)', () => expect(isTs('datetime')).toBe(false));
  it('accepts column containing "timestamp" substring', () => expect(isTs('event_timestamp')).toBe(true));
});

// ─── isEpochMs ───────────────────────────────────────────────────────────────
describe('isEpochMs', () => {
  it('accepts valid epoch ms (2024)', () => expect(isEpochMs(1700000000000)).toBe(true));
  it('accepts epoch ms as string', () => expect(isEpochMs('1700000000000')).toBe(true));
  it('rejects value too small (< 9e11)', () => expect(isEpochMs(1000)).toBe(false));
  it('rejects value too large (> 5e12)', () => expect(isEpochMs(6e12)).toBe(false));
  it('rejects NaN string', () => expect(isEpochMs('not-a-number')).toBe(false));
  it('rejects null', () => expect(isEpochMs(null)).toBe(false));
  it('rejects negative number', () => expect(isEpochMs(-1700000000000)).toBe(false));
});

// ─── parseTs ─────────────────────────────────────────────────────────────────
describe('parseTs', () => {
  it('parses epoch ms number', () => {
    expect(parseTs(1700000000000)).toBe(1700000000000);
  });
  it('parses epoch ms as string', () => {
    expect(parseTs('1700000000000')).toBe(1700000000000);
  });
  it('parses ISO 8601 string', () => {
    const result = parseTs('2024-01-15T10:30:00.000Z');
    expect(typeof result).toBe('number');
    expect(result).toBeGreaterThan(9e11);
  });
  it('parses PT/Kibana format DD/MM/YYYY, HH:MM', () => {
    const result = parseTs('15/01/2024, 10:30');
    expect(typeof result).toBe('number');
    expect(result).toBeGreaterThan(9e11);
  });
  it('parses PT format with space separator DD/MM/YYYY HH:MM', () => {
    const result = parseTs('15/01/2024 10:30');
    expect(typeof result).toBe('number');
    expect(result).toBeGreaterThan(9e11);
  });
  it('returns NaN for null', () => expect(parseTs(null)).toBeNaN());
  it('returns NaN for empty string', () => expect(parseTs('')).toBeNaN());
  it('returns NaN for invalid string', () => expect(parseTs('not-a-date')).toBeNaN());
});

// ─── getTsCol ────────────────────────────────────────────────────────────────
describe('getTsCol', () => {
  it('finds column by exact name "timestamp"', () => {
    const f = { headers: ['timestamp', 'value'], rows: [], _tsColCache: undefined };
    expect(getTsCol(f)).toBe('timestamp');
  });
  it('finds column by name "time"', () => {
    const f = { headers: ['time', 'metric'], rows: [], _tsColCache: undefined };
    expect(getTsCol(f)).toBe('time');
  });
  it('finds column by content when ≥70% are epoch ms', () => {
    const f = {
      headers: ['ts', 'value'],
      rows: [
        { ts: '1700000000000', value: '1' },
        { ts: '1700000001000', value: '2' },
        { ts: '1700000002000', value: '3' },
        { ts: 'invalid', value: '4' },
      ],
      _tsColCache: undefined
    };
    expect(getTsCol(f)).toBe('ts');
  });
  it('returns null when no timestamp column found', () => {
    const f = { headers: ['metric', 'value'], rows: [{ metric: '1', value: '2' }], _tsColCache: undefined };
    expect(getTsCol(f)).toBeNull();
  });
  it('uses cache on second call', () => {
    const f = { headers: ['timestamp', 'value'], rows: [], _tsColCache: 'cached-col' };
    expect(getTsCol(f)).toBe('cached-col');
  });
  it('does not match content column when <70% are epoch ms', () => {
    const f = {
      headers: ['ts', 'value'],
      rows: [
        { ts: '1700000000000', value: '1' },
        { ts: 'text', value: '2' },
        { ts: 'text2', value: '3' },
      ],
      _tsColCache: undefined
    };
    expect(getTsCol(f)).toBeNull();
  });
});

// ─── esc ─────────────────────────────────────────────────────────────────────
describe('esc', () => {
  it('escapes ampersand', () => expect(esc('a & b')).toBe('a &amp; b'));
  it('escapes less-than', () => expect(esc('<script>')).toBe('&lt;script&gt;'));
  it('escapes double quote', () => expect(esc('"hello"')).toBe('&quot;hello&quot;'));
  it('returns empty string for null', () => expect(esc(null)).toBe(''));
  it('returns empty string for undefined', () => expect(esc(undefined)).toBe(''));
  it('converts number to escaped string', () => expect(esc(42)).toBe('42'));
  it('does not double-escape', () => expect(esc('&amp;')).toBe('&amp;amp;'));
});

// ─── computeDelta ────────────────────────────────────────────────────────────
describe('computeDelta', () => {
  it('calculates positive delta (a1 worse)', () => {
    expect(computeDelta(110, 100)).toBeCloseTo(10);
  });
  it('calculates negative delta (a1 better)', () => {
    expect(computeDelta(90, 100)).toBeCloseTo(-10);
  });
  it('returns 0 when both are 0', () => {
    expect(computeDelta(0, 0)).toBe(0);
  });
  it('returns 999999 when baseline is 0 and a1 > 0', () => {
    expect(computeDelta(5, 0)).toBe(999999);
  });
  it('returns -999999 when baseline is 0 and a1 < 0', () => {
    expect(computeDelta(-5, 0)).toBe(-999999);
  });
  it('returns null when both are null', () => {
    expect(computeDelta(null, null)).toBeNull();
  });
  it('returns null when a1 is null', () => {
    expect(computeDelta(null, 100)).toBeNull();
  });
  it('returns null when a2 is null', () => {
    expect(computeDelta(100, null)).toBeNull();
  });
  it('uses absolute value of baseline for denominator', () => {
    // a2 = -100, a1 = -90: delta = (-90 - -100) / |-100| * 100 = 10
    expect(computeDelta(-90, -100)).toBeCloseTo(10);
  });
});
