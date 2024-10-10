from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import trafilatura
from trafilatura.settings import use_config
from typing import Dict, Any, Optional
import os

app = FastAPI()
security = HTTPBearer()

class ScrapeResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

def enhanced_scrape(url: str, format: str = 'markdown') -> Dict[str, Any]:
    config = use_config()
    config.set("DEFAULT", "PARAGRAPH_PROCESSING", "yes")
    
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        raise ValueError("Failed to fetch the URL")
    
    content = trafilatura.extract(
        downloaded,
        no_fallback=True,
        output_format=format,
        config=config,
        include_comments=False,
        include_tables=True,
        include_images=True,
        include_links=True,
    )
    
    if content is None:
        raise ValueError("Failed to extract content")
    
    metadata = trafilatura.extract_metadata(downloaded)
    
    return {
        format: content,
        "metadata": {
            "title": metadata.title,
            "language": metadata.language,
            "ogLocaleAlternate": [],
            "sourceURL": str(url),
            "statusCode": 200
        }
    }

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != os.getenv("FEWSATS_SCRAPER_API_KEY", "random-string-default"):
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials.credentials

@app.post("/v0/scrape", response_model=ScrapeResponse)
async def scrape(request: Request, token: str = Depends(verify_token)):
    try:
        data = await request.json()
        url = data.get('url')
        format = data.get('format', 'markdown')

        if not url:
            raise ValueError("URL is required")

        content = enhanced_scrape(url, format)
        return ScrapeResponse(success=True, data=content)
    except ValueError as e:
        return ScrapeResponse(success=False, error=str(e)), 400
    except trafilatura.exceptions.HttpError as e:
        return ScrapeResponse(success=False, error=f"HTTP error: {str(e)}"), 502
    except Exception as e:
        return ScrapeResponse(success=False, error=f"Unexpected error: {str(e)}"), 500

if __name__ == "__main__":
    import uvicorn
    
    if "FEWSATS_SCRAPER_API_KEY" not in os.environ:
        print("Error: FEWSATS_SCRAPER_API_KEY environment variable is not set")
        exit(1)
    
    uvicorn.run(app, host="0.0.0.0", port=9111)