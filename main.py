from flask import Flask, render_template, request
import argparse
import bus

app = Flask(__name__)
args = None


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/busInfo")
def busInfo():

    postcode = request.args.get('postcode')

    lat, lon = bus.get_lat_lon(postcode)
    bus_stops = bus.get_bus_stops(args.app_id, args.app_key, lat, lon)
    departures_closest = bus.get_next_buses(args.app_id, args.app_key, bus_stops[0])

    buses_closest = [(dep["operator_name"], dep["aimed_departure_time"]) for dep in departures_closest]
    bus_stop_names = [(stop["name"], stop["distance"], buses_closest) for stop in bus_stops]
    #bus_info = [stop['distance', 'description']]


    return render_template('info.html', postcode=postcode, bus_stop_names=bus_stop_names)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-postcode', type=str)
    parser.add_argument('-app_id', type=str)
    parser.add_argument('-app_key', type=str)
    args = parser.parse_args()

    app.run()
