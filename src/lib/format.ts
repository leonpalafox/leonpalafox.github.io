const KANJI_DIGITS = ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九'];

/** 2026 → 二〇二六年, matching the vertical date treatment in the identity mockup. */
export function kanjiYear(date: Date): string {
  return (
    String(date.getFullYear())
      .split('')
      .map((d) => KANJI_DIGITS[Number(d)])
      .join('') + '年'
  );
}

export function isoDate(date: Date): string {
  return date.toISOString().slice(0, 10);
}

/** 2026-05-13 → 05.13 */
export function monthDay(date: Date): string {
  const iso = isoDate(date);
  return `${iso.slice(5, 7)}.${iso.slice(8, 10)}`;
}

export function fullDate(date: Date, lang: 'es' | 'en' = 'en'): string {
  return date.toLocaleDateString(lang === 'es' ? 'es-MX' : 'en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC',
  });
}
