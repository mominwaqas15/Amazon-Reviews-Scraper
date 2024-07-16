import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

second_first_iteration = True

def convert_to_desired_format(row):
    review_text = row['review_text']
    rating = row['rating'].split()[0]  # Extracting the numerical rating
    
    return {
        'Review': review_text,
        'Rating': rating
    }

# Function to get the reviews from a single page
def get_reviews_and_ratings_from_page(soup):
    reviews_data = []
    review_blocks = soup.find_all('div', {'data-hook': 'review'})
    
    for block in review_blocks:
        review_text = block.find('span', {'data-hook': 'review-body'}).text.strip()
        
        # Extracting the rating
        rating_element = block.find('i', {'data-hook': 'review-star-rating'})
        if rating_element:
            rating_text = rating_element.find('span', {'class': 'a-icon-alt'}).text.strip()
        else:
            rating_text = 'Rating not found'
        
        reviews_data.append({
            'review_text': review_text,
            'rating': rating_text
        })
    
    return reviews_data

# Function to handle initial pop-up and scrape all reviews using Selenium for pagination
def scrape_all_reviews_with_selenium(start_url_template, star_levels, max_pages_per_star):
    # Set up Selenium WebDriver (replace with your WebDriver path)
    chromedriver_path = r'C:\Users\momin\Desktop\chromedriver-win64\chromedriver.exe'

    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=service, options=options)

    all_reviews = []

    for star in star_levels:
        start_url = start_url_template.format(star)
        print(f"Scraping {star.replace('_', ' ')} reviews...")

        # Navigate to the start URL
        driver.get(start_url)

        try:
            # Handle initial pop-up or consent banner
            decline_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'sp-cc-rejectall-link')))
            decline_button.click()
        except:
            print("No initial pop-up found or unable to click Decline button.")

        first_iteration = True
        page_count = 0

        while page_count < max_pages_per_star:
            # Wait for the reviews to load
            time.sleep(5)
            
            # Get page source and create BeautifulSoup object
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            reviews = get_reviews_and_ratings_from_page(soup)
            
            # Append reviews to the list
            all_reviews.extend(reviews)
            print(f"Scraped {len(reviews)} reviews. Total reviews: {len(all_reviews)}")
            
            # Find the next button and click it if it exists
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'li.a-last a')
                if first_iteration:
                    next_button.click()  # Click the next button only on the first page
                    time.sleep(3)  # Add a short delay to allow the next page to load

                    # Check for sign-in prompt after clicking next
                    handle_sign_in(driver)

                    first_iteration = False
                else:
                    next_button.click()
                    time.sleep(3)  # Add a short delay to allow the next page to load
            except:
                print("No more pages to scrape.")
                break

            page_count += 1

    # Close the WebDriver
    driver.quit()

    return all_reviews

# Function to handle sign-in process if prompted
def handle_sign_in(driver):
    global second_first_iteration
    try:
        # Check if sign-in page appears
        if second_first_iteration:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]')))

            # Enter email and continue
            email_input = driver.find_element(By.ID, 'ap_email')
            email_input.send_keys("mominwaqas15@gmail.com")  # Replace with your email
            continue_button = driver.find_element(By.ID, 'continue')
            continue_button.click()

            # Enter password and sign in
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'ap_password')))
            password_input = driver.find_element(By.ID, 'ap_password')
            password_input.send_keys("M4321786W")  # Replace with your password
            sign_in_button = driver.find_element(By.ID, 'signInSubmit')
            sign_in_button.click()

            # Wait after sign-in for 15 seconds
            time.sleep(10)
            second_first_iteration = False

    except Exception as e:
            print(f"Sign-in process error: {e}")

# URLs for each star level
base_url_template = "https://www.amazon.co.uk/Martins-Chocolatier-Signature-Collection-Chocolate/product-reviews/B08DRKZ7FJ/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&filterByStar={}&pageNumber=1"
star_levels = ["five_star", "four_star", "three_star", "two_star", "one_star"]
max_pages_per_star = 10

all_reviews = scrape_all_reviews_with_selenium(base_url_template, star_levels, max_pages_per_star)

converted_data = [convert_to_desired_format(row) for row in all_reviews]

df = pd.DataFrame(converted_data)

# Output filename
output_filename = 'product_reviews_all_star_levels.xlsx'

# Save to Excel
df.to_excel(output_filename, index=False)

print(f"Saved all reviews to {output_filename}")