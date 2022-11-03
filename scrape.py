import csv
import json

import bs4
import requests
from urllib.parse import urlparse


products_list = []

url = "https://webscraper.io/test-sites/e-commerce/scroll"
base_url = urlparse(url).scheme + "://" + urlparse(url).netloc

res = requests.get(url)
res.raise_for_status()

soupObj = bs4.BeautifulSoup(res.text, "html.parser")
cats_list = soupObj.select(".category-link")
for cat in cats_list:
    res_cat = requests.get(base_url + cat.get("href"))
    res_cat.raise_for_status()

    soupObjCat = bs4.BeautifulSoup(res_cat.text, "html.parser")

    subcats_list = soupObjCat.select(".subcategory-link")
    for subcat in subcats_list:
        print(subcat.get("href"))

        res_subcat = requests.get(base_url + subcat.get("href"))
        res_subcat.raise_for_status()

        soupObjItems = bs4.BeautifulSoup(res_subcat.text, "html.parser")
        items_list = soupObjItems.select("div.row.ecomerce-items.ecomerce-items-scroll")
        for item in items_list:
            items = json.loads(item.attrs["data-items"])  # list of dicts
            for dict in items:
                dict2list = list(dict.values())
                dict2list.insert(1, f"{url}/product/{dict['id']}")
                products_list.append(dict2list)


with open("products.csv", "w", newline="") as csv_f:
    writer = csv.writer(csv_f)
    writer.writerow(["Product ID", "URL", "Title", "Description", "Price"])
    writer.writerows(products_list)
