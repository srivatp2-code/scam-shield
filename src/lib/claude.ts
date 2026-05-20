import Anthropic from "@anthropic-ai/sdk";
import type { ContentBlockParam } from "@anthropic-ai/sdk/resources/messages";
import type { ScanResult, ScamPattern, Verdict } from "../types";
import { buildSystemPrompt } from "./prompt";

const MODEL_VISION = "claude-sonnet-4-5";
const MODEL_TEXT = "claude-haiku-4-5";
const MAX_TOKENS = 1024;

const VALID_VERDICTS: Verdict[] = ["safe", "suspicious", "scam"];
const VALID_IMAGE_TYPES = [
  "image/jpeg",
  "image/png",
  "image/gif",
  "image/webp",
] as const;
type ImageMediaType = (typeof VALID_IMAGE_TYPES)[number];

export interface ScanInput {
  text?: string;
  imageBase64?: string;
  imageMediaType?: string;
}

export class ScanError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ScanError";
  }
}

function stripFences(s: string): string {
  const trimmed = s.trim();
  const match = trimmed.match(/^```(?:json)?\s*([\s\S]*?)\s*```$/);
  return match ? match[1].trim() : trimmed;
}

function isScanResult(value: unknown): value is ScanResult {
  if (!value || typeof value !== "object") return false;
  const v = value as Record<string, unknown>;
  if (!VALID_VERDICTS.includes(v.verdict as Verdict)) return false;
  if (
    typeof v.confidence !== "number" ||
    !Number.isFinite(v.confidence) ||
    v.confidence < 1 ||
    v.confidence > 10
  )
    return false;
  if (typeof v.headline !== "string" || v.headline.length === 0) return false;
  if (
    !Array.isArray(v.red_flags) ||
    !v.red_flags.every((f) => typeof f === "string")
  )
    return false;
  if (typeof v.what_to_do !== "string" || v.what_to_do.length === 0)
    return false;
  if (
    v.if_already_clicked !== undefined &&
    typeof v.if_already_clicked !== "string"
  )
    return false;
  return true;
}

function buildUserContent(input: ScanInput): ContentBlockParam[] {
  if (input.imageBase64 && input.imageMediaType) {
    if (
      !(VALID_IMAGE_TYPES as readonly string[]).includes(input.imageMediaType)
    ) {
      throw new ScanError(
        "That image type isn't supported. Try a JPEG, PNG, GIF, or WebP screenshot.",
      );
    }
    return [
      {
        type: "image",
        source: {
          type: "base64",
          media_type: input.imageMediaType as ImageMediaType,
          data: input.imageBase64,
        },
      },
      { type: "text", text: "Analyze this message screenshot." },
    ];
  }
  return [{ type: "text", text: input.text ?? "" }];
}

function formatApiError(err: unknown): string {
  const status = (err as { status?: number } | null)?.status;
  if (status === 401)
    return "Your API key looks invalid. Double-check it in Settings.";
  if (status === 429)
    return "You're sending requests too fast. Wait a moment and try again.";
  if (status === 529)
    return "Anthropic's servers are busy. Try again in a few seconds.";

  if (err instanceof Anthropic.APIConnectionError) {
    return "Couldn't reach Anthropic. Check your internet connection.";
  }

  if (typeof status === "number") {
    return `Anthropic returned an error (${status}). Try again, or open an issue if it keeps happening.`;
  }
  return "Something went wrong. Try again, or open an issue if it keeps happening.";
}

export async function scanMessage(
  input: ScanInput,
  apiKey: string,
  patterns: ScamPattern[],
): Promise<ScanResult> {
  const hasText = Boolean(input.text && input.text.trim().length > 0);
  const hasImage = Boolean(input.imageBase64 && input.imageMediaType);
  if (!hasText && !hasImage) {
    throw new ScanError("Please paste a message or upload a screenshot first.");
  }

  const client = new Anthropic({ apiKey, dangerouslyAllowBrowser: true });
  const model = hasImage ? MODEL_VISION : MODEL_TEXT;
  const userContent = buildUserContent(input);

  let response: Anthropic.Messages.Message;
  try {
    response = await client.messages.create({
      model,
      max_tokens: MAX_TOKENS,
      system: buildSystemPrompt(patterns),
      messages: [{ role: "user", content: userContent }],
    });
  } catch (err) {
    throw new ScanError(formatApiError(err));
  }

  const textBlock = response.content.find((b) => b.type === "text");
  if (!textBlock || textBlock.type !== "text") {
    throw new ScanError(
      "Got an unexpected response. Try again — if it keeps happening, open an issue.",
    );
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(stripFences(textBlock.text));
  } catch {
    throw new ScanError(
      "Got an unexpected response. Try again — if it keeps happening, open an issue.",
    );
  }

  if (!isScanResult(parsed)) {
    throw new ScanError(
      "Got an unexpected response. Try again — if it keeps happening, open an issue.",
    );
  }

  return parsed;
}
