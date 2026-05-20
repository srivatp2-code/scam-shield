# Scam Shield

A free, open-source web app that helps you check whether a suspicious email or text is a scam. Paste the message (or upload a screenshot) and get a clear 🟢 / 🟡 / 🔴 verdict in plain English.

| Onboarding | Main screen | Result |
| --- | --- | --- |
| `[screenshot here]` | `[screenshot here]` | `[screenshot here]` |

## Why this exists

Scams are getting more sophisticated, and the people most likely to be targeted — parents, grandparents, anyone who isn't online all day — are often the least equipped to evaluate them. Existing tools either bury the answer in jargon or require a corporate subscription. Scam Shield is meant to be the thing you text to your mom: a single page, no signup, no tracking, and an answer she can read.

## How it works

```
┌───────────────────────────────────────────────────────────────┐
│                       Your device                             │
│                                                               │
│   ┌────────────┐      ┌──────────────┐      ┌──────────────┐  │
│   │  Paste a   │ ───▶ │   Browser    │ ───▶ │   Anthropic  │  │
│   │  message   │      │  (this app)  │      │     API      │  │
│   └────────────┘      └──────┬───────┘      └──────┬───────┘  │
│                              │                      │         │
│                              ▼                      ▼         │
│                      ┌──────────────┐       Verdict + reasons │
│                      │ localStorage │              │          │
│                      │  • API key   │              │          │
│                      │  • history   │              ▼          │
│                      └──────────────┘     ┌────────────────┐  │
│                                           │  🔴/🟡/🟢       │  │
│                                           │  plain English │  │
│                                           └────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

Everything runs in your browser. Your message is sent directly to Anthropic using your own API key. Nothing is sent to us — there is no "us."

## 30-second setup

1. **Get an Anthropic API key** (free to start): https://console.anthropic.com/settings/keys
2. **Open Scam Shield** in your browser.
3. **Paste your key** when prompted — it's saved on your device only.
4. **Paste a suspicious message** and tap "Check this message."

## Contributing scam patterns

Scam Shield ships with a small library of known scam patterns in [`src/scam-patterns/`](src/scam-patterns/). Each is a JSON file. When you add more, Claude gets better at spotting them.

See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for how to submit a new pattern — and please sanitize any real messages before committing them.

## Running locally

```bash
npm install
npm run dev
```

Open http://localhost:5173.

Production build (static, deploys anywhere):

```bash
npm run build
```

Output goes to `dist/`. Deploy with Cloudflare Pages, GitHub Pages, Netlify, Vercel, or any static host — see [Deploying](#deploying) below.

## Deploying

### Cloudflare Pages

1. Push the repo to GitHub.
2. In the Cloudflare dashboard, create a new Pages project and connect to the repo.
3. Set the build settings:
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Environment variables:** *(none)*
4. Deploy. Every push to `main` redeploys automatically.

### Other static hosts

Same idea — build with `npm run build`, serve the `dist/` directory. No backend, no env vars.

## Contributors

This is an open-source project. Anyone is welcome to contribute scam patterns, bug fixes, or accessibility improvements. See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

## Limitations & disclaimer

> Scam Shield is a helpful second opinion. It is **not** legal, financial, or security advice.

- **Claude can be wrong.** Like any AI, it can miss a real scam (a false 🟢) or flag a real message as suspicious (a false 🔴). Treat the verdict as a starting point, not a verdict in the legal sense.
- **Always verify with the real sender through a known channel.** If a message claims to be from your bank, your kid, or the IRS — call the number on the back of your card, call your kid directly, or look up the agency's number on their official website. Don't use any phone number or link in the suspicious message.
- **Already replied or paid?** Time matters. Contact your bank, your local police, and (in the US) [reportfraud.ftc.gov](https://reportfraud.ftc.gov). Don't wait.
- **Your data stays local.** Messages you check are sent directly from your browser to Anthropic's API and aren't stored on any server we control. Scan history lives in your browser's localStorage; clearing your browser data clears it. Anthropic's API has its own [usage policies](https://www.anthropic.com/legal/usage-policy) and may retain request data per their terms.
- **You pay Anthropic, not us.** API costs are billed by Anthropic to whoever owns the key. A typical scan costs well under a cent.

## License

[MIT](LICENSE) © 2026 Sri Pusarla
