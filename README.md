# WeddingVerse Data Scraper

This project is a web scraper designed to collect data from wedding-related websites.  It uses Python and asynchronous programming for efficient data retrieval.

## Project Structure

The project is organized into several key components:

* **Scrapers:**
    * `scrape_photographers.py`: Scrapes data for photographers.
    * `scrape_makeup.py`: Scrapes data for makeup artists.
    * `scrape_planners.py`: Scrapes data for wedding planners.
    * `scrape_venues.py`: Scrapes data for wedding venues.
    * `scrape_searates.py`: Scrapes sea rates data (purpose unclear without further investigation).
    * `scrape_venue_single_url.py`: Scrapes data from a single venue URL.

* **Utilities:**
    * `utilities/combine_json.py`: Combines JSON files.
    * `utilities/combine_csv.py`: Combines CSV files.
    * `utilities/count_json_objects.py`: Counts objects in JSON files.
    * `utilities/getUrls.py`: (Purpose unclear without further investigation).
    * `utilities/splitFile.py`: Splits files.

* **Decorators:**
    * `scrape_decorators.py`: Contains reusable decorators for scraping tasks.

* **Authentication:**
    * `ssoLogin.py`: Handles authentication (likely using OAuth2).

* **Orchestration:**
    * `run_scrape.sh`: A bash script that runs the scraping tasks.

* **Archived Data:**
    * `archived/`: Contains archived scraped data.

## Data Flow

1. The `run_scrape.sh` script iterates and runs the `scrape_photographers.py` script multiple times.  (Further investigation needed to determine the exact data flow for other scrapers).
2. Each scraper retrieves data from target websites.
3. Data is processed and saved as JSON or CSV files.
4. Utility scripts combine and process the collected data.

## Usage

To run the scraper, execute the `run_scrape.sh` script.  This script will run the individual scraper scripts in the background.

## Further Development

* Investigate the purpose of `utilities/getUrls.py`.
* Clarify the data flow for scrapers other than `scrape_photographers.py`.
* Add more detailed documentation for each script.
* Implement error handling and logging.
