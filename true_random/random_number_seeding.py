#!/usr/bin/env python3

"""
Seed a true random number to relevant libraries
"""

import os
import json
import random
import requests


def seed_via_random_api(minimum, maximum, api_key, random_url="https://api.random.org/json-rpc/2/invoke"):
    """
    Seeds PYTHONHASHSEED and the random library via a random number generated using the random.org API

    Parameters
    ----------
    minimum: int
        Smallest int to return
    maximum:
        Largest int to return
    api_key: str
        User API Key from random.org
    random_url: str (default is current version 2 API)
        API base URL

    Returns
    -------
    Union[int,list]
        If 1 random number requested, return an int. If multiple requested, return a list of ints
    """
    if minimum >= maximum:
        raise ValueError(f"Maximum ({maximum}) must be greater minimum ({minimum})")
    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {"apiKey": api_key, "n": 1, "min": int(minimum), "max": int(maximum), "replacement": True},
        "id": 24601,
    }
    headers = {"content-type": "application/json"}
    response = requests.post(random_url, data=json.dumps(payload), headers=headers)
    data = json.loads(response.text)["result"]["random"]["data"]
    random.seed(data)
    os.environ["PYTHONHASHSEED"] = str(data)
    return data
