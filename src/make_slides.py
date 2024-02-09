"""Module for generating pitch with OpenAI services"""

import json
from utils import write_text, write_image, make_run, make_run_sub, read_yaml
from utils_openai import get_text, parse_text, get_image, get_revised_prompt, get_image_url
from utils_pptx import make_presentation

################################################################################
#                                                                              #
#                                Global Variables                              #
#                                                                              #
################################################################################

SYSTEM_PROMPT = """
You will be generating compelling marketing text for a new startup that needs help crafting its 
pitch for potential investors. You will be provided a description of the product You will use the 
description to generate several outputs. First you will generate a name for the company. Second, 
you will generate a company tagline. Third, you will generate a problem statement with 5 bullet 
points of 5-10 words that summarizes the problem as it exists today that the company will address. 
Fourth, you will generate a solution statement that states in one sentence how the company's 
product will solve that problem. You will also receive additional instructions about the desired
tone of outputs. For example, if you receive the instruction "humorous" you should inject jokes
into your output. Do not include the exact words in the instructions in your output. Your output 
will be JSON with the following keys: name, tag, problem, solution. The value for the problem key 
will be a list of strings.
"""

################################################################################
#                                                                              #
#                                    Functions                                 #
#                                                                              #
################################################################################

def make_user_text_prompt(product_description:str, product_vibes:str):
    """Function for making prompt for text components of pitch"""
    user_prompt = "\n".join((
        f"Description: {product_description}", 
        f"Instructions: {product_vibes}"
    ))
    return user_prompt

def make_write_user_text_prompt(product_description:str, product_vibes:str, run_sub_path:str):
    "Function making and writing to file prompt for text components of pitch"
    text_prompt = make_user_text_prompt(product_description, product_vibes)
    write_text(run_sub_path, "text-prompt", text_prompt)
    return text_prompt

def make_image_prompt(company_name:str, product_description:str, product_vibes:str):
    """Function making prompt for logo"""
    image_prompt = " ".join((
        "I NEED to test how the tool works with extremely simple prompts.",
        "DO NOT add any detail, just use it AS-IS:"
        f"A {product_vibes} logo",
        f"containing images for {company_name}",
        f"which makes {product_description}"
    ))
    return image_prompt

def make_write_image_prompt(company_name:str, product_description:str, product_vibes:str,
                            run_sub_path:str):
    """Function making and writing to file prompt for logo"""
    image_prompt = make_image_prompt(company_name, product_description, product_vibes)
    write_text(run_sub_path, "image-prompt", image_prompt)
    return image_prompt

def get_write_text(api_key:str, user_text_prompt:str, run_sub_path:str):
    """Function getting and writing to file text components of pitch"""
    try:
        text_response = get_text(api_key, SYSTEM_PROMPT, user_text_prompt)
    except Exception as error:
        raise RuntimeError("Get text API call failed") from error
    try:
        text = parse_text(text_response)
    except Exception as error:
        raise RuntimeError("Failed to parse JSON in text response") from error
    try:
        write_text(run_sub_path, "text", json.dumps(text))
    except Exception as error:
        raise RuntimeError("Failed to write parsed text response to file") from error
    return text

def get_write_image(api_key:str, image_prompt:str, run_sub_path:str):
    """Function getting and writing to file logo"""
    try:
        image_response = get_image(api_key, image_prompt)
    except Exception as error:
        raise RuntimeError("Get image API call failed") from error
    try:
        image_revised_prompt = get_revised_prompt(image_response)
    except Exception as error:
        raise RuntimeError("Failed to get revised prompt from image response") from error
    try:
        write_text(run_sub_path, "image-prompt-revised", image_revised_prompt)
    except Exception as error:
        raise RuntimeError("Failed to write revised prompt to file") from error
    try:
        image_url = get_image_url(image_response)
    except Exception as error:
        raise RuntimeError("Failed to get image url from image response") from error
    try:
        logo_fp = write_image(run_sub_path, "logo", image_url)
    except Exception as error:
        raise RuntimeError("Failed to write logo to file") from error
    return logo_fp

def main(config_fp):
    """Function for running module"""
    run = make_run()
    print(f"Run: {run}")
    try:
        config = read_yaml(config_fp)
    except FileNotFoundError as error:
        print(f"An error occured: {error}")
        return
    try:
        description = config["PRODUCT"]["DESCRIPTION"]
        vibes = config["PRODUCT"]["VIBES"]
        api_key = config["OPENAI"]["SECRET_KEY"]
    except KeyError as error:
        print(f"An error occured: {error}")
        return
    run_sub_path = make_run_sub(description, run)
    text_prompt = make_write_user_text_prompt(description, vibes, run_sub_path)
    try:
        text = get_write_text(api_key, text_prompt, run_sub_path)
    except RuntimeError as error:
        print(f"An error has occured: {error}")
        return
    name = text.get("name")
    tag = text.get("tag")
    image_prompt = make_write_image_prompt(name, description, vibes, run_sub_path)
    try:
        logo_fp = get_write_image(api_key, image_prompt, run_sub_path)
    except RuntimeError as error:
        print(f"An error has occured: {error}")
        return
    try:
        make_presentation(logo_fp, name, tag, f"{run_sub_path}/presentation.pptx")
    except Exception as error:
        print(f"An error has occured: {error}")
    print(f"Run {run} succeeded.")

################################################################################
#                                                                              #
#                                       Main                                   #
#                                                                              #
################################################################################

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description = "Generate a pitch for your product")
    parser.add_argument("-c", "--config", required = True, help = "Path to config file")
    args = parser.parse_args()

    main(config_fp = args.config)
