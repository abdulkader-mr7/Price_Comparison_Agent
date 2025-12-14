from .utils import get_stealth_context
import random
import asyncio

# async def scrape_flipkart(query, browser):
#     results = []
#     context = await get_stealth_context(browser)
#     page = await context.new_page()
#
#     try:
#         url = f"https://www.flipkart.com/search?q={query.replace(' ', '%20')}"
#         await page.goto(url, timeout=45000)
#         await asyncio.sleep(random.uniform(1, 3))
#
#         # Flipkart has different layouts (grid vs list).
#         # We'll try generic selectors for cards.
#         # Common container class for search results in grid: ._1AtVbE
#
#         await page.wait_for_selector('div._1AtVbE', timeout=10000)
#
#         # Select proper container cards (ignoring headers/footers)
#         products = await page.query_selector_all('div._1AtVbE')
#
#         count = 0
#         for product in products:
#             if count >= 5: break
#
#             try:
#                 # Logic for "Grid" view (common for electronics)
#                 # Title: div._4rR01T or a.s1Q9rs
#                 title_el = await product.query_selector("div._4rR01T")
#                 if not title_el:
#                     title_el = await product.query_selector("a.s1Q9rs")
#
#                 # Price: div._30jeq3
#                 price_el = await product.query_selector("div._30jeq3")
#
#                 # Image: img._396cs4
#                 img_el = await product.query_selector("img._396cs4")
#
#                 # Link: a._1fQZEK or a.s1Q9rs
#                 link_el = await product.query_selector("a._1fQZEK")
#                 if not link_el:
#                         link_el = await product.query_selector("a.s1Q9rs")
#
#                 if title_el and price_el and img_el:
#                     title = await title_el.inner_text()
#                     price = await price_el.inner_text()
#                     image = await img_el.get_attribute("src")
#                     link = await link_el.get_attribute("href")
#
#                     results.append({
#                         'title': title,
#                         'price': price,
#                         'image': image,
#                         'link': f"https://www.flipkart.com{link}",
#                         'source': 'Flipkart'
#                     })
#                     count += 1
#             except Exception as e:
#                 print(f"Flipkart item error: {e}")
#                 continue
#
#     except Exception as e:
#         print(f"Error scraping Flipkart: {e}")
#     finally:
#         await context.close()
#
#     return results

from .utils import get_stealth_context
import random
import asyncio

async def scrape_flipkart(query, browser):
    results = []
    context = await get_stealth_context(browser)
    page = await context.new_page()

    try:
        url = f"https://www.flipkart.com/search?q={query.replace(' ', '%20')}"
        await page.goto(
            url,
            timeout=45000,
            wait_until="domcontentloaded"

        )

        await asyncio.sleep(random.uniform(1.5, 3))

        # 🔑 CLOSE LOGIN POPUP
        try:
            await page.wait_for_selector("button._2KpZ6l._2doB4z", timeout=5000)
            await page.click("button._2KpZ6l._2doB4z")
        except:
            pass

        # Wait for real product cards (not containers)
        await page.wait_for_selector("div._1AtVbE > div > div", timeout=15000)

        cards = await page.query_selector_all("div._1AtVbE > div > div")

        for card in cards:
            if len(results) >= 5:
                break

            try:
                title_el = await card.query_selector("div._4rR01T, a.s1Q9rs")
                price_el = await card.query_selector("div._30jeq3")
                img_el = await card.query_selector("img")
                link_el = await card.query_selector("a")

                if not (title_el and price_el and img_el and link_el):
                    continue

                results.append({
                    "title": (await title_el.inner_text()).strip(),
                    "price": (await price_el.inner_text()).strip(),
                    "image": await img_el.get_attribute("src"),
                    "link": "https://www.flipkart.com" + await link_el.get_attribute("href"),
                    "source": "Flipkart"
                })

            except Exception as e:
                print("Flipkart card error:", e)

    except Exception as e:
        print(f"Error scraping Flipkart: {e}")

    finally:
        await context.close()

    return results
