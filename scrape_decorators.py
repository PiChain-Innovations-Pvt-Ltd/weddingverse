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

            sersection = page.locator('.mui-1dziutq')
            serprice = page.locator('.mui-v1mhxp')
            
            services = {}

            for i in range(await sersection.count()):
                services[await sersection.nth(i).inner_text()] = await serprice.nth(i).inner_text()

            offsection = page.locator('.mui-n4csy7').nth(0).locator('.mui-2qqqnq')
            offerings = []
            for i in range(await offsection.count()):
                offerings.append(await offsection.nth(i).inner_text())
            
            policysection = page.locator('.mui-n4csy7').nth(1).locator('.mui-1hlxkic')
            policies = []
            for i in range(await policysection.count()):
                policies.append(await policysection.nth(i).inner_text())
            
            othersection = page.locator('.mui-7ynsxr')
            otherinfo = {}
            # otherinfo["Brand Used"] = await othersection.nth(0).inner_text()
            # otherinfo["is willing to travel to venue"] = await othersection.nth(1).inner_text().split()
            # otherinfo["is willing to travel other indian cities"] = await othersection.nth(1).inner_text()
            for i in range(await othersection.count()):
                otherText = await othersection.nth(i).inner_text()
                otherinfo[otherText.split('-')[0].strip()] = otherText.split('-')[1].strip()
            
            # Use the locator to get the `src` attribute
            image_urls_list = []
            image_elements = page.locator('.album-images')

            for i in range(await image_elements.count()):
                src_value = await image_elements.nth(i).get_attribute('src')
                image_urls_list.append(src_value)
            
            return{
                "Decorator Name": title,
                "Decorator Location": location,
                "Price": price,
                "Services": services,
                "Offerings": offerings,
                'Policies': policies,
                "Other Information": otherinfo,
                "Images": image_urls_list
            }
        except Exception as e:
            print(f"For URL: {url}")
            print(f"Failed while scraping the master data: {e}")
            return
            # return {
            #     "Artist Name": "",
            #     "Artist Location": "",
            #     "Price": "",
            #     "Services": "",
            #     "Offerings": "",
            #     'Policies': "",
            #     "Other Information": ""
            # }

def generateUrl(csv):
    try:
        print(f"Generating URLs for CSV: {csv}")
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv)
        planner_name = df['Decorator Name'].tolist()
        planner_locations = df['Decorator Location'].tolist()
        urls = []
        trimmed_loc = []
        for loc in planner_locations:
            trimmed_loc.append(loc.split(",")[1].strip())
        
        for location, name in zip(trimmed_loc, planner_name):
            urls.append("https://www.weddingbazaar.com/wedding-decorators/{}/{}".format(location.replace(' ', '-').lower(), name.replace(' ', '-').lower()))
        return urls
    except Exception as e:
        print(f"Failed while generating the URLs from CSV: {e}")
        return urls


async def csv_to_json(csv_file_loc="PLEASE PROVIDE CSV LOCATION"):

    try:
        generatedurls = generateUrl(csv_file_loc)
        final_json = []

        # You will have a list of all the makeup artists for particular locality
        for url in generatedurls:
            # Scrape data for one of that list
            datalist = await scrape_data(url)
            if datalist is not None:
                print(f"Successfully collected master data for {url}: {datalist}")
                final_json.append(datalist)
            else:
                print(f"Failed for URL {url}")
            # print(f"Scraped Data is {datalist}.")
        # This is a JSON of all the hotels (detailed) in a particular locality
        # Convert and write JSON object to file
        json_loc = csv_file_loc.replace("csv_loc_data", "json_loc_data").replace(".csv", ".json")
        print(f"Writing data to json: {json_loc}")
        with open(json_loc, "w") as outfile: 
            json.dump(final_json, outfile, ensure_ascii=False)
    except Exception as e:
        print(f"Failed while converting CSV to JSON: {e}")
        
# Function to scrape data from the page
async def scrape_data_to_csv(url):
    async with async_playwright() as p:
        try:
            print(f"Scraping pre-flight data for URL: {url}")
             # Launch a new browser instance
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Navigate to the specified URL
            await page.goto(url)

            # Extract the required information
            decorator_name = await page.locator('h3.mui-11hgfej').all_inner_texts()
            decorator_location = await page.locator("p.mui-1vzi93v").all_inner_texts()
            price = await page.locator("p.mui-17vjgne").all_inner_texts()
            print(decorator_name)

            # Close the browser
            await browser.close()

            return {
                "Decorator Name": decorator_name,
                "Decorator Location": decorator_location,
                "Price": price,

            }
        except Exception as e:
            print(f"Failed while writing generating CSV: {e}")
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
        print(f"Failed while write the data to CSV file: {e}")


async def main(csv_file_loc="PLEASE PROVIDE CSV LOCATION"):

    # result = json.dumps(await scrape_data("https://www.weddingbazaar.com/wedding-photographers/delhi/soulmate-films"), ensure_ascii=False)
    # print(result)
    # return result

    with open(f"weddingbazaar/decorators/txt_loc_list/split_file_{sys.argv[1]}.txt") as file_in:
        urls = []
        for line in file_in:
            urls.append(line)
    try:
        for url in urls:
            data = await scrape_data_to_csv(url)
            csv_file = "weddingbazaar/decorators/csv_loc_data/{}.csv".format(url[30:-2])
            print(f"Writing decorator to CSV file: {csv_file}")
            await write_to_csv(data, csv_file)
            await csv_to_json(csv_file)

        
    except Exception as e:
        print(f"Failed in the main function: {e}")


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())