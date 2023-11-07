from bs4 import BeautifulSoup
import requests
import random

from Products import Variables


def scrape_product(product, serial, results):

    try:
        product_name = product.find("span", {"class": "a-text-normal"}).get_text(strip=True)

        product_price = product.find("span", {"class": "a-offscreen"}).get_text(strip=True)
        product_price = int(float(product_price.replace("₹", "").replace(",", "")))

        product_image_link = product.find("img", {"class": "s-image"})["src"]
        product_link = "https://www.amazon.in" + product.find("a", {"class": "a-link-normal"})["href"]

    except AttributeError:
        return serial

    product_details = {
        "product_name": product_name,
        "product_price": product_price,
        "product_image_link": product_image_link,
        "product_link": product_link
    }

    results["Amazon" + str(serial)] = product_details
    return serial + 1


def search_results(search_string, user_agents):
    url = "https://www.amazon.in/s?k=" + search_string.replace(" ", "+")

    print()
    print("Retrieving products from Amazon...")
    print("URL: " + url + "\n")

    results = {}
    serial = 1
    status_code = 503

    session = requests.Session()

    while (status_code == 503):
        headers = {"User-Agent": random.choice(user_agents)}
        print("Amazon process: ")
        print(f"Using User Agent: {headers['User-Agent']}")
        response = session.get(url, headers=headers)

        if response.status_code == 200:
            print()
            soup = BeautifulSoup(response.content, "html.parser")
            product_listings = soup.find_all("div", {"data-component-type": "s-search-result"})

            for product in product_listings:
                serial = scrape_product(product, serial, results)

            status_code = 200

        else:
            print(f"Failed to retrieve the page. Status Code: {response.status_code} Retrying...\n")

    return results


# search_query = input("Enter your search query: ")
# results = search_results(search_query, Variables.user_agents)
#
# for serial, product in results.items():
#     print(f"Serial_No: {serial}")
#     print(f"Product_Name: {product['product_name']}")
#     print(f"Product_Price: {product['product_price']}")
#     print(f"Product_Image_Link: {product['product_image_link']}")
#     print(f"Product_Page_Link: {product['product_link']}")
#     print()
