from scrapers.manager import search_products
import sys

# Force utf-8 for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

print("Testing synchronous search_products wrapper...")
try:
    results = search_products("test query")
    print("Success!")
    print(results)
except Exception as e:
    print(f"FAILED with error: {e}")
    import traceback
    traceback.print_exc()
