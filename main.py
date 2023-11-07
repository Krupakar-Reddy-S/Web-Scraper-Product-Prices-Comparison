from Products import Amazon
from Products import Flipkart1
from Products import Flipkart2
from Products import Flipkart3
from Products import Snapdeal
from Products import Variables

import matplotlib.pyplot as plt
import multiprocessing
import webbrowser
import queue


def fetch_amazon(search_query, results):
    amazon_results = Amazon.search_results(search_query, Variables.user_agents)
    results.put(amazon_results)


def fetch_snapdeal(search_query, results):
    snapdeal_results = Snapdeal.search_results(search_query, Variables.user_agents)
    results.put(snapdeal_results)


def fetch_flipkart1(search_query, results):
    flipkart1_results = Flipkart1.search_results(search_query, Variables.user_agents)
    results.put(flipkart1_results)


def fetch_flipkart2(search_query, results):
    flipkart2_results = Flipkart2.search_results(search_query, Variables.user_agents)
    results.put(flipkart2_results)


def fetch_flipkart3(search_query, results):
    flipkart3_results = Flipkart3.search_results(search_query, Variables.user_agents)
    results.put(flipkart3_results)


def products_validation(products):
    product_prices = [product.get('product_price', 0) for product in products.values()]
    average_product_price = int(sum(product_prices) / len(product_prices) if product_prices else 0)
    print("Validated products based on Average Price.")
    print(f"Average Product Price: ₹{average_product_price}")
    print(f"Validation Limit: ₹{int(average_product_price * 0.75)}\n")

    products_copy = products.copy()

    for serial, product in products_copy.items():
        if product.get('product_price', 0) < (average_product_price * 0.75) or product.get('product_price', 0) > (average_product_price * 1.75):
            del products[serial]

    return products


def plot_prices_with_links_and_tooltips(product_results, search_query):

    product_names = [product_data.get("product_name") for product_data in product_results.values()]
    product_prices = [product_data.get("product_price") for product_data in product_results.values()]
    product_links = [product_data.get("product_link") for product_data in product_results.values()]
    product_serials = list(product_results.keys())

    x = list(range(1, len(product_names) + 1))

    fig, ax = plt.subplots()

    ax.plot(x, product_prices, marker='o', linestyle='-')
    tooltips = []

    buffer_x = 0.5
    buffer_y = 100

    def hover(event):
        for tooltip in tooltips:
            tooltip.set_visible(False)

        for i, (xi, price, serial, name) in enumerate(zip(x, product_prices, product_serials, product_names)):
            if event.xdata is not None and event.ydata is not None:
                if (xi - buffer_x) <= event.xdata <= (xi + buffer_x) and (price - buffer_y) <= event.ydata <= (price + buffer_y):
                    tooltip_text = f"Serial: {serial}\nName: {name}\nPrice: ₹{price}"
                    tooltip = ax.text(xi, price, tooltip_text, fontsize=8, ha='center', va='bottom', visible=True,
                                      bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black"))
                    tooltips.append(tooltip)

        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', hover)

    def on_click(event):
        if event.xdata is not None and event.ydata is not None:
            point_index = int(event.xdata) - 1
            if 0 <= point_index < len(product_links):
                webbrowser.open(product_links[point_index])

    fig.canvas.mpl_connect('button_press_event', on_click)

    ax.set_xlabel("Products")
    ax.set_ylabel("Price in ₹")
    ax.set_title(f"Product Prices of search query: {search_query}")

    plt.show()


search_query = input("Enter your search query: ")

results = multiprocessing.Queue()
process1 = multiprocessing.Process(target=fetch_amazon, args=(search_query, results))
process2 = multiprocessing.Process(target=fetch_snapdeal, args=(search_query, results))
process3 = multiprocessing.Process(target=fetch_flipkart1, args=(search_query, results))
process4 = multiprocessing.Process(target=fetch_flipkart2, args=(search_query, results))
process5 = multiprocessing.Process(target=fetch_flipkart3, args=(search_query, results))

process1.start()
process2.start()
process3.start()
process4.start()
process5.start()

process1.join()
process2.join()
process3.join()
process4.join()
process5.join()

Product_results = {}
while True:
    try:
        Product_results.update(results.get_nowait())
    except queue.Empty:
        break

for serial, product in Product_results.items():
    print(f"Serial_No: {serial}")
    print(f"Product_Name: {product['product_name']}")
    print(f"Product_Price: {product['product_price']}")
    print(f"Product_Image_Link: {product['product_image_link']}")
    print(f"Product_Page_Link: {product['product_link']}")
    print()

validate_products = input("Note: Product validation is based on average price and can also remove relevant products\nfrom the graph option defaults to Yes. Enter input for product validation ([Yes]/No): ")
if not validate_products.lower() == "no":
    Product_results = products_validation(Product_results)

plot_prices_with_links_and_tooltips(Product_results, search_query)
