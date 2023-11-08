from bs4 import BeautifulSoup
import requests
import random

from Products import Variables


def scrape_product(product, serial, results):
    try:
        product_name = product.find("a", {"class": "IRpwTa"}).text.strip()

        product_price = product.find("div", {"class": "_30jeq3"}).text.strip()
        product_price = int(product_price.replace("₹", "").replace(",", ""))

        product_image_link = product.find("img", {"class": "_2r_T1I"})["src"]
        product_link = "https://www.flipkart.com" + product.find("a", {"class": "IRpwTa"})["href"]
    except AttributeError:
        return serial

    product_details = {
        "product_name": product_name,
        "product_price": product_price,
        "product_image_link": product_image_link,
        "product_link": product_link
    }

    results["Flipkart" + str(serial)] = product_details
    return serial + 1


def search_results(search_string, user_agents):
    url = "https://www.flipkart.com/search?q=" + search_string.replace(" ", "+")

    print("\nAttempting to Retrieve products from Flipkart2 Structure...")
    print("URL: " + url + "\n")

    results = {}
    serial = 1

    session = requests.Session()

    while True:
        headers = {"User-Agent": random.choice(user_agents)}
        print("Flipkart2 process: ")
        print(f"Using User Agent: {headers['User-Agent']}")
        response = session.get(url, headers=headers)

        if response.status_code == 200:
            print()
            soup = BeautifulSoup(response.content, "html.parser")
            product_listings = soup.find_all("div", {"class": "_1xHGtK _373qXS"})

            for product in product_listings:
                serial = scrape_product(product, serial, results)

            break

        else:
            print(f"Failed to retrieve the page. Status Code: {response.status_code}. Retrying...\n")

    return results


# search_query = input("Enter your search query: ")
# results = search_results(search_query, Variables.user_agents)
#
# for product in results:
#     print("Product Name:", product["product_name"])
#     print("Product Price:", product["product_price"])
#     print("Product Image Link:", product["product_image_link"])
#     print("Product Link:", product["product_link"])
#     print()
