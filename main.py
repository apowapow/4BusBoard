import requests
import argparse
from typing import Tuple, List, Dict
from pprint import pprint


API_POSTCODES = "http://api.postcodes.io/postcodes/{0}"
API_NEARBY_STOPS = "http://transportapi.com/v3/uk/places.json?lat={0}&lon={1}&type=bus_stop&app_id={2}&app_key={3}"
API_NEXT_BUSES = "http://transportapi.com/v3/uk/bus/stop/{0}/live.json&app_id={1}&app_key={2}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-postcode', type=str)
    parser.add_argument('-stopcode', type=str)
    parser.add_argument('-app_id', type=str)
    parser.add_argument('-app_key', type=str)
    args = parser.parse_args()

    lat, lon = get_lat_lon(args.postcode)
    bus_stops = get_bus_stops(args.app_id, args.app_key, lat, lon)
    get_next_buses(args.app_id, args.app_key, bus_stops[0])


def get_lat_lon(postcode: str) -> Tuple:
    resp = requests.get(url=API_POSTCODES.format(postcode))

    if 200 <= resp.status_code <= 299:
        data = resp.json()
        return data["result"]["latitude"], data["result"]["longitude"]
    else:
        raise Exception("Failed to get lon/lat: status {0}".format(resp.status_code))


def get_bus_stops(app_id, app_key, lat: float, lon: float) -> List[Dict]:
    resp = requests.get(url=API_NEARBY_STOPS.format(lat, lon, app_id, app_key))

    if 200 <= resp.status_code <= 299:
        return [member for member in resp.json()["member"]]
    else:
        raise Exception("Failed to get bus stops: status {0}".format(resp.status_code))


def get_next_buses(app_id, app_key, bus_stop: dict):
    print(bus_stop["atcocode"])
    resp = requests.get(url=API_NEXT_BUSES.format(bus_stop["atcocode"], app_id, app_key))

    if 200 <= resp.status_code <= 299:
        data = resp.json()
        pprint(data)
    else:
        raise Exception("Failed to get next buses: status {0}".format(resp.status_code))


if __name__ == "__main__":
    main()
