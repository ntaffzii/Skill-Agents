# Web Capture Providers

`web-capture` is the provider-neutral web reading layer for local agents.

## Provider Contract

Every provider should return the same basic shape:

```json
{
  "success": true,
  "provider": "local-static",
  "url": "https://example.com",
  "title": "Example",
  "description": "",
  "content": "Readable Markdown-like text",
  "truncated": false,
  "links": []
}
```

## Built-In Providers

- `local-static` - fetch normal public HTML and extract readable content locally.
- `local-browser` - render public JavaScript-heavy pages with Playwright when browser runtime is installed.
- `firecrawl` - optional cloud/self-hosted adapter enabled by `FIRECRAWL_API_KEY` and optional `FIRECRAWL_API_URL`.

## Social Sites

For Facebook, Instagram, Threads, X, TikTok, LinkedIn, and similar platforms:

- Capture public pages only.
- Do not bypass login walls, CAPTCHAs, private accounts, paywalls, or platform access controls.
- Prefer official APIs, user exports, or user-provided HTML for stable structured data.
- Treat blocked or incomplete pages as a normal result, not something to evade.

## Adding Providers

Add a provider only when:

1. It can return the standard content shape.
2. Its credentials live in environment variables.
3. Missing credentials fail clearly.
4. It has rate limits and public-only safety notes.
5. It does not require skills/workflows to know provider-specific internals.
