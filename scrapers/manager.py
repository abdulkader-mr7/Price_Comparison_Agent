import asyncio
from playwright.async_api import async_playwright
from .amazon import scrape_amazon
from .flipkart import scrape_flipkart
from .meesho import scrape_meesho

async def search_products_async(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            # Run scrapers in parallel with shared browser
            results = await asyncio.gather(
                scrape_amazon(query, browser),
                scrape_flipkart(query, browser),
                scrape_meesho(query, browser),
                return_exceptions=True
            )
            
            # Process results and handle errors
            data = {
                'amazon': results[0] if not isinstance(results[0], Exception) else {'error': str(results[0])},
                'flipkart': results[1] if not isinstance(results[1], Exception) else {'error': str(results[1])},
                'meesho': results[2] if not isinstance(results[2], Exception) else {'error': str(results[2])},
            }
            return data
        finally:
            await browser.close()

def search_products(query):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        return asyncio.run_coroutine_threadsafe(
            search_products_async(query), loop
        ).result()
    else:
        return loop.run_until_complete(search_products_async(query))

