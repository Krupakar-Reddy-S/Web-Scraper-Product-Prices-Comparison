# Web-Scraper-Product-Prices-Comparison
The code scrapes product details from search result of Amazon, Flipkart and snapdeal (All Indian), with an option to filter for relevant products based on Average price and shows their graph comparison.

```
Web-Scraper/
├── Products/
│   ├── amazon.py
│   ├── flipkart1.py
│   ├── flipkart2.py
│   ├── flipkart3.py
│   ├── snapdeal.py
│   ├── variable.py
│   ├── __init__.py
├── requirements.txt
├── README.md
├── main.py

```

The `main.py` imports the `Products` package and uses the functions in the package to scrape the product details from the respective websites.
All the required packages are listed in the `requirements.txt` file.

### Products Package Contents

- Each file in the package is a web scraper for the respective website.
The `variable.py` file contains the list of user-agents to be used in the request headers.
- The `__init__.py` file is used to make the package.
- All the files contain a `search_results()` function which using the `scrape_product()` function scrapes the product details from the search results page of the respective website.
- The product details are returned as dictionary of the form:

```
{
    key: SerialNo - CompanyName with No. of products till now,
    value: {
        product_name: Name of the product,
        product_price: Price of the product,
        product_image_link: Link to the product image,
        product_link: Link to the product page,
    }
}
```

- The purpose of having multiple files for **Flipkart** is to make sure to scrape products from all the different possible structures of the search results page.
- All the Individual functions for scraping have print() statements to show the progress of the scraping process.

**The core logic of the scraping process is to find the HTML tags and their attributes which contain the required data and extract them.**

### Explanation of `main.py` file

- The `main.py` file first takes an input from the user as the search query and then uses it to call the `search_results()` function of each of the scraper files in the `Products` package.
- Since the request calls run till a response is received, it make the process very slow so the `multiprocessing` module is used to run the functions in parallel to reduce runtime.
- The returned dictionaries are then combined into a single dictionary and are printed to the console.
- The `filter_products()` function is then called which takes the combined dictionary as input and filters the products based on the average price of the products.
- Based on the users choice filtration occurs and the products dictionary is then used to plot a graph using the `matplotlib` module.
- The graph has the product names on the x-axis and the prices on the y-axis, and there is a tooltip displaying the product details on hovering over the data points.
- When any datapoint is clicked, the link to the product page is opened in the default browser using the `webbrowser` module.

> **Note:** ConnectionError and others are handled using try-except blocks to give feedback about the users input.

