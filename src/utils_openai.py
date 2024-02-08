"""Module with util functions for working with OpenAI API"""

import json
from openai import OpenAI

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

def get_image(openai_api_key:str, image_prompt:str):
    "Function getting logo"
    client = OpenAI(api_key = openai_api_key)
    response = client.images.generate(
        model = "dall-e-3",
        prompt = image_prompt
    )
    return response

def get_revised_prompt(image_response):
    """Function getting revised prompt from API return"""
    revised_prompt = image_response.data[0].revised_prompt
    return revised_prompt

def get_image_url(image_response):
    """Function getting image URL from API return"""
    image_url = image_response.data[0].url
    return image_url
