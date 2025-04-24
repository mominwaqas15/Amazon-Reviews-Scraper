# Amazon Reviews Scraper

This project is designed to scrape product reviews from Amazon for a specified product, handle pagination, filter by star rating, and combine the scraped data into a single Excel file.

## Project Structure

The project consists of the following Python scripts:
1. `scrape_reviews.py`: Scrapes reviews from the initial URL and saves them to an Excel file.
2. `scrape_reviews_at_star_level.py`: Scrapes reviews filtered by star levels and saves them to an Excel file.
3. `combiner.py`: Combines the two Excel files into a single Excel file.

## Setup

### Prerequisites

- Python 3.6 or higher
- Google Chrome
- ChromeDriver compatible with your Chrome version
- Required Python libraries: `selenium`, `pandas`, `beautifulsoup4`, `openpyxl`

### Installation

1. Clone the repository:
   `git clone https://github.com/mominwaqas15/amazon-reviews-scraper.git`
   `cd amazon-reviews-scraper`

2. Install the required Python packages:
   `pip install -r requirements.txt`

3. Download ChromeDriver and place it in a known directory. Update the `chromedriver_path` variable in `scrape_reviews.py` and `scrape_reviews_at_star_level.py` with the path to your ChromeDriver.

## Usage

### Scrape Reviews from Initial URL

To scrape reviews from the initial URL and save them to an Excel file, run:
`python scrape_reviews.py`
This will generate a file named `product.xlsx` containing the scraped reviews.

### Scrape Reviews by Star Levels

To scrape reviews filtered by different star levels and save them to an Excel file, run:
`python scrape_reviews_at_star_level.py`
This will generate a file named `product_reviews_all_star_levels.xlsx` containing the scraped reviews.

### Combine Excel Files

To combine the two Excel files (`product.xlsx` and `product_reviews_all_star_levels.xlsx`) into a single file, run:
`python combiner.py`
This will generate a file named `combined.xlsx` containing the combined reviews.
