import os
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

if not os.path.isdir("data"):
    os.mkdir("data")

# Set up Selenium
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # run in background
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
# Disable automation flags that indicate bot activity
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# Disable webdriver property
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
driver.get("https://www.amazon.in/s?k=soft+toys")

# Scroll to load dynamic content
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

soup = BeautifulSoup(driver.page_source, 'html.parser')
#driver.quit()

pages = int(soup.find('span', class_='s-pagination-item s-pagination-disabled').text.strip())
sponsored_data = []

driver.execute_script("window.open('');")

for i in range(pages):
    if i > 0:
        driver.switch_to.window(driver.window_handles[0])
        driver.get(f"https://www.amazon.in/s?k=soft+toys&page={i+1}")
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # All product containers
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    print(f"Found {len(products)} products.")

    # Extract sponsored products only
    sponsored_product_links = []

    for product in products:
        if product.find('span', string='Sponsored'):
            product_link = product.find('a', class_='a-link-normal s-no-outline')
            sponsored_product_links.append(f"https://www.amazon.in{product_link['href']}")

    driver.switch_to.window(driver.window_handles[1])

    for product_url in sponsored_product_links:
        driver.get(product_url)
        time.sleep(2)  # Wait for the page to load

        # Parse the product page
        product_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract product details
        title_tag = product_soup.find('span', class_='a-size-large product-title-word-break')
        title = title_tag.text.strip() if title_tag else "N/A"

        brand_tag = product_soup.find('a', id='bylineInfo')
        brand = brand_tag.text.strip() if brand_tag else "Unknown"

        if brand.startswith("Visit"):
            brand = brand.replace("Visit the ", "")
            brand = brand.replace(" Store", "")
        elif brand.startswith("Brand"):
            brand = brand.replace("Brand: ", "")

        rating_tag = product_soup.find('span', class_='a-icon-alt')
        rating = rating_tag.text.split()[0]
        reviews = None

        if rating=="Previous":
            rating = None
        else:
            review_tag = product_soup.find('span', {'class': 'a-size-base', 'id': 'acrCustomerReviewText'})
            reviews = review_tag.text.split()[0].replace(",", "") if review_tag else None

        price_tag = product_soup.find('span', class_='a-price-whole')
        price = price_tag.text.replace(",", "") if price_tag else None

        img_tag = product_soup.find('img', class_='a-dynamic-image a-stretch-vertical')
        img_url = img_tag['src'] if img_tag else None
        if img_url == None:
            img_tag = product_soup.find('img', class_='a-dynamic-image a-stretch-horizontal')
            img_url = img_tag['src'] if img_tag else None

        sponsored_data.append({
            'Title': title,
            'Brand': brand,
            'Rating': rating,
            'Reviews': reviews,
            'Selling Price': price,
            'Image URL': img_url,
            'Product URL': product_url
        })

# Save to CSV
df = pd.DataFrame(sponsored_data)
df.to_csv("data/sponsored_soft_toys.csv", index=False)

print("Scraping done. Data saved to sponsored_soft_toys.csv")
# time.sleep(1000)

