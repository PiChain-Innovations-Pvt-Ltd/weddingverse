import csv, time, json, sys
# from playwright.sync_api import sync_playwright
import asyncio
from playwright.async_api import async_playwright
import pandas as pd

# Function to scrape data from the page
async def scrape_data(url):
    async with async_playwright() as p:
        try:
            print(f"Scraping master data for URL: {url}")
            # Launch a new browser instance
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Navigate to the specified URL
            await page.goto(url)

            title = await page.locator('.mui-0').locator('.mui-hqp9xc').inner_text()
            location = await page.locator('.mui-0').locator('.mui-1fty1qh').inner_text()
            price = await page.locator('.mui-0').locator('.mui-9l3uo3').nth(2).inner_text()

            #Event area availability
            areaName = []
            indout = []
            seats = []
            floating = []
            combined_event_area = []
            parent_boxes_event_area = page.locator('.mui-1xjsxd4').locator('..')
            for i in range(await parent_boxes_event_area.count()):
                areaName.append(await parent_boxes_event_area.nth(i).locator('.mui-1xjsxd4').inner_text())
                indout.append(await parent_boxes_event_area.nth(i).locator('.mui-16b68b1').nth(0).inner_text())
                seats.append(await parent_boxes_event_area.nth(i).locator('.mui-16b68b1').nth(1).inner_text())
                floating.append(await parent_boxes_event_area.nth(i).locator('.mui-16b68b1').nth(2).inner_text())
            
            for aname, iot, st, fl in zip(areaName, indout,seats,floating):
                d = {
                    "event_area_name": aname,
                    "seating": iot,
                    "no_of_seats": st,
                    "floating_capacity": fl
                }
                combined_event_area.append(d)


            
            # Services locator
            services_offered = page.locator('.mui-15hpam0')
            veg = await services_offered.nth(0).locator('.mui-v1mhxp').inner_text()
            nonveg = await services_offered.nth(0).locator('.mui-v1mhxp').inner_text()
            serv = {
                veg: veg,
                nonveg: nonveg
            }
            
            # Amenities
            amenities = []
            amn = page.locator('.mui-2qqqnq')
            for i in range(await amn.count()):
                amenities.append(await amn.nth(i).inner_text())
            
            # Other information
            other_info = []
            inf = page.locator('.mui-7ynsxr')
            for i in range(await inf.count()):
                d = {}
                text = await inf.nth(i).inner_text()
                text = text.split('-')
                text2 = [t.strip() for t in text]
                d[text2[0]] = text2[1]
                other_info.append(d)        

            await browser.close()

            return {
                "Venue Name": title,
                "Venue Location": location,
                "Price per Plate": price,
                "Event Areas": combined_event_area,
                "Services": serv,
                "Amenities": amenities,
                "Other info": other_info
            }
        except Exception as e:
            print(f"For URL: {url}")
            print(f"Exception occurred while scraping the master data: {e}")
            return {
                "Venue Name": "",
                "Venue Location": "",
                "Price per Plate": "",
                "Event Areas": "",
                "Services": "",
                "Amenities": "",
                "Other info": ""
            }
        


def generateUrl(csv):
    try:
        print(f"Generating URLs for CSV: {csv}")
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv)
        venue_name = df['Venue Name'].tolist()
        venue_locations = df['Venue Location'].tolist()
        urls = []
        trimmed_loc = []
        for loc in venue_locations:
            trimmed_loc.append(loc.split(",")[1].strip())
        
        for location, name in zip(trimmed_loc, venue_name):
            urls.append("https://www.weddingbazaar.com/wedding-venues/{}/{}".format(location.replace(' ', '-').lower(), name.replace(' ', '-').lower()))
        return urls
    except Exception as e:
        print(f"Exception occured while generating the URLs from CSV: {e}")
        return urls


async def main(csv_file_loc="PLEASE PROVIDE CSV LOCATION"):

    try:
        # URL of the page to scrape
        url = "https://www.weddingbazaar.com/wedding-venues-in-bellandur--bangalore"

        # Scrape data from the page
        # data = await scrape_data(url)
        # generatedurls = generateUrl("data-venue/wedding-venues-in-aerocity--delh.csv")
        generatedurls = generateUrl(csv_file_loc)
        final_json = []

        # You will have a list of all the hotels for particular locality
        for url in generatedurls:
            # Scrape data for one of that list
            datalist = await scrape_data(url)
            print(f"Successfully collected master data for {url}: {datalist}")
            final_json.append(datalist)
            # print(f"Page title is {datalist}.")
        # This is a JSON of all the hotels (detailed) in a particular locality
        # Convert and write JSON object to file
        json_loc = csv_file_loc.replace("csv_loc_data", "json_loc_data").replace(".csv", ".json")
        print(f"Writing data to json: {json_loc}")
        with open(json_loc, "w") as outfile: 
            json.dump(final_json, outfile)
    except Exception as e:
        print(f"Exception occurred while calling the inner function: {e}")


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())