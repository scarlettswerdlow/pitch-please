"""Module for OpenAI services"""

import json
from openai import OpenAI

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

def make_user_text_prompt(product_description:str, brand:str):
    """Function making prompt for text components of pitch"""
    user_text_prompt = "\n".join((
        f"Description: {product_description}", 
        f"Instructions: {brand}"
    ))
    return user_text_prompt

def get_text(openai_api_key:str, system_prompt:str, user_prompt:str):
    """Function getting text components of pitch"""
    client = OpenAI(api_key = openai_api_key)
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        response_format = {"type": "json_object"},
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response

def parse_text(text_response):
    """Function parsing get_text response"""
    content = json.loads(text_response.choices[0].message.content)
    rv = {
        "name": content.get("name"),
        "tag": content.get("tag"),
        "problem": content.get("problem"),
        "solution": content.get("solution")
    }
    return rv

def text_wrapper(product_description:str, brand:str, openai_api_key:str):
    """Function executing OpenAI text process"""
    user_text_prompt = make_user_text_prompt(product_description, brand)
    text_response = get_text(openai_api_key, SYSTEM_PROMPT, user_text_prompt)
    parsed_text = parse_text(text_response)
    return parsed_text

def make_logo_prompt(company_name:str, product_description:str, brand:str):
    """Function making prompt for logo"""
    image_prompt = " ".join((
        "I NEED to test how the tool works with extremely simple prompts.",
        "DO NOT add any detail, just use it AS-IS:"
        f"A {brand} logo",
        f"containing images for {company_name}",
        f"which makes {product_description}"
    ))
    return image_prompt

def get_logo(openai_api_key:str, image_prompt:str):
    "Function getting logo"
    client = OpenAI(api_key = openai_api_key)
    response = client.images.generate(
        model = "dall-e-3",
        prompt = image_prompt
    )
    return response

def get_logo_url(image_response):
    """Function getting image URL from API return"""
    image_url = image_response.data[0].url
    return image_url

def logo_wrapper(company_name:str, product_description:str, brand:str, openai_api_key:str):
    """Function executing OpenAI logo process"""
    logo_prompt = make_logo_prompt(company_name, product_description, brand)
    logo_response = get_logo(openai_api_key, logo_prompt)
    logo_url = get_logo_url(logo_response)
    return logo_url
