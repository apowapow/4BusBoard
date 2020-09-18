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
    # lat, lon = bus.get_lat_lon(args.postcode)
    # bus_stops = bus.get_bus_stops(args.app_id, args.app_key, lat, lon)
    # departures = bus.get_next_buses(args.app_id, args.app_key, bus_stops[0])

    postcode = request.args.get('postcode')
    return render_template('info.html', postcode=postcode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-postcode', type=str)
    parser.add_argument('-app_id', type=str)
    parser.add_argument('-app_key', type=str)
    args = parser.parse_args()

    app.run()
