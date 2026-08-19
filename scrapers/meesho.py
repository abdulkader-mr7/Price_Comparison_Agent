from .utils import get_stealth_context
import random
import asyncio

async def scrape_meesho(query, browser):
    results = []
    context = await get_stealth_context(browser)
    page = await context.new_page()
    
    try:
        url = f"https://www.meesho.com/search?q={query.replace(' ', '%20')}"
        # Set shorter timeout for page load in case of blocking proxy or anti-bot
        try:
             await page.goto(url, timeout=15000, wait_until="domcontentloaded")
        except:
             pass

        await asyncio.sleep(random.uniform(1, 3))
        
        # Check if we got an access denied page
        content = await page.content()
        if "Access Denied" in content:
             print("Meesho access denied (IP blocked). Returning empty results gracefully.")
             return results
        
        # Wait for either old grid class or any product-like card
        try:
             await page.wait_for_selector('div[class*="ProductList__GridCol"]', timeout=5000)
             products = await page.query_selector_all('div[class*="ProductList__GridCol"]')
        except:
             # Look for any links with image and price
             products = await page.query_selector_all('a[href*="/p/"]')
             if not products:
                  products = await page.query_selector_all('a[href*="/s/"]')

        for product in products[:5]:
            try:
                # Handle generic anchor tags
                if await product.evaluate("el => el.tagName") == "A":
                     link_el = product
                     img_el = await product.query_selector("img")
                     texts = await product.inner_text()
                else:
                     link_el = await product.query_selector("a")
                     img_el = await product.query_selector("img")
                     texts = await product.inner_text()
                
                title = ""
                price = ""
                
                if img_el:
                     title = await img_el.get_attribute("alt")

                for line in texts.split('\n'):
                     if '₹' in line and not price:
                          price = line.strip()
                     elif len(line) > 10 and not title: # Fallback for title if no alt
                          title = line.strip()
                
                if not title and img_el:
                     title = "Meesho Product"

                if price and img_el:
                    image = await img_el.get_attribute("src")
                    link = await link_el.get_attribute("href")
                    if not link.startswith('http'):
                         link = f"https://www.meesho.com{link}"
                    
                    results.append({
                        'title': title.strip(),
                        'price': price.strip(),
                        'image': image,
                        'link': link,
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
