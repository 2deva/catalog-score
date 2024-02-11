import os
import tempfile
import cv2  # Import opencv-python
import uuid  # Import uuid for generating unique file names
import requests


def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        
        # Generate a unique file name using uuid
        temp_file_name = str(uuid.uuid4()) + ".jpg"
        temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)
        
        # Save the image to the temporary file
        with open(temp_file_path, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded to: {temp_file_path}")
        return temp_file_path
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def calculate_ppi(width_px, height_px, width_inches, height_inches):
    diagonal_resolution_px = (width_px ** 2 + height_px ** 2) ** 0.5
    diagonal_inches = (width_inches ** 2 + height_inches ** 2) ** 0.5
    ppi = round(diagonal_resolution_px / diagonal_inches, 2)
    return ppi

def get_image_info(temp_file_path):
    try:
        img = cv2.imread(temp_file_path)  # Use cv2 to read the image
        if img is None:
            raise Exception("Error: Unable to read image")
        
        height_px, width_px, _ = img.shape
        resolution_x, resolution_y = 96, 96  # Set default resolution if not available
        ppi = calculate_ppi(width_px, height_px, width_px / resolution_x, height_px / resolution_y)
        return ppi
    except Exception as e:
        print(f"Error extracting image information: {e}")
        return None
    
def score_title(title):
    title_score = 100 if title and len(title) > 0 and title != 'NA' else 0
    return title_score

def score_price(price):
    price_score = 100 if price and len(price) > 0 and price != 'NA' else 0
    return price_score

def score_seller(seller):
    seller_score = 100 if seller and len(seller) > 0 and seller != 'NA' else 0
    return seller_score

def score_image(images):
    image_urls = [value['url'] for value in images.values()]
    image_score = 0
    ppi_score = 0

    if image_urls:
        for image_url in image_urls:
            temp_file_path = download_image(image_url)
            image_ppi = get_image_info(temp_file_path)
            if image_ppi and image_ppi > 72:
                ppi_score += 0.5

    if len(image_urls) >= 1:
        image_score += 50

    if len(image_urls) >= 2:
        image_score += 20

    if ppi_score >= 1:
        image_score += 30

    return image_score
    
def score_details(details):
    details_score = 0
    total = 0
    for key, value in details.items():
        if key != "Nutritional Info" and key != "Additives Info":
            if value is not None and value != 'NA':
                details_score+=1
            total+=1
    details_score = int((details_score/total)*100)
    return details_score

def completenessScoring(product_data):

    complete = 0
    total = -3

    for key, value in product_data.items():
        if key != '_id' and key != "product_url":
            if key != 'product_details':
                if key == 'image':
                    if value is not None and len(value) > 0:
                        complete+=1
                elif value is not None and value != 'NA':
                    complete+=1

            elif key == 'product_details' and isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    if nested_key != "Nutritional Info" and nested_key != "Additives Info":
                        if nested_value is not None and nested_value != 'NA':
                            complete+=1
                        total+=1
        total+=1
    return round(complete/total)*100

def complianceScoring(product_data):

    compliant = 0

    for key, value in product_data.items():
        if key == 'product_details' and isinstance(value, dict):
            for nested_key, nested_value in value.items():
                if nested_key == "Imported Product Country Of Origin" and nested_value is not None and nested_value != 'NA':
                    compliant+=1
                elif nested_key == "Manufacturer Name" and nested_value is not None and nested_value != 'NA':
                    compliant+=1
                elif nested_key == "Customer Support" and nested_value is not None and nested_value != 'NA':
                    compliant+=1
                elif nested_key == "Customer Support Phone" and nested_value is not None and nested_value != 'NA':
                    compliant+=1
                elif nested_key == "Manufacturer Address" and nested_value is not None and nested_value != 'NA':
                    compliant+=1
                elif nested_key == "Nutritional Info" and nested_value is not None and nested_value != 'NA':
                    compliant+=1
                elif nested_key == "Additives Info" and nested_value is not None and nested_value != 'NA':
                    compliant+=1

    return round(compliant/7)*100

def correctnessScoring(product_data):

    s1 = score_title(product_data['title'])
    s2 = score_price(product_data['price'])
    s3 = score_seller(product_data['seller_name'])
    s4 = score_image(product_data['image'])
    s5 = score_details(product_data['product_details'])

    correctness = round (s1*0.2 + s2*0.1 + s3*0.1 + s4*0.3 + s5*0.3)

    return int(correctness)
def score_product(product_data):
    completenesScore = completenessScoring(product_data)
    correctnessScore = correctnessScoring(product_data)
    complianceScore = complianceScoring(product_data)
    totalScore = int(completenesScore*0.5 + correctnessScore*0.3 + complianceScore*0.2)
    print(product_data['title'])
    product_score = {
        'completeness_score': completenesScore,
        'correctness_score': correctnessScore,
        'compliance_score': complianceScore,
        'total_score': totalScore
    }
    return product_score