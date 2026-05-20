import type { ScamPattern } from "../types";

const VALID_CATEGORIES: ScamPattern["category"][] = [
  "delivery",
  "government",
  "financial",
  "romance",
  "employment",
  "tech-support",
  "other",
];

function isScamPattern(value: unknown): value is ScamPattern {
  if (!value || typeof value !== "object") return false;
  const v = value as Record<string, unknown>;
  return (
    typeof v.id === "string" &&
    typeof v.name === "string" &&
    typeof v.description === "string" &&
    typeof v.example === "string" &&
    Array.isArray(v.red_flags) &&
    v.red_flags.every((f) => typeof f === "string") &&
    typeof v.category === "string" &&
    (VALID_CATEGORIES as string[]).includes(v.category)
  );
}

export async function loadPatterns(): Promise<ScamPattern[]> {
  const modules = import.meta.glob("../scam-patterns/*.json", {
    eager: true,
    import: "default",
  }) as Record<string, unknown>;

  const patterns: ScamPattern[] = [];
  for (const [path, mod] of Object.entries(modules)) {
    if (path.endsWith("/index.json")) continue;
    if (isScamPattern(mod)) {
      patterns.push(mod);
    } else if (import.meta.env.DEV) {
      console.warn(`[scam-shield] Skipping invalid pattern file: ${path}`);
    }
  }
  patterns.sort((a, b) => a.id.localeCompare(b.id));
  return patterns;
}
