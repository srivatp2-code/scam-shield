"""Generate the Scam Shield technical design PDF.

Run from anywhere:
    python3 docs/build_tech_design_pdf.py

Output: docs/TECH_DESIGN.pdf
"""

from __future__ import annotations

import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

OUT_PATH = Path(__file__).resolve().parent / "TECH_DESIGN.pdf"

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

base = getSampleStyleSheet()

INK = colors.HexColor("#111827")
MUTED = colors.HexColor("#6B7280")
BORDER = colors.HexColor("#E5E7EB")
CODE_BG = colors.HexColor("#F3F4F6")
RED = colors.HexColor("#B91C1C")
YELLOW = colors.HexColor("#B45309")
GREEN = colors.HexColor("#15803D")

TITLE = ParagraphStyle(
    "Title",
    parent=base["Title"],
    fontName="Helvetica-Bold",
    fontSize=28,
    leading=34,
    textColor=INK,
    spaceAfter=8,
    alignment=TA_LEFT,
)

SUBTITLE = ParagraphStyle(
    "Subtitle",
    parent=base["Normal"],
    fontName="Helvetica",
    fontSize=14,
    leading=20,
    textColor=MUTED,
    spaceAfter=18,
)

H1 = ParagraphStyle(
    "H1",
    parent=base["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=20,
    leading=26,
    textColor=INK,
    spaceBefore=24,
    spaceAfter=10,
)

H2 = ParagraphStyle(
    "H2",
    parent=base["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=14,
    leading=20,
    textColor=INK,
    spaceBefore=14,
    spaceAfter=6,
)

H3 = ParagraphStyle(
    "H3",
    parent=base["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=16,
    textColor=INK,
    spaceBefore=8,
    spaceAfter=4,
)

BODY = ParagraphStyle(
    "Body",
    parent=base["BodyText"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=15,
    textColor=INK,
    spaceAfter=8,
)

BULLET = ParagraphStyle(
    "Bullet",
    parent=BODY,
    leftIndent=14,
    bulletIndent=2,
    spaceAfter=3,
)

CALLOUT = ParagraphStyle(
    "Callout",
    parent=BODY,
    fontSize=10,
    textColor=INK,
    leftIndent=10,
    rightIndent=10,
    borderColor=BORDER,
    borderWidth=0,
    backColor=colors.HexColor("#FEF3C7"),
    spaceBefore=6,
    spaceAfter=10,
)

CODE = ParagraphStyle(
    "Code",
    parent=base["Code"],
    fontName="Courier",
    fontSize=8.5,
    leading=11,
    textColor=INK,
    backColor=CODE_BG,
    borderPadding=8,
    leftIndent=0,
    rightIndent=0,
    spaceBefore=4,
    spaceAfter=10,
)

CAPTION = ParagraphStyle(
    "Caption",
    parent=BODY,
    fontSize=9,
    textColor=MUTED,
    spaceAfter=12,
    alignment=TA_CENTER,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def p(text: str, style: ParagraphStyle = BODY) -> Paragraph:
    return Paragraph(text, style)


def code(text: str) -> Preformatted:
    return Preformatted(text, CODE)


def bullets(items: list[str], style: ParagraphStyle = BULLET) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(t, style), leftIndent=14) for t in items],
        bulletType="bullet",
        start="•",
        leftIndent=18,
        bulletFontName="Helvetica",
        bulletFontSize=9,
    )


def kv_table(rows: list[tuple[str, str]], col_widths=(1.6 * inch, 4.6 * inch)) -> Table:
    data = [[Paragraph(f"<b>{k}</b>", BODY), Paragraph(v, BODY)] for k, v in rows]
    t = Table(data, colWidths=list(col_widths))
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, BORDER),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return t


def section_header(title: str, anchor: str) -> Paragraph:
    return Paragraph(f'<a name="{anchor}"/>{title}', H1)


# ---------------------------------------------------------------------------
# Page template with header / footer
# ---------------------------------------------------------------------------


def header_footer(canvas, doc):
    canvas.saveState()
    # Header
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.75 * inch, LETTER[1] - 0.55 * inch, "Scam Shield · Technical Design")
    canvas.drawRightString(
        LETTER[0] - 0.75 * inch,
        LETTER[1] - 0.55 * inch,
        f"v0.1.0",
    )
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.4)
    canvas.line(
        0.75 * inch,
        LETTER[1] - 0.65 * inch,
        LETTER[0] - 0.75 * inch,
        LETTER[1] - 0.65 * inch,
    )
    # Footer
    canvas.setFillColor(MUTED)
    canvas.drawString(0.75 * inch, 0.5 * inch, "github.com/srivatp2-code/scam-shield")
    canvas.drawRightString(LETTER[0] - 0.75 * inch, 0.5 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_doc(path: Path) -> BaseDocTemplate:
    doc = BaseDocTemplate(
        str(path),
        pagesize=LETTER,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.9 * inch,
        bottomMargin=0.85 * inch,
        title="Scam Shield — Technical Design",
        author="Sri Pusarla",
        subject="Scam Shield MVP technical design document",
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="normal",
    )
    doc.addPageTemplates(
        [PageTemplate(id="main", frames=frame, onPage=header_footer)]
    )
    return doc


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------


def build_story() -> list:
    s: list = []

    # ---- Title page ----
    s.append(Spacer(1, 0.5 * inch))
    s.append(p("Scam Shield", TITLE))
    s.append(p("Technical Design &amp; Architecture", SUBTITLE))
    s.append(p(
        "A free, open-source web app that helps non-technical users — think parents and grandparents — "
        "decide whether a suspicious email or text is a scam. This document is the engineering blueprint: "
        "what the system does, why it's built the way it is, and how to extend it without breaking the privacy contract.",
        BODY,
    ))
    s.append(Spacer(1, 0.3 * inch))
    s.append(kv_table([
        ("Version", "v0.1.0 (MVP)"),
        ("Status", "Released"),
        ("Repository", "github.com/srivatp2-code/scam-shield"),
        ("License", "MIT"),
        ("Author", "Sri Pusarla"),
        ("Bundle size", "≈118 KB gzipped / ≈400 KB raw"),
    ]))

    s.append(PageBreak())

    # ---- Table of contents (static) ----
    s.append(p("Contents", H1))
    toc_items = [
        "1. Executive Summary",
        "2. Goals and Non-Goals",
        "3. System Architecture",
        "4. Technology Stack",
        "5. Data Model",
        "6. Component Design",
        "7. Scam Classification Logic",
        "8. Privacy &amp; Security Architecture",
        "9. UI State Machine &amp; Accessibility",
        "10. Error Handling and Resilience",
        "11. Build, Bundle, and Deployment",
        "12. Extensibility",
        "13. Limitations and Future Work",
        "Appendix A — Full System Prompt",
        "Appendix B — ScanResult JSON Schema",
        "Appendix C — Project File Tree",
    ]
    s.append(bullets(toc_items))
    s.append(PageBreak())

    # ---- 1. Executive Summary ----
    s.append(section_header("1. Executive Summary", "exec"))
    s.append(p(
        "Scam Shield is a single-page web application that classifies arbitrary text or screenshots as "
        "<b>safe</b>, <b>suspicious</b>, or <b>scam</b>, and returns a grandparent-readable explanation. "
        "There is no backend: the user supplies their own Anthropic API key (BYOK), and the browser "
        "calls <font face='Courier'>api.anthropic.com</font> directly using the official SDK with "
        "<font face='Courier'>dangerouslyAllowBrowser: true</font>. Verdicts are produced by a single "
        "structured-JSON call to Claude, primed with a system prompt that injects a community-curated "
        "library of known scam patterns.",
    ))
    s.append(p(
        "Three properties define the design and constrain every decision:",
        BODY,
    ))
    s.append(bullets([
        "<b>Privacy is structural.</b> Because there is no backend, no scan data can leak from a server we control — there isn't one.",
        "<b>Accessibility is non-negotiable.</b> 18 px base font, 44 px tap targets, 375 px mobile-first layout, plain-English copy aimed at someone in their 70s.",
        "<b>Extensibility is community-driven.</b> Adding a new scam pattern is a single JSON file plus a PR; the loader picks it up at build time via Vite's <font face='Courier'>import.meta.glob</font>.",
    ]))

    # ---- 2. Goals ----
    s.append(section_header("2. Goals and Non-Goals", "goals"))
    s.append(p("Goals", H2))
    s.append(bullets([
        "Produce a single, unambiguous verdict (🟢 / 🟡 / 🔴) per message, with concrete red-flag citations.",
        "Work for text messages, emails, and image screenshots — same interface, one button.",
        "Be usable one-handed on a 375 px-wide phone with no horizontal scrolling.",
        "Ship as a static site that any CDN can host. Build command is <font face='Courier'>npm run build</font>; output is <font face='Courier'>dist/</font>.",
        "Allow the scam pattern library to grow through community pull requests without modifying app code.",
    ]))
    s.append(p("Non-goals", H2))
    s.append(bullets([
        "Not a replacement for security advice. The disclaimer is explicit in the README and UI.",
        "Not a server-side service. No backend, no database, no per-user accounts.",
        "Not an analytics product. Zero telemetry, zero third-party scripts.",
        "Not multi-tenant. Each browser is its own world; the API key and history are device-local.",
        "Not multilingual in v0.1.0 — English-only copy and prompt.",
    ]))

    # ---- 3. Architecture ----
    s.append(section_header("3. System Architecture", "arch"))
    s.append(p(
        "Scam Shield is a static React SPA. There are only three actors at runtime: the user's browser, "
        "the user's localStorage, and Anthropic's API. Every other component in the diagram below is "
        "source code that compiles into the browser bundle.",
        BODY,
    ))

    arch_diagram = (
        "┌─────────────────────────────────────────────────────────────────────────┐\n"
        "│                            User device (browser)                        │\n"
        "│                                                                         │\n"
        "│   ┌────────────┐   text/image    ┌──────────────────────────────────┐   │\n"
        "│   │  ScanInput │ ───────────────▶│             App.tsx              │   │\n"
        "│   └────────────┘                  │     (View state machine)         │   │\n"
        "│         ▲                         └──────┬─────────────────┬─────────┘   │\n"
        "│         │ verdict /                      │                 │             │\n"
        "│         │ error                          ▼                 ▼             │\n"
        "│   ┌────────────┐                ┌─────────────────┐  ┌──────────────┐   │\n"
        "│   │ ResultCard │                │  lib/claude.ts  │  │ lib/storage  │   │\n"
        "│   │  History   │                │  scanMessage()  │  │  (API key,   │   │\n"
        "│   └────────────┘                └────────┬────────┘  │   history)   │   │\n"
        "│                                          │            └─────┬────────┘   │\n"
        "│                                          │                  │            │\n"
        "│                                          ▼                  ▼            │\n"
        "│   ┌──────────────────────────┐    ┌─────────────────────────────────┐   │\n"
        "│   │  scam-patterns/*.json    │    │      window.localStorage        │   │\n"
        "│   │  → lib/patterns.ts       │    │  scamshield:apiKey              │   │\n"
        "│   │  → lib/prompt.ts         │    │  scamshield:history (last 20)   │   │\n"
        "│   │  injected as system msg  │    └─────────────────────────────────┘   │\n"
        "│   └──────────────────────────┘                                          │\n"
        "│                                          │                              │\n"
        "└──────────────────────────────────────────┼──────────────────────────────┘\n"
        "                                           │ HTTPS (user's own key)\n"
        "                                           ▼\n"
        "                          ┌──────────────────────────────┐\n"
        "                          │     api.anthropic.com        │\n"
        "                          │   /v1/messages (Claude)      │\n"
        "                          └──────────────────────────────┘"
    )
    s.append(code(arch_diagram))
    s.append(p("Figure 1. Runtime data flow. The dashed boundary is the device.", CAPTION))

    s.append(p("Layered view", H2))
    s.append(p(
        "The codebase is organized in three layers, with strict one-way dependencies:",
        BODY,
    ))
    s.append(bullets([
        "<b>UI layer</b> (<font face='Courier'>src/components/*</font> and <font face='Courier'>App.tsx</font>) — purely presentational. Owns the View state machine, handles input events, and renders results.",
        "<b>Lib layer</b> (<font face='Courier'>src/lib/*</font>) — business logic: API client, storage wrapper, prompt builder, pattern loader. No React imports.",
        "<b>Data layer</b> — TypeScript types in <font face='Courier'>src/types.ts</font> and JSON in <font face='Courier'>src/scam-patterns/</font>. No code.",
    ]))
    s.append(p(
        "UI imports lib; lib imports types and patterns; nothing imports UI. This means the entire scanning "
        "and storage system can be unit-tested without rendering React.",
        BODY,
    ))

    # ---- 4. Tech stack ----
    s.append(section_header("4. Technology Stack", "stack"))
    s.append(kv_table([
        ("Build", "Vite 5 (rolldown) — dev server with HMR, production build to <font face='Courier'>dist/</font>."),
        ("UI", "React 18 + TypeScript (strict mode)."),
        ("Styling", "Tailwind CSS v3 — no UI library, no CSS-in-JS, single utility class system."),
        ("Icons", "lucide-react (tree-shakeable SVG components)."),
        ("AI SDK", "@anthropic-ai/sdk 0.97.1 with <font face='Courier'>dangerouslyAllowBrowser: true</font>."),
        ("State", "React hooks only. No Redux, Zustand, etc. The app is too small."),
        ("Routing", "None. Conditional render on a single View union."),
        ("Tests", "Build-time TypeScript strict mode; manual smoke test via verification checklist."),
        ("Package mgr", "npm (Node 18+)."),
    ]))
    s.append(p("Rationale for the absence of common things", H2))
    s.append(bullets([
        "<b>No state management library.</b> The app has ~7 pieces of state; useState handles it.",
        "<b>No router.</b> One screen at a time, modeled as a View union; URL hash routing would add bytes for no value.",
        "<b>No CSS framework beyond Tailwind.</b> A component library would add 100 KB+ and impose its own accessibility opinions; we want explicit control over font sizes and tap targets.",
        "<b>No tests in v0.1.0.</b> Time-bound MVP. Phase 6 verification was manual via Claude Preview's MCP at 375 px. Adding Playwright is high-value future work.",
        "<b>No backend.</b> This is the load-bearing privacy claim; adding one defeats the architecture.",
    ]))

    # ---- 5. Data model ----
    s.append(section_header("5. Data Model", "data"))
    s.append(p(
        "All runtime types live in <font face='Courier'>src/types.ts</font>. The schema is intentionally small.",
        BODY,
    ))

    s.append(p("Verdict", H2))
    s.append(code('type Verdict = "safe" | "suspicious" | "scam";'))

    s.append(p("ScanResult — what Claude returns", H2))
    s.append(code(
        '''interface ScanResult {
  verdict: Verdict;              // "safe" | "suspicious" | "scam"
  confidence: number;            // integer 1..10
  headline: string;              // one sentence, plain English
  red_flags: string[];           // specific phrases quoted from input
  what_to_do: string;            // grandparent-friendly next step
  if_already_clicked?: string;   // recovery — only set when verdict==="scam"
}'''
    ))

    s.append(p("ScanHistoryItem — what gets persisted", H2))
    s.append(code(
        '''interface ScanHistoryItem {
  id: string;                    // crypto.randomUUID(), with fallback
  timestamp: number;             // Date.now()
  input_preview: string;         // first 120 chars of text, or "[image]"
  result: ScanResult;
}'''
    ))

    s.append(p("ScamPattern — community-contributed JSON", H2))
    s.append(code(
        '''interface ScamPattern {
  id: string;                    // kebab-case, matches filename
  name: string;                  // short human label
  description: string;           // 1–2 sentences
  example: string;               // sanitized verbatim message
  red_flags: string[];           // 3–6 observable tells
  category:
    | "delivery" | "government" | "financial" | "romance"
    | "employment" | "tech-support" | "other";
}'''
    ))

    s.append(p(
        "Each scam pattern lives as a standalone JSON file under <font face='Courier'>src/scam-patterns/</font>. "
        "Vite inlines them at build time. The loader runs a runtime shape check so a malformed contribution "
        "is silently skipped (with a dev-mode warning) rather than crashing the app.",
        BODY,
    ))

    # ---- 6. Component design ----
    s.append(section_header("6. Component Design", "components"))

    s.append(p("6.1 Storage layer — src/lib/storage.ts", H2))
    s.append(p(
        "A thin <font face='Courier'>localStorage</font> wrapper with two namespaced keys "
        "(<font face='Courier'>scamshield:apiKey</font>, <font face='Courier'>scamshield:history</font>) "
        "and try/catch around every read and write. Private-browsing failures degrade silently: a user can "
        "still scan in an Incognito window, they just won't accumulate history.",
        BODY,
    ))
    s.append(p(
        "History is capped at 20 entries, newest first. Cap is enforced on write — "
        "<font face='Courier'>addToHistory</font> prepends the new item then slices.",
        BODY,
    ))

    s.append(p("6.2 Pattern loader — src/lib/patterns.ts", H2))
    s.append(p(
        "Uses Vite's <font face='Courier'>import.meta.glob('../scam-patterns/*.json', { eager: true, import: 'default' })</font> "
        "to inline every pattern at build time. Each loaded object is validated against the ScamPattern shape "
        "via an <font face='Courier'>isScamPattern</font> type guard (id/name/description/example are strings, "
        "red_flags is a string array, category is one of the allowed enum values). "
        "<font face='Courier'>index.json</font> is skipped by path — it's a discovery aid, not a pattern.",
        BODY,
    ))

    s.append(p("6.3 Prompt builder — src/lib/prompt.ts", H2))
    s.append(p(
        "Single function: <font face='Courier'>buildSystemPrompt(patterns)</font>. Returns a static template "
        "with <font face='Courier'>{{PATTERNS}}</font> replaced by a formatted dump (name, category, description, "
        "example, indented red-flag bullets). The template itself lists the 12 scam pattern categories Claude "
        "should look for, the decision rules, and the strict JSON output contract. See Appendix A.",
        BODY,
    ))

    s.append(p("6.4 Claude API client — src/lib/claude.ts", H2))
    s.append(p(
        "Single public function: <font face='Courier'>scanMessage(input, apiKey, patterns) → Promise&lt;ScanResult&gt;</font>. "
        "Steps:",
        BODY,
    ))
    s.append(bullets([
        "Reject empty input early with a ScanError.",
        "Construct an Anthropic client with <font face='Courier'>dangerouslyAllowBrowser: true</font>.",
        "Choose model: <font face='Courier'>claude-sonnet-4-5</font> for image input, <font face='Courier'>claude-haiku-4-5</font> for text-only (faster, cheaper).",
        "Build a single user message: either <font face='Courier'>[{type:'text'}]</font> or <font face='Courier'>[{type:'image'}, {type:'text': 'Analyze this message screenshot.'}]</font>.",
        "Set <font face='Courier'>max_tokens: 1024</font> and the patterns-injected system prompt.",
        "Strip optional <font face='Courier'>```json</font> code fences defensively, JSON.parse, then run an <font face='Courier'>isScanResult</font> shape check on the parsed object.",
        "Map any thrown error to a grandparent-friendly ScanError message via <font face='Courier'>formatApiError</font>.",
    ]))

    s.append(p("6.5 UI components — src/components/*", H2))
    s.append(kv_table([
        ("Layout", "Header with Shield wordmark + Settings gear. Centered <font face='Courier'>max-w-xl</font> main slot. Footer with GitHub link and privacy reminder."),
        ("PrivacyNote", "🔒 banner shown on the main screen. Single sentence stating data flow."),
        ("ApiKeySetup", "Three numbered steps (link → password input → save). Reused in both onboarding (initial) and settings (edit/clear) modes. Includes a 'Why do I need a key?' expander explaining BYOK."),
        ("ScanInput", "Textarea + 'Or upload a screenshot' button. One input at a time — typing clears the image, uploading clears the text. Inline error display."),
        ("ResultCard", "Colored verdict header (red/yellow/green), headline, red-flag bullets, highlighted 'What to do' panel, and a red-tinted 'If you already clicked' panel rendered only for scam verdicts."),
        ("HistoryList", "Collapsible last-20. Each entry shows the verdict color dot, the input preview, and a relative timestamp ('1 min ago', 'Yesterday', 'May 12'). Click reopens the ResultCard. Clear-history link at the bottom."),
    ]))

    # ---- 7. Classification ----
    s.append(section_header("7. Scam Classification Logic", "classification"))
    s.append(p(
        "Classification is single-call. We do not chain multiple model invocations, do not use embeddings, "
        "and do not maintain server-side state. Everything depends on the system prompt, the pattern library, "
        "and Claude's reasoning ability over a structured-JSON contract.",
        BODY,
    ))

    s.append(p("7.1 Inputs", H2))
    s.append(bullets([
        "<b>Text mode:</b> raw user-pasted message, trimmed but otherwise untouched. Sent as a single text content block.",
        "<b>Image mode:</b> base64-encoded screenshot with explicit <font face='Courier'>media_type</font> (one of <font face='Courier'>image/jpeg | image/png | image/gif | image/webp</font>), followed by a fixed text prompt &quot;Analyze this message screenshot.&quot;",
    ]))

    s.append(p("7.2 Model selection", H2))
    s.append(kv_table([
        ("Text-only input", "claude-haiku-4-5 — fast, cheap, capable enough for English scam detection."),
        ("Image input", "claude-sonnet-4-5 — vision model with stronger OCR + reasoning over screenshots."),
        ("max_tokens", "1024 — comfortably above typical structured output (~250–400 tokens)."),
        ("Streaming", "Not used. The UI shows 'Reading the message…' until the full JSON arrives, then validates and renders. Streaming partial JSON would complicate the parse/validate flow."),
    ]))

    s.append(p("7.3 Prompt design — five mechanisms", H2))
    s.append(bullets([
        "<b>Audience priming.</b> 'Imagine someone in their 70s' biases word choice toward plain English. Explicit ban on jargon: never say 'phishing,' say 'a fake message pretending to be USPS.'",
        "<b>Scam taxonomy.</b> 12 named patterns: urgency, authority impersonation, unusual payment, lookalike domains, credential requests, generic greetings, grammar mismatches, refund confirmations, wrong-number pivots, upfront-payment job offers, fake tech support, emotional manipulation.",
        "<b>Few-shot via pattern library.</b> Five seed patterns are injected verbatim. Each carries a sanitized example and 3–6 observable red flags. Community contributions expand this without code changes.",
        "<b>Decision rules.</b> Explicit tie-breakers — 'when in doubt between safe and suspicious, choose suspicious'; 'between suspicious and scam, require clear evidence to call it scam.' This nudges Claude toward calibrated outputs and prevents both crying-wolf and false-negatives equally.",
        "<b>Strict JSON contract.</b> The output schema is given inline. The model is instructed to return ONLY JSON, no markdown fences and no prose. The client strips fences defensively in case the model adds them anyway.",
    ]))

    s.append(p("7.4 Output contract — what the model must produce", H2))
    s.append(code(
        '''{
  "verdict": "safe" | "suspicious" | "scam",
  "confidence": <integer 1–10>,
  "headline": "<one sentence>",
  "red_flags": ["<phrase quoted from message>", ...],
  "what_to_do": "<concrete next step>",
  "if_already_clicked": "<recovery steps; OMIT unless verdict === 'scam'>"
}'''
    ))
    s.append(p(
        "If the response fails to parse or doesn't match this shape, the client throws a generic "
        "<i>Got an unexpected response</i> error rather than guessing.",
        BODY,
    ))

    s.append(p("7.5 Verdict semantics — how the UI interprets each value", H2))

    verdict_table_data = [
        [Paragraph("<b>verdict</b>", BODY), Paragraph("<b>Color</b>", BODY), Paragraph("<b>UI label</b>", BODY), Paragraph("<b>Renders recovery panel?</b>", BODY)],
        [Paragraph("safe", BODY), Paragraph("green-600", BODY), Paragraph("🟢 Looks Safe", BODY), Paragraph("No", BODY)],
        [Paragraph("suspicious", BODY), Paragraph("yellow-500", BODY), Paragraph("🟡 Suspicious", BODY), Paragraph("No", BODY)],
        [Paragraph("scam", BODY), Paragraph("red-600", BODY), Paragraph("🔴 Scam", BODY), Paragraph("Yes (if <font face='Courier'>if_already_clicked</font> present)", BODY)],
    ]
    verdict_table = Table(verdict_table_data, colWidths=[1.0 * inch, 1.0 * inch, 1.4 * inch, 2.6 * inch])
    verdict_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F9FAFB")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    s.append(verdict_table)
    s.append(Spacer(1, 6))

    s.append(p("7.6 Why a single-shot prompt instead of a classifier model?", H2))
    s.append(bullets([
        "<b>No training data needed.</b> A fine-tuned classifier would require labeled examples and ongoing retraining as scams evolve. Claude already generalizes.",
        "<b>Reasoning is the product.</b> The user needs to see <i>why</i> something is a scam, not just a score. Generative output gives us free-form red flags and recovery advice that a classifier cannot.",
        "<b>Cost &amp; latency are acceptable.</b> Haiku-class scans complete in roughly 1–2 seconds. The user is already in 'I'm worried about this message' mode; a brief wait is fine.",
        "<b>Updates ship without a model retrain.</b> Adding patterns is a PR. Tweaking decision rules is a prompt edit.",
    ]))

    # ---- 8. Privacy ----
    s.append(section_header("8. Privacy & Security Architecture", "privacy"))
    s.append(p(
        "The privacy story is the architecture. There is no server with a hard drive that could be subpoenaed or breached, "
        "because there is no server. Concretely:",
        BODY,
    ))
    s.append(bullets([
        "<b>No backend.</b> The repo contains zero server code. The 'deploy' is uploading static files to a CDN.",
        "<b>BYOK.</b> The user supplies their own Anthropic key. The key is stored only in <font face='Courier'>localStorage</font>, never sent anywhere except as an Authorization header on direct calls to <font face='Courier'>api.anthropic.com</font>.",
        "<b>Zero third-party scripts.</b> No analytics, no error reporting, no fonts CDN, no CAPTCHA. The only outbound origin at runtime is <font face='Courier'>api.anthropic.com</font> — verified in Phase 6 via the Network panel.",
        "<b>Scan history is device-local.</b> Up to the last 20 results live in <font face='Courier'>localStorage</font>. Clearing browser data clears history. A Clear-history link gives an explicit in-app reset.",
        "<b>No PII collection.</b> The app never asks for a name, email, or phone number.",
    ]))

    s.append(p("8.1 The <font face='Courier'>dangerouslyAllowBrowser</font> flag", H2))
    s.append(p(
        "The Anthropic SDK requires this opt-in flag for direct browser calls because, in a typical SaaS context, "
        "shipping an API key to the browser leaks it to whoever opens the page. In Scam Shield, the user IS the one "
        "shipping the key — to themselves. The flag is therefore not 'dangerous' in our deployment; it is the whole "
        "point of the BYOK design. <b>CLAUDE.md explicitly warns future contributors not to 'fix' this.</b>",
        BODY,
    ))

    s.append(p("8.2 Threat model", H2))
    s.append(p(
        "Within the deployment described above, the threats Scam Shield does and does not address:",
        BODY,
    ))
    s.append(bullets([
        "<b>Mitigated — server-side data breach.</b> No server, no breach.",
        "<b>Mitigated — third-party telemetry leakage.</b> No third parties.",
        "<b>Mitigated — credential exfiltration via supply chain.</b> The only key on the device is the user's own; no shared secrets.",
        "<b>Out of scope — browser-level malware.</b> A compromised browser can read localStorage. This is true of any local-storage application.",
        "<b>Out of scope — Anthropic's data retention.</b> Once the API call is in flight, Anthropic's usage policy governs it. Documented in the README disclaimer.",
        "<b>Out of scope — host CDN integrity.</b> A compromised static host could ship a malicious bundle. Mitigation: Subresource Integrity is a future addition.",
    ]))

    # ---- 9. UI state machine ----
    s.append(section_header("9. UI State Machine & Accessibility", "ui"))
    s.append(p("9.1 View states", H2))
    s.append(code(
        '''type View =
  | "loading"      // mount: read API key + history, load patterns
  | "needs-key"    // first-run; show ApiKeySetup in onboarding mode
  | "idle"         // main screen: PrivacyNote + ScanInput + HistoryList
  | "scanning"     // ScanInput frozen, button reads "Reading the message…"
  | "result"       // ResultCard for the most recent scan
  | "settings";    // ApiKeySetup in edit/clear mode'''
    ))
    s.append(p("9.2 Transitions", H2))
    s.append(bullets([
        "<b>loading → needs-key</b>: no API key in storage.",
        "<b>loading → idle</b>: API key present.",
        "<b>needs-key → idle</b>: user saves a key (also reachable from settings).",
        "<b>idle → scanning</b>: user submits non-empty input.",
        "<b>scanning → result</b>: API returned a valid ScanResult; history is updated.",
        "<b>scanning → idle</b>: API or shape error; <font face='Courier'>scanError</font> is set and rendered inline by ScanInput.",
        "<b>result → idle</b>: user taps 'Check another message.'",
        "<b>idle / result → settings</b>: user taps the gear icon.",
        "<b>settings → idle</b>: cancel or save.",
        "<b>settings → needs-key</b>: 'Remove key from this device.'",
    ]))

    s.append(p("9.3 Accessibility design", H2))
    s.append(kv_table([
        ("Base font", "18 px set on &lt;html&gt;. All Tailwind utilities are recomputed against this root."),
        ("Tap targets", "Every interactive element has <font face='Courier'>min-h-11</font> (= 2.75 rem ≈ 49.5 px). Verified at runtime."),
        ("Viewport", "Mobile-first; tested at 375 × 812. Content uses <font face='Courier'>max-w-xl</font> centered with <font face='Courier'>px-5</font>. No horizontal scrolling at 375 px (verified)."),
        ("Color contrast", "All text on background pairs satisfy WCAG AA. Verdict header tiles use red-600/yellow-500/green-600 with appropriate foreground."),
        ("Focus states", "Every button has <font face='Courier'>focus:outline-none focus:ring-2 focus:ring-gray-900</font> (or red-600 for destructive)."),
        ("Live errors", "Error containers use <font face='Courier'>role='alert'</font> so screen readers announce them."),
        ("Form labels", "Every input has a real &lt;label htmlFor&gt; — no placeholder-as-label anti-patterns."),
        ("Language", "Plain English. Read level &lt; 8th grade in user-facing copy. No security jargon."),
    ]))

    # ---- 10. Errors ----
    s.append(section_header("10. Error Handling and Resilience", "errors"))
    s.append(p(
        "Errors are rerouted through a single <font face='Courier'>ScanError</font> class whose message is "
        "always safe to render in the UI. Mappings are explicit:",
        BODY,
    ))
    err_data = [
        [Paragraph("<b>Source</b>", BODY), Paragraph("<b>Message shown to user</b>", BODY)],
        [Paragraph("HTTP 401", BODY), Paragraph("Your API key looks invalid. Double-check it in Settings.", BODY)],
        [Paragraph("HTTP 429", BODY), Paragraph("You're sending requests too fast. Wait a moment and try again.", BODY)],
        [Paragraph("HTTP 529", BODY), Paragraph("Anthropic's servers are busy. Try again in a few seconds.", BODY)],
        [Paragraph("APIConnectionError", BODY), Paragraph("Couldn't reach Anthropic. Check your internet connection.", BODY)],
        [Paragraph("JSON parse / shape failure", BODY), Paragraph("Got an unexpected response. Try again — if it keeps happening, open an issue.", BODY)],
        [Paragraph("Empty input", BODY), Paragraph("Please paste a message or upload a screenshot first.", BODY)],
        [Paragraph("Unsupported image type", BODY), Paragraph("That image type isn't supported. Try a JPEG, PNG, GIF, or WebP screenshot.", BODY)],
    ]
    err_table = Table(err_data, colWidths=[1.8 * inch, 4.4 * inch])
    err_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F9FAFB")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    s.append(err_table)
    s.append(Spacer(1, 8))

    s.append(p(
        "All localStorage operations are wrapped in try/catch. A storage failure (Safari private mode, quota exceeded, "
        "user disabled storage) degrades silently — the user can still scan, just won't persist history between reloads.",
        BODY,
    ))

    # ---- 11. Build/deploy ----
    s.append(section_header("11. Build, Bundle, and Deployment", "build"))
    s.append(p("Build pipeline", H2))
    s.append(code(
        '''npm run build
  → tsc -b          (strict TypeScript across the project references)
  → vite build      (Rolldown bundler, Tailwind JIT, asset hashing)
  → dist/
      index.html                 0.6 KB  (entry)
      assets/index-*.css        12.0 KB  (Tailwind utilities)
      assets/index-*.js        365.0 KB  (React + SDK + app code)
      assets/node-*.js          15.2 KB  (browser shim for SDK node paths)
      assets/__vite-browser-external-*.js    0.1 KB

Total gzipped: ~118 KB. Target: under 500 KB. ✓'''
    ))

    s.append(p("Why the &quot;node-*.js&quot; chunk exists", H2))
    s.append(p(
        "The Anthropic SDK ships an agent-toolset module that imports node-only builtins "
        "(<font face='Courier'>node:fs</font>, <font face='Courier'>node:path</font>, etc.). Vite externalizes "
        "these for the browser build and emits a tiny shim. The code paths that would call them are never "
        "executed in BYOK browser usage — only <font face='Courier'>client.messages.create</font> is. The "
        "shim is benign at runtime; the build-time warnings are cosmetic. Future cleanup: pin imports to "
        "<font face='Courier'>@anthropic-ai/sdk/index</font> or add a Vite optimizeDeps exclude.",
        BODY,
    ))

    s.append(p("Deployment", H2))
    s.append(bullets([
        "<b>Cloudflare Pages</b>: connect GitHub repo, set build command <font face='Courier'>npm run build</font>, output directory <font face='Courier'>dist</font>, no env vars. Every push to <font face='Courier'>main</font> redeploys.",
        "<b>GitHub Pages, Netlify, Vercel, S3+CloudFront</b>: identical configuration. The bundle is fully static — no runtime requirements beyond a modern browser.",
        "<b>CSP &amp; SRI</b> (future): a sensible Content-Security-Policy and Subresource Integrity on the JS bundle would harden against a host-level compromise.",
    ]))

    # ---- 12. Extensibility ----
    s.append(section_header("12. Extensibility", "extensibility"))
    s.append(p("Adding a new scam pattern", H2))
    s.append(bullets([
        "Drop a new JSON file in <font face='Courier'>src/scam-patterns/</font>.",
        "Conform to the ScamPattern shape (Section 5). Filename matches <font face='Courier'>id</font>.",
        "Add a one-line entry to <font face='Courier'>src/scam-patterns/index.json</font> for discoverability.",
        "Open a PR. <b>Sanitize the example</b> — see docs/CONTRIBUTING.md for the full PII checklist (names, phone numbers, URLs in bracket notation, fake reference numbers).",
        "On merge, the next build picks it up automatically via <font face='Courier'>import.meta.glob</font>.",
    ]))

    s.append(p("Tuning Claude's behavior", H2))
    s.append(bullets([
        "Edit the template in <font face='Courier'>src/lib/prompt.ts</font>.",
        "Decision rules and the output schema are inline in the template — keep them in sync with <font face='Courier'>isScanResult</font> in <font face='Courier'>src/lib/claude.ts</font>.",
        "Bumping to a newer model is a two-line change at the top of <font face='Courier'>src/lib/claude.ts</font>.",
    ]))

    s.append(p("Why not a plugin system?", H2))
    s.append(p(
        "Three things would justify one: more than ~50 patterns, contributors who need to write code rather than JSON, "
        "or runtime pattern loading from a remote source. None apply yet. A JSON-per-pattern + Vite glob is simpler and "
        "type-safe enough.",
        BODY,
    ))

    # ---- 13. Limitations ----
    s.append(section_header("13. Limitations and Future Work", "limits"))
    s.append(p("Known limitations of v0.1.0", H2))
    s.append(bullets([
        "<b>English only.</b> Both the prompt and the user-facing copy assume English.",
        "<b>Claude can be wrong.</b> Both false positives and false negatives are possible. The README and the UI are explicit about this.",
        "<b>Single message at a time.</b> No conversation context; no carrying over what the user has scanned before. (Past scans live in history but do not feed the next prompt.)",
        "<b>No accessibility audit by a third party</b> — best effort against WCAG AA only.",
        "<b>Image upload size.</b> Not yet capped on the client; very large screenshots may slow the upload.",
        "<b>No Playwright / unit tests.</b> Smoke-tested manually in Phase 6.",
    ]))

    s.append(p("Roadmap candidates (post-MVP)", H2))
    s.append(bullets([
        "End-to-end browser tests in Playwright (golden-path + error paths).",
        "Localization: prompt + UI in at least Spanish and Mandarin.",
        "Optional pattern-feedback loop — a 'this verdict was wrong' link that opens a sanitized PR template.",
        "PWA install + offline cache for assets (still online for API call).",
        "Voice readout of the verdict for low-vision users.",
        "Image-size cap with friendly downscaling client-side.",
        "Subresource Integrity hashes on the production bundle.",
        "Pluggable model selection (let advanced users pick a different Claude model from Settings).",
    ]))

    # ---- Appendix A ----
    s.append(PageBreak())
    s.append(section_header("Appendix A — Full System Prompt", "appA"))
    s.append(p(
        "Below is the full prompt text built by <font face='Courier'>buildSystemPrompt()</font>. The literal "
        "<font face='Courier'>{{PATTERNS}}</font> token is replaced at runtime with each scam pattern formatted "
        "as a small block of name, category, description, example, and indented red-flag bullets.",
        BODY,
    ))
    sys_prompt = (
        'You are a scam-detection expert helping a non-technical person —\n'
        'imagine someone in their 70s — evaluate a suspicious message they received.\n'
        '\n'
        'Your job: classify the message and explain your reasoning in plain English\n'
        'that a grandparent would understand. Never use jargon. Never say "phishing" —\n'
        'say "a fake message pretending to be USPS" or similar. Be specific by\n'
        'quoting actual phrases from the message in your red_flags.\n'
        '\n'
        'Look for these scam patterns:\n'
        '- Urgency manipulation ("act now," "24 hours," "immediately," "final notice")\n'
        '- Authority impersonation (banks, IRS, USPS, FedEx, Amazon, Microsoft, police)\n'
        '- Unusual payment requests (gift cards, wire transfers, cryptocurrency, ...)\n'
        '- Lookalike or suspicious domains (amaz0n.com, paypaI.com, IP addresses, ...)\n'
        '- Credential requests (passwords, one-time codes, SSN, bank account numbers)\n'
        '- Generic greetings ("Dear customer," "Dear user," "Hello sir/madam")\n'
        '- Grammar or formatting that doesn\'t match the claimed sender\n'
        '- Refund or payment confirmations the recipient didn\'t initiate\n'
        '- "Wrong number" texts that pivot to friendship, romance, or crypto investing\n'
        '- Job offers requiring upfront payment, training fees, or check-cashing\n'
        '- Tech support claims of viruses or account compromise requiring remote access\n'
        '- Emotional manipulation (fear, romance, sympathy, prize winnings)\n'
        '\n'
        'Known scam patterns for reference:\n'
        '{{PATTERNS}}\n'
        '\n'
        'Decision rules:\n'
        '- When in doubt between "safe" and "suspicious," choose "suspicious."\n'
        '- When in doubt between "suspicious" and "scam," choose "scam" only if there\n'
        '  is clear evidence (specific quoted red flags); otherwise "suspicious."\n'
        '- Legitimate messages from real senders should be marked "safe."\n'
        '- A legitimate-looking message that asks for sensitive information through an\n'
        '  unusual channel is at least "suspicious."\n'
        '\n'
        'Output: return ONLY a valid JSON object matching this shape. No markdown\n'
        'fences, no preamble, no explanation outside the JSON.\n'
        '\n'
        '{\n'
        '  "verdict": "safe" | "suspicious" | "scam",\n'
        '  "confidence": <integer 1-10>,\n'
        '  "headline": "<one sentence summary in plain English>",\n'
        '  "red_flags": ["<specific phrase or feature from the message>", ...],\n'
        '  "what_to_do": "<grandparent-friendly action the recipient should take>",\n'
        '  "if_already_clicked": "<recovery steps — include this field ONLY if\n'
        '    verdict is \'scam\', otherwise omit it entirely>"\n'
        '}'
    )
    s.append(code(sys_prompt))

    # ---- Appendix B ----
    s.append(section_header("Appendix B — ScanResult JSON Schema", "appB"))
    s.append(p(
        "Equivalent JSON Schema for the structured output. The runtime validator in "
        "<font face='Courier'>src/lib/claude.ts</font> implements this check by hand "
        "(no external schema library).",
        BODY,
    ))
    s.append(code(
        '''{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["verdict", "confidence", "headline", "red_flags", "what_to_do"],
  "properties": {
    "verdict": { "type": "string", "enum": ["safe", "suspicious", "scam"] },
    "confidence": { "type": "integer", "minimum": 1, "maximum": 10 },
    "headline": { "type": "string", "minLength": 1 },
    "red_flags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "what_to_do": { "type": "string", "minLength": 1 },
    "if_already_clicked": { "type": "string" }
  },
  "allOf": [
    {
      "if": { "properties": { "verdict": { "const": "scam" } } },
      "then": {}
    },
    {
      "if": { "not": { "properties": { "verdict": { "const": "scam" } } } },
      "then": { "not": { "required": ["if_already_clicked"] } }
    }
  ]
}'''
    ))

    # ---- Appendix C ----
    s.append(section_header("Appendix C — Project File Tree", "appC"))
    tree = (
        'scam-shield/\n'
        '├── CLAUDE.md                project contract for future contributors\n'
        '├── README.md                user-facing readme\n'
        '├── LICENSE                  MIT\n'
        '├── .gitignore\n'
        '├── .env.example             intentionally empty (no env vars)\n'
        '├── package.json\n'
        '├── package-lock.json\n'
        '├── vite.config.ts\n'
        '├── tailwind.config.js\n'
        '├── postcss.config.js\n'
        '├── tsconfig.json\n'
        '├── tsconfig.app.json\n'
        '├── tsconfig.node.json\n'
        '├── eslint.config.js\n'
        '├── index.html               single entry point\n'
        '├── public/\n'
        '│   └── icon.svg             shield favicon\n'
        '├── src/\n'
        '│   ├── main.tsx             React root bootstrap\n'
        '│   ├── App.tsx              View state machine\n'
        '│   ├── index.css            Tailwind directives + 18 px base\n'
        '│   ├── types.ts             Verdict / ScanResult / ScanHistoryItem / ScamPattern\n'
        '│   ├── components/\n'
        '│   │   ├── Layout.tsx\n'
        '│   │   ├── PrivacyNote.tsx\n'
        '│   │   ├── ApiKeySetup.tsx\n'
        '│   │   ├── ScanInput.tsx\n'
        '│   │   ├── ResultCard.tsx\n'
        '│   │   └── HistoryList.tsx\n'
        '│   ├── lib/\n'
        '│   │   ├── claude.ts        scanMessage() + ScanError\n'
        '│   │   ├── storage.ts       localStorage wrapper\n'
        '│   │   ├── prompt.ts        buildSystemPrompt(patterns)\n'
        '│   │   └── patterns.ts      loadPatterns() via import.meta.glob\n'
        '│   └── scam-patterns/\n'
        '│       ├── index.json       discovery list (skipped by loader)\n'
        '│       ├── usps-package-fee.json\n'
        '│       ├── irs-back-taxes.json\n'
        '│       ├── wrong-number-crypto.json\n'
        '│       ├── refund-confirmation.json\n'
        '│       └── job-offer-upfront.json\n'
        '└── docs/\n'
        '    ├── CONTRIBUTING.md      pattern-PR rules + PII sanitization\n'
        '    └── TECH_DESIGN.pdf      this document'
    )
    s.append(code(tree))

    return s


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = build_doc(OUT_PATH)
    story = build_story()
    doc.build(story)
    print(f"Wrote {OUT_PATH}")
    print(f"Size: {OUT_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
