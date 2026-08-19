from flask import Flask, render_template, request, jsonify
from scrapers.manager import search_products
from scrapers.utils import calculate_offers
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search_api():
    query = request.args.get('q')
    pincode = request.args.get('pincode')

    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        # Results from scrapers
        results = search_products(query)

        # Calculate offers and identify best buy
        all_products = []

        for platform in ['amazon', 'flipkart', 'meesho']:
            if platform in results and isinstance(results[platform], list):
                for product in results[platform]:
                    # Filter out error dicts just in case
                    if 'error' in product: continue

                    offers = calculate_offers(platform, product.get('price'), pincode)
                    product.update(offers)
                    product['best_buy'] = False # Default
                    if offers['effective_price'] > 0:
                        all_products.append(product)

        if all_products:
            # Find the minimum effective price
            best_product = min(all_products, key=lambda p: p['effective_price'])
            # We flag only one product across all platforms as the absolute best buy
            best_product['best_buy'] = True

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
