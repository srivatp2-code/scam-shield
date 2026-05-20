import type { ScanHistoryItem } from "../types";

const KEY_API = "scamshield:apiKey";
const KEY_HISTORY = "scamshield:history";
const HISTORY_LIMIT = 20;

function safeGet(key: string): string | null {
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

function safeSet(key: string, value: string): void {
  try {
    window.localStorage.setItem(key, value);
  } catch {
    // localStorage may be unavailable (private mode, quota exceeded).
    // Silent: the caller will see the next read return stale data.
  }
}

function safeRemove(key: string): void {
  try {
    window.localStorage.removeItem(key);
  } catch {
    // ignore
  }
}

export function getApiKey(): string | null {
  return safeGet(KEY_API);
}

export function setApiKey(key: string): void {
  safeSet(KEY_API, key);
}

export function clearApiKey(): void {
  safeRemove(KEY_API);
}

export function getHistory(): ScanHistoryItem[] {
  const raw = safeGet(KEY_HISTORY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed)) return [];
    return (parsed as ScanHistoryItem[]).slice(0, HISTORY_LIMIT);
  } catch {
    return [];
  }
}

export function addToHistory(item: ScanHistoryItem): void {
  const current = getHistory();
  const next = [item, ...current].slice(0, HISTORY_LIMIT);
  safeSet(KEY_HISTORY, JSON.stringify(next));
}

export function clearHistory(): void {
  safeRemove(KEY_HISTORY);
}
