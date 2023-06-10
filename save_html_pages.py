import os, sys, glob, re
import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

from path import LINK_LIST_PATH, RAW_HTML_DIR


# Encoding for writing the page html files
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def get_page_content(page_url):
    """
    This function should take the URL of a page and return the html
    content (string) of that page.
    """

    resp = requests.get(page_url)

    # Save the page content (html) in the variable "page_html"
    page_html = resp.text

    ###############################

    return page_html


def save_html_pages():
    # Step 1: Read URL/Link list file from LINK_LIST_PATH
    #         to get the urls that need to be saved
    url_df = pd.read_csv(LINK_LIST_PATH, sep="\t")

    # Step 2: Checking the downloaded html page IDs
    html_list = os.listdir(RAW_HTML_DIR)
    id_list = list(map(lambda x: x[:-5], html_list))

    # Step 3: Iterating through the URL list
    for idx, row in url_df.iterrows():
        page_id = row["id"]
        page_url = row["url"]

        # Skip page if already downloaded
        if page_id in id_list:
            continue

        # Step 4: Loading page html
        try:
            # Save the html content of the page in the variable page_html
            page_html = get_page_content(page_url)

        except Exception as e:
            # Pages that were not collected are saved as empty strings
            page_html = ""
            print(f"Error getting page {page_id} html: {e}")

        # Step 5: Saving page html
        try:
            save_path = os.path.join(RAW_HTML_DIR, f"{page_id}.html")

            with open(save_path, "w", encoding=ENCODING) as f:
                f.write(page_html)
            print(f"Saved page {page_id} ({idx+1} / {url_df.shape[0]})")

        except Exception as e:
            with open(save_path, "w", encoding=ENCODING) as f:
                f.write("")
            print("Error saving page {page_id} html:" + str(e))


if __name__ == "__main__":
    save_html_pages()