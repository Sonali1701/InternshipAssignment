import time
import pandas as pd
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver for Microsoft Edge
def init_driver():
    # Automatically download and install the correct version of chromedriver (compatible with Edge)
    chromedriver_autoinstaller.install()

    # Initialize Edge with specific options
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")  # Set a user-agent to avoid detection

    # Set the Edge WebDriver path
    driver = webdriver.Edge(options=options)
    return driver

# Scrape the Amazon "soft toys" products
def scrape_amazon_soft_toys():
    driver = init_driver()
    url = "https://www.amazon.in/s?k=soft+toys"
    driver.get(url)

    # Wait for the page to load completely
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))

    # Scroll to load all products
    scroll_count = 5  # Adjust this value based on how much you want to scroll
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait a bit before scrolling again

    product_data = []

    # Find all products (sponsored or not)
    products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
    print(f"Found {len(products)} total products")

    for product in products:
        try:
            # Check if the product is sponsored
            is_sponsored = product.find_elements(By.XPATH, ".//span[contains(text(), 'Sponsored')]")
            if not is_sponsored:
                continue  # Skip non-sponsored products

            # Extract product details with fallback to handle missing elements
            title = product.find_element(By.XPATH, ".//h2//span").text
            brand = product.find_element(By.XPATH, ".//h5").text if product.find_elements(By.XPATH,
                                                                                          ".//h5") else "Unknown"

            # Handle missing rating (Some products might not have a rating)
            try:
                rating = product.find_element(By.XPATH, ".//span[@class='a-icon-alt']").text.split()[0]
            except:
                rating = "No rating"

            # Handle missing reviews
            try:
                reviews = product.find_element(By.XPATH, ".//span[@class='a-size-base s-underline-text']").text.replace(
                    ",", "")
            except:
                reviews = "No reviews"

            # Handle missing price
            try:
                price_whole = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text.replace(",", "")
                price_frac = product.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text
                price = f"{price_whole}.{price_frac}"
            except:
                price = "No price"

            # Handle missing image
            try:
                image = product.find_element(By.XPATH, ".//img").get_attribute("src")
            except:
                image = "No image"

            # Handle missing product URL
            try:
                url = product.find_element(By.XPATH, ".//a[@class='a-link-normal s-no-outline']").get_attribute("href")
            except:
                url = "No URL"

            # Debugging log to check extracted data
            print(f"Extracted product: {title}, {rating}, {reviews}, {price}, {image}, {url}")

            # Append product data
            product_data.append({
                "Title": title,
                "Brand": brand,
                "Rating": rating,
                "Reviews": reviews,
                "Price": price,
                "Image URL": image,
                "Product URL": url
            })
        except Exception as e:
            print(f"Error extracting product: {e}")
            continue

    driver.quit()

    # Save the scraped data to a CSV file
    df = pd.DataFrame(product_data)
    df.to_csv("soft_toys_sponsored.csv", index=False)
    print(f"\nScraped and saved {len(df)} sponsored products to soft_toys_sponsored.csv")

if __name__ == "__main__":
    scrape_amazon_soft_toys()
