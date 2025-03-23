import random
import numpy as np
import re
import json

def extract_item_json_list(response,target):
    try:
        if isinstance(response, str):
            data = json.loads(response)
        else:
            data = response
        target = target.replace("&amp;", "&").replace("&reg;","®")   
        for key,value in data.items():
            try:
                if value.strip().lower().replace("&amp;", "&").replace("&reg;", "®") == target.strip().lower():
                    return [int(key)]
            except AttributeError:
                continue
        return []
    except json.JSONDecodeError:
        return []

def extract_wrapped_json(response):
    pattern = r'<START>(.*?)<END>'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            return None
    return None

def extract_edit_prompt(response):
    pattern = r'<START>\s*(.*?)\s*<END>'
    result_list = re.findall(pattern, response, re.DOTALL)
    if len(result_list) == 0:
        pattern = r'<START>(.*?)<END>'
        result_list = re.findall(pattern, response, re.DOTALL)
    return result_list 

def ndcg(target_index, max_rank=20):
    if target_index <= 0 or target_index > max_rank:
        return 0.0
    return 1.0 / np.log2(target_index + 1)

def extract_item_list(response, target):
    try:
        response = response.replace(" ", " ")
        target = target.replace(" ", " ").replace("&amp;", "&").replace("&reg;","®")
        index = response.rfind(target)
        if index != -1:
            preceding_text = response[:index].strip()
            numbers = re.findall(r'\d+', preceding_text)
            if numbers:
                result_list = numbers
            else:
                result_list = []
        else:
            result_list = []
    except:
        result_list = []
    return result_list





