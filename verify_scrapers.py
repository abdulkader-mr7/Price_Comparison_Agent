import asyncio
from scrapers.manager import search_products_async
import json
import sys

# Force utf-8 for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("Testing scrapers with query: 'Samsung Galaxy M34'...")
    results = await search_products_async("Samsung Galaxy M34")
    
    with open('verify_result.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("Results written to verify_result.json")

if __name__ == "__main__":
    asyncio.run(main())
