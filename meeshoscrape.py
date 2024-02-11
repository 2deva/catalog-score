from bs4 import BeautifulSoup
import requests
import time
from pymongo import MongoClient


def extract_product_details(product_url, max_retries=3):
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}")

            # Fetch product details URL directly
            response = requests.get(product_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract product details from the soup object
            product_title = soup.select_one('.detail h1.detail-product-name').text.strip()
            product_price = soup.select_one('.offered-price').text.strip().replace(' ', '')  # Remove whitespace
            seller_name = soup.select_one('.detail-product-name[style="font-size: 14px!important"]').text.strip()

            # Extract thumbnail image URLs
            thumbnail_links = soup.select('.thumb-image-ul li.image-gallery-thumbnail a')
            thumbnail_urls = {}
            for i, link in enumerate(thumbnail_links, start=1):
                thumbnail_urls[f"url{i}"] = {'url': link.find('img')['src']}
            print("Thumbnail Image URLs:", thumbnail_urls)  # Debug statement
            
            # Extract product specifications
            product_details = {}
            key_elements = soup.select('.productSpecificationSection .row .col-xl-3')
            value_elements = soup.select('.productSpecificationSection .row div[style^="color: #777;word-break: break-word; overflow:"]')
            for key_element, value_element in zip(key_elements, value_elements):
                key = key_element.text.strip().split('\n', 1)[0]
                value = value_element.text.strip().replace('\n', ' ')
                product_details[key] = value

            # Create a dictionary with all the extracted information
            product_data = {
                'product_url': product_url,
                'title': product_title,
                'price': product_price,
                'seller_name': seller_name,
                'image': thumbnail_urls,  # Storing thumbnail URLs
                'product_details': product_details,
            }

            # Return the product data
            return product_data

        except Exception as e:
            print(f"Exception occurred: {e}")
            print(f"Retrying... (Attempt {attempt + 2})")
            time.sleep(2)  # Wait for 2 seconds before retrying
            continue

    print("Max retries reached. Unable to extract product details.")
    return None

def retrieve_product_urls_from_page(page_url):
    try:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_links = soup.select('.feed-product-main a')
        product_urls = [f"https://ondc.meesho.org{link['href']}" for link in product_links]
        return product_urls
    except Exception as e:
        print(f"Error retrieving product URLs from {page_url}: {e}")
        return []

def retrieve_catalog_data_from_web(catalog_url, database_name, collection_name):
    client = MongoClient('localhost', 27017)
    db = client[database_name]
    collection = db[collection_name]
    
    try:
        # Retrieve all product URLs from the catalog page
        product_urls = retrieve_product_urls_from_page(catalog_url)
        print(f"Number of products found: {len(product_urls)}")

        # Iterate over product URLs
        for index, product_url in enumerate(product_urls, start=1):
            print(f"Processing product {index} - URL: {product_url}...")
            product_data = extract_product_details(product_url)

            # Print the data for debugging
            if product_data:
                print("Extracted Product Data:", product_data)

            # Store data in MongoDB or perform other actions as needed
            if product_data:
                collection.insert_one(product_data)
    except Exception as e:
        print(f"Error retrieving catalog data from {catalog_url}: {e}")
