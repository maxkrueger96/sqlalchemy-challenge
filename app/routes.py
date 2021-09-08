import pandas as pd
from datetime import datetime as dt
from sqlalchemy import func
from sqlalchemy.orm import Session
from flask import jsonify
from Script.script import p_scores, station_measure, year_temps, Measurement, engine
from app import app

e = engine

# welcomes the user, provides urls
@app.route("/")
def hello_user():
    return (
    f"Welcome to my app.<br/> \
        Here is a list of all available routes:<br/><br/> \
            /api/v1.0/precipitation<br/> \
            /api/v1.0/stations<br/> \
            /api/v1.0/tobs<br/> \
            /api/v1.0/YYYY-MM-DD/<start><br/> \
            /api/v1.0/YYYY-MM-DD/<start>/<end>"
)

# queries the average precipitation over the past year
# writes it into a DataFrame -> Dictionary -> JSON
@app.route("/api/v1.0/precipitation")
def prcp_dict():

    q = p_scores
    df = pd.read_sql_query(q.statement, e,index_col="date")
    into_dict = df["round_1"].to_dict()

    return jsonify(into_dict)

# queries a list of 
@app.route("/api/v1.0/stations")
def stations():

    q = station_measure
    df = pd.read_sql_query(q.statement, e,index_col="station")
    into_dict = df["name"].to_dict()
        
    return jsonify(into_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    
    q = year_temps

    df = pd.read_sql_query(q.statement, e,index_col="date")
    into_dict = df["tobs"].to_dict()
        
    return jsonify(into_dict)

@app.route("/api/v1.0/YYYY-MM-DD/<start>")
def start_only(start):

    session = Session(e)
    q = session.query(Measurement.date, func.min(Measurement.tobs), 
        func.round(func.avg(Measurement.tobs),1), func.max(Measurement.tobs)).\
        filter(Measurement.date >= dt.fromisoformat(start)).\
        order_by(Measurement.date).\
        group_by(Measurement.date)
    session.close()

    df = pd.read_sql_query(q.statement,e,index_col="date")
    into_dict = dict.fromkeys(list(df.index))

    for d in list(df.index):
        into_dict[d] = {"TMIN": df["min_1"].loc[df.index == d].values[0],
        "TAVG": df["round_1"].loc[df.index == d].values[0], 
        "TMAX": df["max_1"].loc[df.index == d].values[0]}
    
    return jsonify(into_dict)


@app.route("/api/v1.0/YYYY-MM-DD/<start>/<end>")
def start_end(start,end):

    session = Session(e)
    q = session.query(Measurement.date, func.min(Measurement.tobs), 
    func.round(func.avg(Measurement.tobs),1), func.max(Measurement.tobs)).\
    filter(Measurement.date >= dt.fromisoformat(start)).\
    filter(Measurement.date <= dt.fromisoformat(end)).\
    order_by(Measurement.date).\
    group_by(Measurement.date)
    session.close()

    df = pd.read_sql_query(q.statement,e,index_col="date")
    into_dict = dict.fromkeys(list(df.index))

    for d in list(df.index):
        into_dict[d] = {"TMIN": df["min_1"].loc[df.index == d].values[0],
                "TAVG": df["round_1"].loc[df.index == d].values[0], 
                "TMAX": df["max_1"].loc[df.index == d].values[0]}
    
    return jsonify(into_dict)