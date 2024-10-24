import csv, time, sys
# from playwright.sync_api import sync_playwright
import asyncio
from playwright.async_api import async_playwright
import navigateInside as collect_recursive

# Function to scrape data from the page
async def scrape_data(url):
    async with async_playwright() as p:
        try:
            print(f"Scraping pre-flight data for URL: {url}")
             # Launch a new browser instance
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Navigate to the specified URL
            await page.goto(url)

            # Extract the required information
            venue_name = await page.locator('h3.mui-11hgfej').all_inner_texts()
            venue_location = await page.locator("p.mui-1vzi93v").all_inner_texts()
            price_per_plate = await page.locator("p.mui-17vjgne").all_inner_texts()
            # car_parking_facility = await page.locator("p.mui-1lrpt9r:nth-child(1), .mui-a622ns").all_inner_texts()
            # hall_capacity = await page.locator("p.mui-18jqfyr , .mui-1lrpt9r+ .mui-1lrpt9r .mui-a622ns").all_inner_texts()
            print(venue_name)

            # Close the browser
            await browser.close()

            return {
                "Venue Name": venue_name,
                "Venue Location": venue_location,
                "Price per Plate": price_per_plate,
                # "Car Parking Facility": car_parking_facility,
                # "Hall Capacity": hall_capacity
            }
        except Exception as e:
            print(f"Exception at scraping the data for csv: {e}")
            return {}
       




# Asynchronous function to write data to CSV
async def write_to_csv(data, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data.keys())  # Write the header

            # Get the maximum length of lists to ensure proper row creation
            max_length = max(len(data[key]) for key in data)

            # Write each row
            for i in range(max_length):
                row = [data[key][i] if i < len(data[key]) else '' for key in data]
                writer.writerow(row)
    except Exception as e:
        print(f"Exception occurred while write the data to CSV file: {e}")




async def main():
    with open(f"weddingbazaar/venues/txt_loc_list/split_file_{sys.argv[1]}.txt") as file_in:
        urls = []
        for line in file_in:
            urls.append(line)
    
    for url in urls:
        data = await scrape_data(url)
        csv_file = "weddingbazaar/venues/csv_loc_data/{}.csv".format(url[30:-2])
        print(f"Writing venue to CSV file: {csv_file}")
        await write_to_csv(data, csv_file)
        await collect_recursive.main(csv_file)

    print(f"--------SCRIPT COMPLETED--------")







    # # Write the extracted data to a CSV file
    # csv_file = "venue_data.csv"
    # await write_to_csv(data, csv_file)

    # print(f"Data extracted and saved to {csv_file}.")



# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

# # URL of the page to scrape
# url = "https://www.weddingbazaar.com/wedding-venues-in-bellandur--bangalore"

# # Scrape data from the page
# data = scrape_data(url)

# # Write the extracted data to a CSV file
# csv_file = "venue_data.csv"
# with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=data.keys())
#     writer.writeheader()
#     writer.writerow(data)

# print(f"Data extracted and saved to {csv_file}.")
