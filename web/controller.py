import datetime, requests
from models import db, Product, ProductHistory

api_key = 'replace-me'
api_url = 'http://api.walmartlabs.com/v1'

def fetch_existing_product(upc):
    try:
        product = Product.get(
            Product.upc == upc
        )
        return product
    except:
        return None


def search_walmart_api(upc):
    url = api_url + '/items?apiKey=' + api_key + '&upc=' + str(upc)
    r = requests.get(url)
    json = r.json()

    if 'items' in json and len(json['items']) > 0:
        return json['items'][0]
    
    return None


def get_product(upc):
    product = fetch_existing_product(upc)

    if not product:
        data = search_walmart_api(upc)
    
        if not data:
            return None

        product = Product(
            name = data['name'] or NotImplementedError,
            upc = upc,
            url = data['productUrl'] or None,
            add_to_cart_url = data['addToCartUrl'] or None,
            size = data['attributes']['size'] if 'size' in data['attributes'] else '0 oz',
            empty = False,
            reordered = False
        )
        product.save()

    return product