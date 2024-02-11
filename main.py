from flask import Flask, render_template, request, jsonify
from scoring import score_product
from web_scraping import extract_product_details
from pymongo import MongoClient
from bson.objectid import ObjectId
from meeshoscrape import retrieve_catalog_data_from_web
import time

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/score', methods=['POST'])
def score():
    product_url = request.form['product_url']
    product_data = extract_product_details(product_url)

    if product_data:
        product_score = score_product(product_data)
        return render_template('sps.html', product_data=product_data, product_score=product_score)
    else:
        return render_template('sps.html', product_data=None, product_score=None)





@app.route('/scrape', methods=['POST'])
def scrape_catalog():
    # Retrieve form data
    catalog_url = request.form.get('catalog_url')
    database_name = request.form.get('database_name')
    collection_name = request.form.get('collection_name')

    # Debug print statements to inspect form data
    print("Catalog URL:", catalog_url)
    print("Database Name:", database_name)
    print("Collection Name:", collection_name)
    
    try:
        retrieve_catalog_data_from_web(catalog_url, database_name, collection_name)
        time.sleep(5)  # Simulate scraping delay

        # Return success response
        return jsonify({'status': 'success', 'message': 'Scraping completed!'})
    except Exception as e:
        # Return error response
        return jsonify({'status': 'error', 'message': str(e)})



# MongoDB connection
client = MongoClient('mongodb+srv://deva:Deva%4023%21@cluster0.6snrlbu.mongodb.net/')
db = client['catalog']  # Replace 'catalog_db'
@app.route('/get_collections')
def get_collections():
    # Retrieve collection names from the database
    collection_names = db.list_collection_names()
    return jsonify(collection_names)

@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    if request.method == 'POST':
        # Retrieve the selected collection name from the form
        collection_name = request.form.get('collection_name')
        # Retrieve documents from the selected collection
        collection_data = list(db[collection_name].find({}))
        return render_template('catalog.html', catalog_data=collection_data, collection_name=collection_name)

    # If it's a GET request, render the template with an empty collection_data
    return render_template('catalog.html', catalog_data=[], collection_name=None)


@app.route('/get_product_details', methods=['GET'])
def get_product_details():
    collection_name = request.args.get('collection_name')  # Get the collection name from the request
    product_id = request.args.get('id')
    
    # Retrieve the collection based on the collection name
    collection = db[collection_name]

    # Retrieve product details from the specified collection
    product_details = collection.find_one({'_id': ObjectId(product_id)})
    
    if product_details:
        # Convert ObjectId to string
        product_details['_id'] = str(product_details['_id'])
        return jsonify(product_details)
    else:
        return jsonify({'error': 'Product not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
