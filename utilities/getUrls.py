import xml.etree.ElementTree as ET
import requests
import xml.etree.ElementTree as ET

# URL to fetch the XML data
url = 'https://www.weddingbazaar.com/sitemap/ListingScreenLocalityWise/LocalityWiseVendorListingPageForWEDDING-DECORATORS.xml'

# Fetch the XML data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    xml_data = response.text
    
    # Parse the XML
    root = ET.fromstring(xml_data)

    # Define the namespace
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    # Extract URLs
    urls = [url.find('ns:loc', namespace).text for url in root.findall('ns:url', namespace)]

    # Print the extracted URLs
    for url in urls:
        print(url)
else:
    print(f"Failed to retrieve XML data: {response.status_code}")


# Sample XML data
# xml_data = 

# Parse the XML
root = ET.fromstring(xml_data)

# Define the namespace
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Extract URLs
urls = [url.find('ns:loc', namespace).text for url in root.findall('ns:url', namespace)]

# Print the extracted URLs
for url in urls:
    print(url)
