# Finance Market Providers

`finance-market` is the educational market-data layer for local agents.

## Provider Contract

Every market lookup should include:

- Provider name
- Symbol or asset id
- Currency
- Price or result data
- Timestamp/freshness signal when available
- Disclaimer that the output is not financial advice

## Built-In Providers

- `yahoo-chart` - stock, ETF, index, FX, and Yahoo-compatible symbols through the chart endpoint.
- `coingecko` - crypto spot prices by CoinGecko coin id through `/simple/price`.
- `web-news` - finance-news query planning for use with `web` and `web-capture`.

## Recommended Workflow

1. Use `plan_finance_lookup` to choose providers.
2. Use `get_market_quote` or `get_crypto_price` for price context.
3. Use `plan_finance_news_query`, then `web` or `web-capture`, for current public news.
4. Include provider, currency, and timestamp/freshness caveat in the answer.
5. Avoid buy/sell recommendations unless the user explicitly asks for educational scenario analysis, and still label uncertainty.

## Safety

These tools are for research and education only. They do not replace a broker, exchange, licensed advisor, or official issuer filings.
