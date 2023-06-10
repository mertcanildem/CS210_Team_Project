import os, sys, glob, re
import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from path import RAW_HTML_DIR, PARSED_HTML_PATH

# Encoding for writing the parsed data to JSONS file

ENCODING = "utf-8"


def extract_content_from_page(file_path):
    """
    This function should take as an input the path to one html file
    and return a dictionary "parsed_data" having the following information:

    parsed_data = {
        "province": Date of the news on the html page
        "sun_hour": a calculation of the average passage of time based on the position of the Sun in the sky
        "rainy_day": number of days which the weather is rainy
        "monthly_amount_rain":amount of rain in a month in terms of (mm)
        "fastest_wind": fastest wind recorded (m/sn)
        "average_temperature":annually (°C)
        "highest_snow": highest snow recorded (cm)
        }

    This function is used in the parse_html_pages() function.

    """
    parsed_data = {}

    with open(file_path, 'r', encoding=ENCODING) as f:
        soup = bs(f.read(), 'lxml')

    parsed_data ={}

    th_element = soup.find('th', {'style': 'width:22%'})
    if th_element:
        text = th_element.text.strip()
    parsed_data['province'] = text


    try:
        sum = 0
        for i in range (1,13):
            if i<10:
                id_val = '0' + str(i)
            else:
                id_val = str(i)
            value = soup.find('td', id='g'+id_val).text
            converted_value = float(value.replace(',', '.'))
            sum += float(converted_value)
        average = sum/12   #take average annually
        formatted_average = format(average, ".2f")
        parsed_data['sun_hour'] = formatted_average
    except Exception as e:
        print(f"Failed to parse page")
        parsed_data['sun_hour'] = 0.0


    sum2 = 0
    for i in range(1, 13):
        if i < 10:
            id_val = '0' + str(i)
        else:
            id_val = str(i)
        value2 = soup.find('td', id='h' + id_val).text
        converted_value2 = float(value2.replace(',', '.'))
        sum2 += float(converted_value2)   #find annual amount
    formatted_average2 = format(sum2, ".2f")
    parsed_data['rainy_day'] = formatted_average2


    sum3 = 0
    for i in range(1, 13):
        if i < 10:
            id_val = '0' + str(i)
        else:
            id_val = str(i)
        value3 = soup.find('td', id='i' + id_val).text
        converted_value3 = float(value3.replace(',', '.'))
        sum3 += float(converted_value3)  #find annual amount
    formatted_average3 = format(sum3, ".2f")
    parsed_data['monthly_amount_rain'] = formatted_average3



    pattern = r'([\d.]+) m/sn'
    match = soup.find('b', text=re.compile(pattern))
    if match:
        number = match.string.strip().split()[0]
    parsed_data['fastest_wind'] = number


    sum4 = 0
    for i in range(1, 13):
        if i < 10:
            id_val = '0' + str(i)
        else:
            id_val = str(i)
        value4 = soup.find('td', id='d' + id_val).text
        converted_value4 = float(value4.replace(',', '.'))
        sum4 += float(converted_value4)
    average4 = sum4 / 12
    formatted_average4 = format(average4, ".2f")
    parsed_data['average_temperature'] = formatted_average4


    pattern2 = r'([\d.]+) cm'
    match2 = soup.find('b', text=re.compile(pattern2))
    if match2:
        number2 = match2.string.strip().split()[0]
    parsed_data['highest_snow'] = number2

    ##################################

    return parsed_data


def parse_html_pages():
    # Load the parsed pages
    parsed_id_list = []
    if os.path.exists(PARSED_HTML_PATH):
        with open(PARSED_HTML_PATH, "r", encoding=ENCODING) as f:
            # Saving the parsed ids to avoid reparsing them
            for line in f:
                data = json.loads(line.strip())
                id_str = data["id"]
                parsed_id_list.append(id_str)
    else:
        with open(PARSED_HTML_PATH, "w", encoding=ENCODING) as f:
            pass

    # Iterating through html files
    for file_name in os.listdir(RAW_HTML_DIR):
        page_id = file_name[:-5]

        # Skip if already parsed
        if page_id in parsed_id_list:
            continue

        # Read the html file and extract the required information

        # Path to the html file
        file_path = os.path.join(RAW_HTML_DIR, file_name)

        try:
            parsed_data = extract_content_from_page(file_path)
            parsed_data["id"] = page_id
            print(f"Parsed page {page_id}")

            # Saving the parsed data
            with open(PARSED_HTML_PATH, "a", encoding=ENCODING) as f:
                f.write("{}\n".format(json.dumps(parsed_data)))

        except Exception as e:
            print(f"Failed to parse page {page_id}: {e}")



if __name__ == "__main__":
    parse_html_pages()