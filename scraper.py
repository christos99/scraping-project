import logging
import re
import string
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def scrape_data(keywords, price_low, price_high, excluded_keyword, output_file, update_progress=None):
    # Set up Chrome options (headless mode is optional)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize WebDriver
    logging.info('Initializing WebDriver.')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Sanitize keywords
        keywords_str = '_'.join(keywords)
        valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
        sanitized_keywords = ''.join(c for c in keywords_str if c in valid_chars).lower()

        # Construct the search query
        search_query = '%20'.join(keywords)
        url = f'https://www.insomnia.gr/classifieds/search/?&q={search_query}&type=classifieds_advert&price_low={price_low}&price_high={price_high}&nodes=14&sortby=priceHigh'
        
        driver.get(url)
        logging.info('Webpage loaded successfully.')
        driver.implicitly_wait(10)

        # Initialize data list
        data = []

        # Loop through pages
        page_number = 1
        while True:
            logging.info(f'Processing page {page_number}')
            ads = driver.find_elements(By.CSS_SELECTOR, 'li.ipsStreamItem[data-role="activityItem"]')
            
            if not ads:
                logging.info('No ads found on this page.')
                break
            
            for ad in ads:
                try:
                    # Extract ad details
                    title_element = ad.find_element(By.CSS_SELECTOR, 'span.ipsContained.ipsType_break > a[data-linktype="link"]')
                    title = title_element.get_attribute('textContent').strip()
                    link = title_element.get_attribute('href')

                    if all(keyword.lower() in title.lower() for keyword in keywords) and (not excluded_keyword or excluded_keyword.lower() not in title.lower()):
                        price_element = ad.find_element(By.CSS_SELECTOR, 'span.ipsStream_price')
                        price_text = price_element.text.strip()

                        # Convert price
                        price_numeric = re.sub(r'[^\d.,]', '', price_text).replace('.', '').replace(',', '.')
                        price_value = float(price_numeric)

                        data.append({
                            'Page': page_number,
                            'Title': title,
                            'Price (€)': price_value,
                            'Link': link,
                        })
                except Exception as e:
                    logging.error(f'Error processing ad: {e}')

            # Update progress
            if update_progress:
                update_progress(page_number)

            # Navigate to next page
            try:
                next_button_li = driver.find_element(By.CSS_SELECTOR, 'li.ipsPagination_next')
                if 'ipsPagination_inactive' in next_button_li.get_attribute('class'):
                    break
                next_button = next_button_li.find_element(By.TAG_NAME, 'a')
                driver.get(next_button.get_attribute('href'))
                page_number += 1
            except NoSuchElementException:
                break

        # Save to Excel
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
        logging.info(f'Data saved to {output_file}')
        return data

    finally:
        driver.quit()