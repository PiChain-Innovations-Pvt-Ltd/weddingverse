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
            venue_name = await page.locator('#tracking_system_root').inner_text()
            
            print(venue_name)

            # Close the browser
            await browser.close()

            return {
                "Venue Name": venue_name
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
    data = await scrape_data("https://www.searates.com/container/tracking/?number=CNICB24012820&type=BL&sealine=REGU")
   
    
    # for url in urls:
    #     data = await scrape_data(url)
    #     csv_file = "weddingbazaar/venues/csv_loc_data/{}.csv".format(url[30:-2])
    #     print(f"Writing venue to CSV file: {csv_file}")
    #     await write_to_csv(data, csv_file)
    #     await collect_recursive.main(csv_file)

    print(f"--------SCRIPT COMPLETED--------")



# Run the main function
# if __name__ == "__main__":
#     pass
#     # asyncio.run(main())





# import requests
# import json

# # Use the Tor proxy for requests
# proxies = {
#     'http': 'socks5h://127.0.0.1:9050',
#     'https': 'socks5h://127.0.0.1:9050'
# }

# url = "https://g.weddingbazaar.com/"

# payload = "{\"query\":\"query _count($where: Vendor_listingWhereInput, $findFirstCategoryWhere2: CategoryWhereInput) {\\n  findFirstCategory(where: $findFirstCategoryWhere2) {\\n    _count {\\n      vendor_listing(where: $where)\\n      __typename\\n    }\\n    __typename\\n  }\\n}\",\"variables\":{\"findFirstCategoryWhere2\":{\"slug\":{\"equals\":\"wedding-decorators\"}},\"where\":{\"AND\":[{\"status\":{\"equals\":1}}]}}}"
# headers = {
#   'accept': '*/*',
#   'accept-language': 'en-US,en;q=0.9',
#   'content-type': 'application/json',
#   'origin': 'https://www.weddingbazaar.com',
#   'priority': 'u=1, i',
#   'referer': 'https://www.weddingbazaar.com/',
#   'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
#   'sec-ch-ua-mobile': '?0',
#   'sec-ch-ua-platform': '"Windows"',
#   'sec-fetch-dest': 'empty',
#   'sec-fetch-mode': 'cors',
#   'sec-fetch-site': 'same-site',
#   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
# }

# response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)

# print(response.text)




import requests
# bil_of_lading = "CNICB24012820"
bil_of_lading = "EMCU5358951"

url = f"https://www.searates.com/tracking-system/reverse/tracking?route=true&last_successful=false&number={bil_of_lading}&sealine=REGU&type=BL"

# Use the Tor proxy for requests
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

payload = {}
headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9',
  'priority': 'u=1, i',
  'referer': 'https://www.searates.com/container/tracking/?number=CNICB24012820&type=BL&sealine=REGU',
  'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'traceparent': '00-49bfe06a97394521ac82ce9056a22c00-35c1e65c47a3f974-01',
  'tracestate': '2914910@nr=0-1-3461589-388581761-35c1e65c47a3f974----1727326320689',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
#   'x-newrelic-id': 'VwIBUFNbARADXFlRAQMBX1M=',
  'x-referer': 'https://www.searates.com/',
#   'Cookie': 'PHPSESSID=r6ub482buthkm1reldngvp6lfg; __cf_bm=FgKPUo8ATU1hRWA6tuqiWwayqOn3BX452ZwevYgiTcA-1727330383-1.0.1.1-1TgQi_XduNVN8yUuw3n23LiIyIqimBhR0IwyU3HO4yTiHcTDgtDXpr1PTB0T0xwv6CNY_JBlIRrxGL7gu7Kmxw'
}

response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)

print(response.text)




