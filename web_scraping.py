# single product web_scraping.py

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def extract_product_details(product_url):
    try:
        # Fetch the HTML content of the product page
        response = requests.get(product_url)
        if response.status_code != 200:
            print(f"Failed to fetch product page: {response.status_code}")
            return None

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract thumbnail image URLs
        thumbnail_links = soup.select('.thumb-image-ul li.image-gallery-thumbnail a')
        thumbnail_urls = {}
        for i, link in enumerate(thumbnail_links, start=1):
            thumbnail_urls[f"url{i}"] = {'url': link.find('img')['src']}
        print("Thumbnail Image URLs:", thumbnail_urls)


        # Extract product details
        product_data = {
            'product_url': product_url,
            'title': soup.select_one('.detail h1.detail-product-name').text.strip(),
            'price': soup.select_one('.offered-price').text.strip(),
            'seller_name': soup.select_one('.detail-product-name[style="font-size: 14px!important"]').text.strip(),
            'image': thumbnail_urls,
            'product_details': {
                key.text.strip().split('\n', 1)[0]: value.text.strip().replace('\n', ' ')
                for key, value in zip(
                    soup.select('.productSpecificationSection .row .col-xl-3'),
                    soup.select('.productSpecificationSection .row div[style^="color: #777;word-break: break-word; overflow:"]')
                )
            }
        }

        print("Product Data:", product_data)
        return product_data
    except Exception as e:
        print(f"Error extracting product details: {e}")
        return None

#extract_product_details('https://ondc.meesho.org/product/campus-sutra-women-stylish-jacket-m---m/1105262143')