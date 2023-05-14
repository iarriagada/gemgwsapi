#!/usr/bin/env python3

import epics
import os
import time
from flask import Flask, jsonify

app = Flask(__name__)

os.environ["EPICS_CA_ADDR_LIST"] = "172.17.2.45"

gws_key = {
    "ws:cpWindSpeed":"wind_speed",
    "ws:cpTemp50m":"temperature",
    "ws:cpHumid":"humidity",
    "ws:cpWindDir":"wind_dir"
}

gws_api_dict = {
    "temperature":{"value":None, "timestamp":None, "unit":"C"},
    "humidity":{"value":None, "timestamp":None, "unit":"%"},
    "wind_speed":{"value":None, "timestamp":None, "unit":"m/s"},
    "wind_dir":{"value":None, "timestamp":None, "unit":"deg"},
}

greetings = [
    {"id":1, "name":"Hola", "lang":"espanol"},
    {"id":2, "name":"Hello", "lang":"english"},
    {"id":3, "name":"Kipa", "lang":"chileno"}
]

@app.get("/greetings")
def get_greetings():
    return jsonify(greetings)

@app.get("/gws_values")
def get_gws_values():
    return jsonify(gws_api_dict)

def connect_epics_chans(chan_dict):
    # Create the EPICS channels dictionary
    epics_chans = {chan:epics.PV(chan) for chan in chan_dict}
    print(epics_chans.keys())
    time.sleep(0.25) # Give it some time for the channels to connect
    for c in epics_chans:
        # caget one round for the values of all channels.
        # TODO: Automatic retries
        print(f"{c}= {epics_chans[c].value}")
    return epics_chans

def mon_epics_chans(epics_chans, epics_key, api_dict):
    for c in epics_chans:
        api_dict[epics_key[c]]['value'] = epics_chans[c].value
        epics_chans[c].add_callback(on_change,
                                    key=epics_key,
                                    vals=api_dict)

def on_change(pvname=None, value=None, timestamp=None, **kw):
    kw['vals'][kw['key'][pvname]]['value'] = value
    kw['vals'][kw['key'][pvname]]['timestamp'] = timestamp


if __name__ == '__main__':
    print('Starting websocket!!!')
    epics_chans = connect_epics_chans(gws_key)
    mon_epics_chans(epics_chans, gws_key, gws_api_dict)
    app.run(host="0.0.0.0", port=8888)

