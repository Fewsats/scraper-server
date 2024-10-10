# Web Scraping Service

FastAPI-based web scraping service using Trafilatura. Similar to firecrawl.dev in output format and request parameters.

## Setup

1. Clone repo
2. Install dependencies: `make install`
3. Set API key: `export FEWSATS_SCRAPER_API_KEY=your-secret-token`

## Run

`make run`

## API

`POST /v0/scrape`

Headers:
- `Authorization: Bearer your-secret-token`

Body:

```json
{
    "url": "https://example.com",
    "format": "markdown"
}
```

Response:

```json
{
    "success": true,
    "data": {
        "markdown": "...",
        "metadata": {
        "title": "...",
        "language": "...",
        "ogLocaleAlternate": [],
        "sourceURL": "https://paywithhub.com",
            "statusCode": 200
        }
    }
}
```

Example cURL request:

```bash
curl -X POST http://localhost:9111/v0/scrape \
     -H "Authorization: Bearer $FEWSATS_SCRAPER_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://paywithhub.com", "format": "markdown"}'
```