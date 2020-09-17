import requests
import json
from typing import Tuple


API_POSTCODES = "http://api.postcodes.io/postcodes/{0}"
API_TRANSPORT = "http://transportapi.com"


def main():
    print(get_lon_lat("postcode"))


def get_lon_lat(postcode: str) -> Tuple:
    resp = requests.get(url=API_POSTCODES.format(postcode))

    if 200 <= resp.status_code <= 299:
        data = resp.json()
        return data["result"]["longitude"], data["result"]["latitude"]
    else:
        raise Exception("Failed to get lon/lat: status code {0}".format(resp.status_code))


if __name__ == "__main__":
    main()
