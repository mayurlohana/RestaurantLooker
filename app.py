import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# postcode = 'EC4M7RF'
def get_restaurants(postcode):
    base = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/"
    URL = base + postcode

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    response = requests.get(URL, headers=headers)
    data = response.json()
    restaurants = data['restaurants']

    resDetails = []

    if restaurants:
        for res in restaurants:
            name = res['name']
            addDetails = res['address']
            address = addDetails['firstLine'] + ', ' + '(' + addDetails['postalCode'] + ')' + ' - ' + addDetails['city']
            rating = res['rating']['starRating']
            cuisines = [cuisine['name'] for cuisine in res['cuisines']]
            resDetails.append([name, address, rating, cuisines])
        
        return resDetails, None
    
    else:
        return None, "OOPS! No Restaurants here, Mate! or You Enetered wrong POST Code"
    

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/restaurants', methods=['GET', 'POST'])
def restaurants():
    if request.method == 'POST':
        postcode = request.form.get('postcode')
        restaurants, error_message = get_restaurants(postcode)
        if restaurants:
            total_pages = len(restaurants) // 10 + (1 if len(restaurants) % 10 > 0 else 0)
            return render_template('restaurants.html', restaurants=restaurants[:10], total_pages=total_pages, current_page=1)
        else:
            return render_template('error.html', error_message=error_message)
    return render_template('postcode_form.html')


if __name__ == '__main__':
    app.run(debug=True)