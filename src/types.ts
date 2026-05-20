export type Verdict = "safe" | "suspicious" | "scam";

export interface ScanResult {
  verdict: Verdict;
  confidence: number;
  headline: string;
  red_flags: string[];
  what_to_do: string;
  if_already_clicked?: string;
}

export interface ScanHistoryItem {
  id: string;
  timestamp: number;
  input_preview: string;
  result: ScanResult;
}

export interface ScamPattern {
  id: string;
  name: string;
  description: string;
  example: string;
  red_flags: string[];
  category:
    | "delivery"
    | "government"
    | "financial"
    | "romance"
    | "employment"
    | "tech-support"
    | "other";
}
