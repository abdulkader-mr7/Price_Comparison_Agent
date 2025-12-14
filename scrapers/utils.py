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
