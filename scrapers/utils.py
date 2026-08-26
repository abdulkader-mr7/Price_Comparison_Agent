import random

# Static list of modern user agents to avoid dependency issues
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
]

async def get_stealth_context(browser):
    """
    Creates a browser context with stealth modifications:
    - Random User Agent
    - Masked navigator.webdriver
    - Random viewport
    - Extra headers
    """
    user_agent = random.choice(USER_AGENTS)
    
    # Random viewport
    width = random.randint(1366, 1920)
    height = random.randint(768, 1080)
    
    context = await browser.new_context(
        user_agent=user_agent,
        viewport={'width': width, 'height': height},
        java_script_enabled=True,
        locale='en-US',
        timezone_id='Asia/Kolkata' # Localized for better results
    )
    
    # Mask automation flags
    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        
        // Mock plugins to look like Chrome
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        
        // Add random mouse movements later if needed
    """)
    
    return context


def parse_price(price_str):
    """Convert price string like '₹1,299' or '1299' to float."""
    if not price_str:
        return 0.0
    # Remove currency symbols and commas
    clean_price = price_str.replace('₹', '').replace(',', '').strip()
    try:
        return float(clean_price)
    except ValueError:
        return 0.0

def calculate_offers(platform, price_str, pincode=None):
    """
    Simulates delivery costs and card discounts based on platform and price.
    Returns dictionary with simulated data and the effective price.
    """
    base_price = parse_price(price_str)

    if base_price == 0.0:
        return {
            'delivery_cost': 0,
            'discount': 0,
            'effective_price': 0,
            'delivery_desc': 'Unknown',
            'discount_desc': 'None'
        }

    # Default values
    delivery_cost = 0
    discount = 0
    delivery_desc = "Free Delivery"
    discount_desc = "No Offers"

    # Simulate delivery costs based on platform and PIN code (mock logic)
    if platform.lower() == 'amazon':
        if base_price < 500:
            delivery_cost = 40
            delivery_desc = "+ ₹40 Delivery"

        # Amazon card discount (e.g. 10% off ICICI/SBI up to max 1500)
        if base_price > 2000:
            discount = min(base_price * 0.10, 1500)
            discount_desc = f"Includes ₹{int(discount)} Bank Discount (ICICI/SBI)"

    elif platform.lower() == 'flipkart':
        if base_price < 500:
            delivery_cost = 40
            delivery_desc = "+ ₹40 Delivery"

        # Flipkart card discount (e.g. 5% cashback Axis Bank)
        discount = min(base_price * 0.05, 1000)
        discount_desc = f"Includes ₹{int(discount)} Cashback (Axis Bank)"

    elif platform.lower() == 'meesho':
        # Meesho is usually free delivery
        delivery_cost = 0
        delivery_desc = "Free Delivery"
        # Often flat discounts
        if base_price > 1000:
            discount = 100
            discount_desc = "Flat ₹100 Off"

    # Some simulated PIN code logic: If it starts with certain digits, add extra shipping for remote areas
    if pincode and len(pincode) == 6:
        # Example: Let's assume North East PIN codes start with 79
        if pincode.startswith('79'):
            delivery_cost += 50
            delivery_desc = f"+ ₹{int(delivery_cost)} Delivery to {pincode}"

    effective_price = base_price + delivery_cost - discount

    return {
        'delivery_cost': int(delivery_cost),
        'discount': int(discount),
        'effective_price': int(effective_price),
        'delivery_desc': delivery_desc,
        'discount_desc': discount_desc
    }
