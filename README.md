# WeddingVerse Data Scraper

This project is a web scraper designed to collect data from wedding-related websites.  It uses Python and asynchronous programming for efficient data retrieval.

## Project Structure

The project is organized into several key components:

* **Scrapers:**
    * `scrape_photographers.py`: Scrapes data for photographers.
    * `scrape_makeup.py`: Scrapes data for makeup artists.
    * `scrape_planners.py`: Scrapes data for wedding planners.
    * `scrape_venues.py`: Scrapes data for wedding venues.
    * `scrape_venue_single_url.py`: Scrapes data from a single venue URL.

* **Utilities:**
    * `utilities/combine_json.py`: Combines JSON files.
    * `utilities/combine_csv.py`: Combines CSV files.
    * `utilities/count_json_objects.py`: Counts objects in JSON files.
    * `utilities/getUrls.py`: It generates URLs for web scraping, given a single XML source.
    * `utilities/splitFile.py`: Splits files containing URLs for ship tracking.

* **Decorators:**
    * `scrape_decorators.py`: Contains reusable decorators for scraping tasks.

* **Authentication:**
    * `ssoLogin.py`: Handles authentication. Contains backend APIs for OAuth2 authentication.

* **Orchestration:**
    * `run_scrape.sh`: A bash script that runs the scraping tasks.

* **Archived Data:**
    * `archived/`: Contains archived scraped data.

## Data Flow

1. The `run_scrape.sh` script iterates and runs the `scrape_<object>.py` script parallally. It collects all the URLs from a single URL. All the URLs are stored in separate files, number of files and batches are determined on the basis of CPU and RAM of runner machine. On running the script, all 100-200 instances will run concurrently, launching individual browsers in an asynchronous fashion.
> [!CAUTION]
> This script will use all of your RAM and CPU, and hang the system if the concurrency is not determined carfefully.
2. Each scraper retrieves data from target websites.
3. Data is processed and saved as JSON or CSV files.
4. Utility scripts combine and process the collected data.

## Usage

To run the scraper, execute the `run_scrape.sh` script.  This script will run the individual scraper scripts in the background.

## Further Development

* Bypassing using proxy and bot blockers
