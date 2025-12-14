from .utils import get_stealth_context
import random
import asyncio

async def scrape_meesho(query, browser):
    results = []
    context = await get_stealth_context(browser)
    page = await context.new_page()
    
    try:
        url = f"https://www.meesho.com/search?q={query.replace(' ', '%20')}"
        await page.goto(url, timeout=45000, wait_until="domcontentloaded")
        await asyncio.sleep(random.uniform(1, 3))
        
        # Meesho is an SPA. Wait for grid.
        await page.wait_for_selector('div[class*="ProductList__GridCol"]', timeout=10000)
        
        products = await page.query_selector_all('div[class*="ProductList__GridCol"]')
        
        for product in products[:5]:
            try:
                # Title: p[class*="NewProductCard__ProductTitle"] 
                # Often generic classes like 'sc-...'
                
                # We can try selecting by structure
                # Title usually in a p tag with specific color or styling
                
                title_el = await product.query_selector('p[color="greyT2"]') # Product name often has this
                
                # Price: h5
                price_el = await product.query_selector("h5")
                
                # Image: img
                img_el = await product.query_selector("img")
                
                # Link: a
                link_el = await product.query_selector("a")
                
                title = ""
                if title_el:
                        title = await title_el.inner_text()
                else:
                        # Fallback: Try fetching alt text from image
                        title = await img_el.get_attribute("alt") if img_el else "Unknown Product"

                if price_el and img_el:
                    price = await price_el.inner_text()
                    image = await img_el.get_attribute("src")
                    link = await link_el.get_attribute("href")
                    
                    results.append({
                        'title': title,
                        'price': price,
                        'image': image,
                        'link': f"https://www.meesho.com{link}",
                        'source': 'Meesho'
                    })
            except Exception as e:
                print(f"Meesho item error: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping Meesho: {e}")
    finally:
        await context.close()
        
    return results
