"""Module with util functions for make_slides.py"""

import time
import string
import os
import urllib.request
import yaml

def make_run():
    """Function for making run string"""
    run = time.strftime("%Y%m%d%H%M", time.localtime())
    return run

def read_yaml(file_path:str):
    """Function for reading in yaml config file"""
    with open(file_path, encoding = "utf-8", mode = "r") as f:
        return yaml.safe_load(f)

def clean_string_for_directory(directory_name:str):
    """Function for removing punctuation and spaces in strings"""
    cleaned_directory_name = directory_name.translate(str.maketrans("", "", string.punctuation)).\
        replace(" ", "-")
    return cleaned_directory_name

def make_directory(directory_path:str):
    """Function for creating directory if it doesn't exist"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return directory_path

def make_run_sub(description:str, run:str):
    """Function for creating run subdirectory"""
    results_sub_path = make_directory("results")
    product_sub = clean_string_for_directory(description)
    product_sub_path = make_directory(f"{results_sub_path}/{product_sub}")
    run_sub_path = make_directory(f"{product_sub_path}/{run}")
    return run_sub_path

def write_text(run_sub_path:str, type_:str, text:str):
    """Function writing text to file"""
    write_fp = f"{run_sub_path}/{type_}.txt"
    with open(write_fp, mode = "w", encoding = "utf-8") as f:
        f.write(text)

def write_image(run_sub_path:str, type_:str, image_url:str):
    """Function writing image to file"""
    write_fp = f"{run_sub_path}/{type_}.jpg"
    urllib.request.urlretrieve(image_url, write_fp)
