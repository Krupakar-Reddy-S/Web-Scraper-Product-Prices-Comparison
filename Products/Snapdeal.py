from bs4 import BeautifulSoup
import requests
import random

from Products import Variables


def scrape_product(product, serial, results):
    try:
        product_name = product.find('p', class_='product-title').text.strip()

        product_price = product.find('span', class_='product-price').text.strip()
        product_price = int(product_price.replace("Rs.", "").replace(",", ""))

        product_link = product.find('a', class_='dp-widget-link')['href']

        image_element = product.find('img', class_='product-image lazy-load')
        product_image_link = image_element.get('data-src')

    except AttributeError:
        return serial

    product_details = {
        'product_name': product_name,
        'product_price': product_price,
        'product_image_link': product_image_link,
        'product_link': product_link
    }

    results["Snapdeal" + str(serial)] = product_details
    return serial + 1


def search_results(search_string, user_agents):
    url = f"https://www.snapdeal.com/search?keyword={search_string.replace(' ', '%20')}&sort=rlvncy"

    print()
    print("Retrieving products from Snapdeal...")
    print("URL: " + url + "\n")

    results = {}
    serial = 1

    session = requests.Session()

    while True:
        headers = {"User-Agent": random.choice(user_agents)}
        print("Snapdeal process: ")
        print(f"Using User Agent: {headers['User-Agent']}")
        response = session.get(url, headers=headers)

        if response.status_code == 200:
            print()
            soup = BeautifulSoup(response.text, 'html.parser')
            product_listings = soup.find_all('div', class_='product-tuple-listing')

            for product in product_listings:
                serial = scrape_product(product, serial, results)

            break

        else:
            print(f"Failed to retrieve the page. Status Code: {response.status_code} Retrying...\n")

    return results


# search_query = input("Enter your search query: ")
# results = search_results(search_query, Variables.user_agents)
#
# for serial, product in results.items():
#     print(f"Serial No: {serial}")
#     print(f"Name: {product['product_name']}")
#     print(f"Price: {product['product_price']}")
#     print(f"Image Link: {product['product_image_link']}")
#     print(f"Product Link: {product['product_link']}")
#     print()
