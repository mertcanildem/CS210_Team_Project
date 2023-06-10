import os, sys, glob, re
import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import uuid

from path import LINK_LIST_PATH

# Encoding for writing the URLs to the .txt file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def save_link(url, page):
    """
    Save collected link/url and page to the .txt file in LINK_LIST_PATH
    """
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(LINK_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, url, str(page)]) + "\n")


def download_links_from_index():
    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """

    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url", "page"]) + "\n")
        start_page = 1
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(LINK_LIST_PATH, sep="\t")
        if data.shape[0] == 0:
            start_page = 1
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max()
            downloaded_url_list = data["url"].to_list()

    # WRITE YOUR CODE HERE
    #########################################
    # Start downloading from the page "start_page"
    # which is the page you ended at the last
    # time you ran the code (if you had an error and the code stopped)
    rootURL = 'https://www.mgm.gov.tr/veridegerlendirme/il-ve-ilceler-istatistik.aspx?k=undefined&m='
    provinces = [
        "ADANA",
        "ADIYAMAN",
        "AFYONKARAHISAR",
        "AGRI",
        "AKSARAY",
        "AMASYA",
        "ANKARA",
        "ANTALYA",
        "ARDAHAN",
        "ARTVIN",
        "AYDIN",
        "BALIKESIR",
        "BARTIN",
        "BATMAN",
        "BAYBURT",
        "BILECIK",
        "BINGOL",
        "BITLIS",
        "BOLU",
        "BURDUR",
        "BURSA",
        "CANAKKALE",
        "CANKIRI",
        "CORUM",
        "DENIZLI",
        "DIYARBAKIR",
        "DUZCE",
        "EDIRNE",
        "ELAZIG",
        "ERZINCAN",
        "ERZURUM",
        "ESKISEHIR",
        "GAZIANTEP",
        "GIRESUN",
        "GUMUSHANE",
        "HAKKARI",
        "HATAY",
        "IGDIR",
        "ISPARTA",
        "İSTANBUL/FLORYA",
        "IZMIR",
        "K.MARAS",
        "KARABUK",
        "KARAMAN",
        "KARS",
        "KASTAMONU",
        "KAYSERI",
        "KILIS",
        "KIRIKKALE",
        "KIRKLARELI",
        "KIRSEHIR",
        "KOCAELI",
        "KONYA",
        "KUTAHYA",
        "MALATYA",
        "MANISA",
        "MARDIN",
        "MERSIN",
        "MUGLA",
        "MUS",
        "NEVSEHIR",
        "NIGDE",
        "ORDU",
        "OSMANIYE",
        "RIZE",
        "SAKARYA",
        "SAMSUN",
        "SIIRT",
        "SINOP",
        "SIVAS",
        "SANLIURFA",
        "SIRNAK",
        "TEKIRDAG",
        "TOKAT",
        "TRABZON",
        "TUNCELI",
        "USAK",
        "VAN",
        "YALOVA",
        "YOZGAT",
        "ZONGULDAK"
    ]
    for pid in range(start_page-1, 81):
        province = provinces[pid]
        pageURL = '{}{}'.format(rootURL, province)

        collected_url = pageURL

        page = pid

        if collected_url not in downloaded_url_list:
            print("\t", collected_url, flush=True)
            save_link(collected_url, page)
        #########################################


if __name__ == "__main__":
    download_links_from_index()