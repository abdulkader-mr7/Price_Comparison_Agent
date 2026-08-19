from .utils import get_stealth_context
import random
import asyncio

async def scrape_amazon(query, browser):
    results = []
    # Create isolated context for this scrape
    context = await get_stealth_context(browser)
    page = await context.new_page()
    
    try:
        url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
        await page.goto(url, timeout=45000, wait_until='domcontentloaded')
        
        # Anti-bot delay
        await asyncio.sleep(random.uniform(1.5, 3.5))
        
        # fast wait for results
        await page.wait_for_selector('div[data-component-type="s-search-result"]', timeout=15000)
        
        products = await page.query_selector_all('div[data-component-type="s-search-result"]')
        
        for product in products[:5]: # Top 5 results
            try:
                title_el = await product.query_selector("h2 span")
                price_el = await product.query_selector(".a-price span.a-offscreen")
                if not price_el:
                     price_el = await product.query_selector(".a-price-whole") # Fallback
                     
                img_el = await product.query_selector("img.s-image")

                link_el = await product.query_selector("a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
                if not link_el:
                    link_el = await product.query_selector("h2 a")
                
                if title_el and price_el and img_el:
                    title = await title_el.inner_text()

                    if len(title) < 15:
                        alt_title = await img_el.get_attribute("alt")
                        if alt_title:
                             title = alt_title

                    price = await price_el.inner_text()
                    if not price.startswith("₹"):
                        price = f"₹{price}"

                    image = await img_el.get_attribute("src")

                    link = ""
                    if link_el:
                        link_href = await link_el.get_attribute("href")
                        if link_href:
                            link = f"https://www.amazon.in{link_href}"
                    
                    results.append({
                        'title': title,
                        'price': price,
                        'image': image,
                        'link': link,
                        'source': 'Amazon'
                    })
            except Exception as e:
                print(f"Amazon item error: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
    finally:
        await context.close()
        
    return results
