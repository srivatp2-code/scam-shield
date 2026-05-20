# Scam Shield

An open-source web app that uses Claude to detect scams in messages, designed for non-technical users.

## Architecture

- **Client-side only.** No backend. Everything runs in the user's browser.
- **BYOK.** User provides their own Anthropic API key, stored in localStorage.
- **Static deploy.** Builds to a `dist/` folder, deploys to any static host (Cloudflare Pages, GitHub Pages, Netlify).
- **No telemetry.** No analytics, no tracking, no third-party scripts.

## Tech stack

Vite 5 + React 18 + TypeScript (strict) + Tailwind v3 + `@anthropic-ai/sdk`.

## Project conventions

- **No new dependencies without asking.** Keep the bundle small.
- **No backend, ever.** If a feature seems to need one, propose an alternative first.
- **No telemetry, no tracking.** Hard rule.
- **Accessibility first.** Base font 18px, contrast AA minimum, tap targets 44px, works one-handed on mobile.
- **Plain language in user-facing copy.** Imagine a 70-year-old reading it. No jargon — never say "phishing," say "fake message pretending to be X."
- **TypeScript strict mode.** No `any` without a comment explaining why.
- **Functional components and hooks only.** No class components.
- **Tailwind utility classes only.** No CSS-in-JS, no separate CSS files except `index.css` for Tailwind directives.

## Domain concepts

- **Verdict:** the model's classification — `safe`, `suspicious`, or `scam`.
- **Red flags:** specific phrases or features in the message that suggest a scam, quoted from the input.
- **Scam pattern:** a JSON file in `src/scam-patterns/` describing a known scam type, injected into the system prompt as few-shot context. Community-contributed via PRs.

## When extending the system prompt

The system prompt lives in `src/lib/prompt.ts`. Patterns from `src/scam-patterns/` are injected at runtime. If you change the prompt, also update the JSON schema validation in `src/lib/claude.ts` to match.

## Testing principle

Before committing UI changes, manually test in 375px viewport. Before committing prompt changes, run at least three known-scam and three known-safe examples through the model.

## Security boundaries

- Never log the API key.
- Never send the API key anywhere other than `api.anthropic.com`.
- Never store scanned message content outside localStorage on the user's own device.
- The `dangerouslyAllowBrowser: true` flag is intentional and is the entire point of the BYOK architecture — do not "fix" this.
