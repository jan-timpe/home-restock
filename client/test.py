import cv2, requests
from pyzbar.pyzbar import decode

def read_barcodes():
    img = cv2.imread('./img/qrs/spaghetti-sauce-and-noodles.png')
    barcodes = decode(img)

    items = []
    for code in barcodes:
        item = {
            'code': code.data.decode(),
            'upc': code.data.decode()[1:]
        }
        items.append(item)

    return items


def set_initial_data(upc, weight):
    url = 'http://localhost:5000/update/' + str(upc) + '/'
    r = requests.post(url, data={
        'weight': weight
    })

    return r.json()

def update_data(upc, weight, empty=False, reordered=False):
    url = 'http://localhost:5000/update/' + str(upc) + '/'
    r = requests.post(url, data={
        'weight': weight,
        'empty': empty,
        'reordered': reordered
    })

    return r.json()

if __name__ == '__main__':
    items = read_barcodes()

    for item in items:
        r = set_initial_data(item['upc'], 100)
        print(r)

        r = update_data(item['upc'], 50)
        print(r)

        r = update_data(item['upc'], 10, reordered=True)
        print(r)

        r = update_data(item['upc'], 5, empty=True)
        print(r)