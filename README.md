# Scam Shield

A free, open-source web app that helps you check whether a suspicious email or text is a scam. Paste the message (or upload a screenshot) and get a clear 🟢 / 🟡 / 🔴 verdict in plain English.

## Why this exists

Scams are getting more sophisticated, and the people most likely to be targeted — parents, grandparents, anyone who isn't online all day — are often the least equipped to evaluate them. Existing tools either bury the answer in jargon or require a corporate subscription. Scam Shield is meant to be the thing you text to your mom: a single page, no signup, no tracking, and an answer she can read.

## How it works

```
[ Your message ]  →  Your browser  →  api.anthropic.com  →  Verdict
                          ↑
                  (your API key,
                  stored on your device)
```

Everything runs in your browser. Your message is sent directly to Anthropic using your own API key. Nothing is sent to us — there is no "us."

## 30-second setup

1. **Get an Anthropic API key** (free to start): https://console.anthropic.com/settings/keys
2. **Open Scam Shield** in your browser.
3. **Paste your key** when prompted — it's saved on your device only.
4. **Paste a suspicious message** and tap "Check this message."

## Contributing scam patterns

Scam Shield ships with a small library of known scam patterns in `src/scam-patterns/`. Each is a JSON file. When you add more, Claude gets better at spotting them.

See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for how to submit a new pattern.

## Running locally

```bash
npm install
npm run dev
```

Builds to a static `dist/` folder:

```bash
npm run build
```

## License

[MIT](LICENSE)
