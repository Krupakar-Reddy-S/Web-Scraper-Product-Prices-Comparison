from bs4 import BeautifulSoup
import requests
import random

from Products import Variables


def scrape_product(product, serial, results):
    try:
        product_name = product.find("div", {"class": "_4rR01T"}).get_text(strip=True)

        product_price = product.find("div", {"class": "_30jeq3"}).get_text(strip=True)
        product_price = int(product_price.replace("₹", "").replace(",", ""))

        product_image_link = product.find("img", {"class": "_396cs4"})["src"]
        product_link = "https://www.flipkart.com" + product.find("a", {"class": "_1fQZEK"})["href"]

    except AttributeError:
        return serial

    product_details = {
        "product_name": product_name,
        "product_price": product_price,
        "product_image_link": product_image_link,
        "product_link": product_link,
    }

    results["Flipkart" + str(serial)] = product_details
    return serial + 1


def search_results(search_string, user_agents):
    url = f"https://www.flipkart.com/search?q={search_string.replace(' ', '%20')}"

    print("\nAttempting to Retrieve products from Flipkart3 Structure...")
    print("URL: " + url + "\n")

    session = requests.Session()
    results = {}
    serial = 1
    status_code = 500

    while status_code == 500:
        headers = {"User-Agent": random.choice(user_agents)}
        print("Flipkart3 process: ")
        print(f"Using User Agent: {headers['User-Agent']}")
        response = session.get(url, headers=headers)

        if response.status_code == 200:
            print()
            soup = BeautifulSoup(response.content, "html.parser")
            product_listings = soup.find_all("div", {"class": "_1AtVbE"})

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
#     print(f"Serial No: {serial}")
#     print(f"Name: {product['product_name']}")
#     print(f"Price: {product['product_price']}")
#     print(f"Image Link: {product['product_image_link']}")
#     print(f"Product Link: {product['product_link']}")
#     print()
