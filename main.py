from flask import Flask, render_template, request
import argparse
import bus
from pprint import pprint

app = Flask(__name__)
args = None


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/busInfo")
def busInfo():
    postcode = request.args.get('postcode').replace(' ', '')

    try:
        lat, lon = bus.get_lat_lon(postcode)
        bus_stops = bus.get_bus_stops(args.app_id, args.app_key, lat, lon)[:2]
        buses = []

        for i, stop in enumerate(bus_stops):
            departures_closest = bus.get_next_buses(args.app_id, args.app_key, bus_stops[i])
            buses.append([(dep["operator_name"], dep["aimed_departure_time"]) for dep in departures_closest])

        bus_times = [(stop["name"], stop["distance"], buses[i]) for i, stop in enumerate(bus_stops)]

        return render_template('info.html', postcode=postcode, bus_times=bus_times)

    except Exception as e:
        return render_template('info.html', postcode=postcode, error_message="No buses found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-postcode', type=str)
    parser.add_argument('-app_id', type=str)
    parser.add_argument('-app_key', type=str)
    args = parser.parse_args()

    app.run()
