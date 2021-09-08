from IPython import get_ipython

import pandas as pd
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

db = "sqlite:///Database/hawaii.sqlite"
engine = create_engine(db)
Base = automap_base()
Base.prepare(engine, reflect = True)
Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine) 
dates_des = session.query(Measurement.date).\
        order_by(Measurement.date.desc())
session.close()

last_date = dates_des.first().date
last_date_dt = dt.datetime.strptime(last_date, "%Y-%m-%d")
prev_year = last_date.replace("2017", "2016")
prev_year_dt = dt.datetime.strptime(prev_year, "%Y-%m-%d")

session = Session(engine) 
p_scores = session.query(Measurement.date, func.round(func.avg(Measurement.prcp),4)).\
        filter(Measurement.date >= prev_year_dt - dt.timedelta(days=1)).\
        order_by(Measurement.date).\
        group_by(Measurement.date)
session.close()  

p_df = pd.read_sql_query(p_scores.statement,engine)
p_df.set_index("date",inplace=True)
p_df.rename(columns={"round_1":"avg_prcp"},inplace=True)
p_df.sort_values("date")

session = Session(engine) 
stations = session.query(Station.station)
session.close()

station_num = stations.count()

session = Session(engine) 
station_measure = session.query(Measurement.station, Station.name,func.count(Measurement.date)).\
        group_by(Station.name).\
        order_by(func.count(Measurement.date).desc()).\
        join(Station, Station.station == Measurement.station)
session.close()

station_meas = station_measure.all()

session = Session(engine) 
station_temp = session.query(Measurement.station, func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        group_by(Measurement.station).\
        filter(Measurement.station == station_meas[0][0])
session.close()

session = Session(engine) 
year_temps = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= prev_year_dt - dt.timedelta(days=1)).\
        filter_by(station= station_meas[0][0])
session.close()   

temp_df= pd.read_sql_query(year_temps.statement,engine)




