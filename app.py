from flask import Flask, json, jsonify
import analysis as ana

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
def prcp_dict():
    q = ana.p_scores
    df = ana.pd.read_sql_query(q.statement, ana.engine,index_col="date")
    into_dict = df["prcp"].to_dict()
    return jsonify(into_dict)


@app.route("/api/v1.0/stations")
def stations():
    q = ana.station_measure
    df = ana.pd.read_sql_query(q.statement, ana.engine,index_col="station")
    into_dict = df["name"].to_dict()
    return jsonify(into_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    q = ana.year_temps
    df = ana.pd.read_sql_query(q.statement, ana.engine,index_col="date")
    into_dict = df["tobs"].to_dict()
    return jsonify(into_dict)

@app.route("/api/v1.0/<start>")
def start_only(start):
    q = ana.session.query(ana.Measurement.date, ana.func.min(ana.Measurement.tobs), 
        ana.func.round(ana.func.avg(ana.Measurement.tobs),1), ana.func.max(ana.Measurement.tobs)).\
        filter(ana.Measurement.date >= start).\
        order_by(ana.Measurement.date).\
        group_by(ana.Measurement.date)
    df = ana.pd.read_sql_query(q.statement,ana.engine,index_col="date")
    into_dict = dict.fromkeys(list(df.index))
    for d in list(df.index):
        into_dict[d] = {"TMIN": df["min_1"].loc[df.index == d].values[0],
        "TAVG": df["round_1"].loc[df.index == d].values[0], 
        "TMAX": df["max_1"].loc[df.index == d].values[0]}
    return jsonify(into_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    q = ana.session.query(ana.Measurement.date, ana.func.min(ana.Measurement.tobs), 
    ana.func.round(ana.func.avg(ana.Measurement.tobs),1), ana.func.max(ana.Measurement.tobs)).\
    filter(ana.Measurement.date >= start).\
    filter(ana.Measurement.date <= end).\
    order_by(ana.Measurement.date).\
    group_by(ana.Measurement.date)
    df = ana.pd.read_sql_query(q.statement,ana.engine,index_col="date")
    into_dict = dict.fromkeys(list(df.index))
    for d in list(df.index):
        into_dict[d] = {"TMIN": df["min_1"].loc[df.index == d].values[0],
                "TAVG": df["round_1"].loc[df.index == d].values[0], 
                "TMAX": df["max_1"].loc[df.index == d].values[0]}
    return jsonify(into_dict)