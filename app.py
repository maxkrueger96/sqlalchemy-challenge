from flask import Flask, jsonify
from analysis import Measurement, Station, p_scores, measure_station, 

app = Flask(__name__)

@app.route("/")
def hello_user():
    return (
"Welcome to my app.\n",

"Here is a list of all available routes:\n\n",

    "List of precipitation measures over the past year from every station, averaged by day:\n"
    f"/api/v1.0/precipitation"

    "List of station ids and names:\n"
    f"/api/v1.0/stations\n"

    "List of temperature observations made by the most active station last year:" 
    f"/api/v1.0/tobs\n" 

    "Minimum temperature, mean temperature, and maximum temperature, starting from a given date: "
    f"/api/v1.0/<start>\n"

    "Minimum temperature, mean temperature, and maximum temperature between start and end dates:"
    f"/api/v1.0/<start>/<end>\n\n"
    )

@app.route("/api/v1.0/precipitation")


@app.route("/api/v1.0/stations")


@app.route("/api/v1.0/tobs")


@app.route("/api/v1.0/<start>")


@app.route("/api/v1.0/<start>/<end>")
