import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import os
import time
import urllib.parse
import re
import random

def setup_driver():
    """Setup undetected Chrome driver with options"""
    options = uc.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    
    # Random user agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    
    try:
        driver = uc.Chrome(options=options)
        driver.set_page_load_timeout(60)  # Increased timeout
        # Add random delay to seem more human-like
        time.sleep(random.uniform(2, 4))
        return driver
    except Exception as e:
        print(f"Error setting up driver: {str(e)}")
        raise

def random_sleep():
    """Add random delay between actions"""
    time.sleep(random.uniform(2, 5))

def scroll_page(driver):
    """Scroll page with random pauses"""
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    current_position = 0
    scroll_step = random.randint(300, 700)  # Random scroll amount
    
    while current_position < total_height:
        current_position += scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(random.uniform(0.5, 1.5))  # Random pause between scrolls

def create_download_dir():
    """Create directory for downloaded images if it doesn't exist"""
    if not os.path.exists('shopbop_images'):
        os.makedirs('shopbop_images')

def sanitize_filename(filename):
    """Clean filename to be valid for all operating systems"""
    # Remove invalid characters and price information
    filename = re.sub(r'\$\d+\.?\d*', '', filename)  # Remove price
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
    # Limit length and remove trailing underscores
    return filename[:100].strip('_')

def download_image(url, filename):
    """Download image from URL and save it"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.shopbop.com/'
        }
        response = requests.get(url, stream=True, headers=headers)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Successfully downloaded: {filename}")
        else:
            print(f"Failed to download: {url} (Status code: {response.status_code})")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def get_product_info(product_element):
    """Extract product name from Shopbop's product element"""
    try:
        product_name = ""
        # Try to find the product name from the link text
        product_link = product_element.find('a', class_='product-title')
        if product_link:
            product_name = product_link.text.strip()
        
        if not product_name:
            # Try to find product name from any text content
            product_name = product_element.get_text().strip()
        
        # Clean up the product name
        product_name = re.sub(r'\s+', ' ', product_name)  # Replace multiple spaces
        product_name = product_name.replace('Not hearted', '')  # Remove "Not hearted" text
        
        if not product_name:
            product_name = f"shopbop_product_{int(time.time())}"
            
        return sanitize_filename(product_name)
    except Exception as e:
        print(f"Error getting product name: {str(e)}")
        return f"shopbop_product_{int(time.time())}"

def scrape_page(driver, page_number, total_images_downloaded):
    """Scrape images from a single Shopbop page"""
    try:
        # First load the base URL
        if page_number == 1:
            url = "https://www.shopbop.com/clothing-sweaters-knits/br/v=1/13317.htm"
            driver.get(url)
            random_sleep()
        else:
            # For subsequent pages, click the "Load More" button
            try:
                load_more = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.load-more-button"))
                )
                # Scroll to the button
                driver.execute_script("arguments[0].scrollIntoView(true);", load_more)
                random_sleep()
                load_more.click()
                print(f"Clicked 'Load More' button for page {page_number}")
                random_sleep()
            except Exception as e:
                print(f"Could not find 'Load More' button: {str(e)}")
                return total_images_downloaded
        
        # Wait for content to load
        try:
            # Try multiple selectors
            selectors = [
                (By.CSS_SELECTOR, "div.product-grid"),
                (By.CSS_SELECTOR, "div.product-tile"),
                (By.CSS_SELECTOR, "[data-testid='product-grid']"),
                (By.CSS_SELECTOR, ".s-product-grid")
            ]
            
            for selector in selectors:
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located(selector)
                    )
                    print(f"Found products using selector: {selector}")
                    break
                except:
                    continue
        except Exception as e:
            print(f"Warning: Timeout waiting for products on page {page_number}")
        
        # Scroll with random pauses
        scroll_page(driver)
        
        # Parse the page
        print("Parsing page content...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Try multiple selectors to find products
        products = []
        selectors = [
            "product-tile",
            "product",
            "s-product-card",
            "s-result-item"
        ]
        
        for selector in selectors:
            products = soup.find_all(class_=selector)
            if products:
                print(f"Found {len(products)} products with selector '{selector}'")
                break
        
        if not products:
            print("No products found with standard selectors, trying alternative approach...")
            products = soup.find_all('div', {'data-testid': True})
        
        print(f"Found {len(products)} products on page {page_number}")
        
        # Process only the new products (skip previously processed ones)
        start_index = (page_number - 1) * 100
        end_index = page_number * 100
        products_to_process = products[start_index:end_index]
        
        print(f"Processing products {start_index} to {end_index}")
        
        for product in products_to_process:
            # Try multiple image selectors
            img = None
            img_selectors = ['product-image', 'productImage', 'img']
            for selector in img_selectors:
                img = product.find('img', class_=selector) or product.find('img')
                if img:
                    break
            
            if not img:
                continue
            
            src = img.get('src') or img.get('data-src') or img.get('srcset')
            if not src:
                continue
            
            if isinstance(src, str) and ('icon' in src.lower() or 'logo' in src.lower() or '.svg' in src.lower()):
                continue
            
            # Get product name
            product_name = get_product_info(product)
            filename = os.path.join('shopbop_images', f'{product_name}_page{page_number}.jpg')
            
            # Ensure unique filename
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(filename):
                filename = f"{base}_{counter}{ext}"
                counter += 1
            
            # Download image
            download_image(src, filename)
            total_images_downloaded += 1
            random_sleep()
        
        return total_images_downloaded
            
    except Exception as e:
        print(f"An error occurred on page {page_number}: {str(e)}")
        return total_images_downloaded

def scrape_shopbop():
    """Main function to scrape images from Shopbop"""
    driver = setup_driver()
    create_download_dir()
    total_pages = 5  # First 5 pages
    total_images_downloaded = 0
    
    try:
        for page in range(1, total_pages + 1):
            total_images_downloaded = scrape_page(driver, page, total_images_downloaded)
            
            # Add a delay between pages to be respectful to the server
            if page < total_pages:
                time.sleep(5)  # Increased delay between pages
                
        print(f"\nScraping completed! Total images downloaded: {total_images_downloaded}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_shopbop() 