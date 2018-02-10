from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import warnings
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from pandas import DataFrame
from datetime import timedelta
import datetime
from datetime import datetime
from flask import Flask, jsonify
import json 
import decimal, datetime

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii4.sqlite")
print("Connected to DB")

# reflect an existing database into a new model
AutomapBase = automap_base()
# reflect the tables
AutomapBase.prepare(engine, reflect=True)
print("Reflected tables")

# Save reference to the table
Measurement = AutomapBase.classes.Measurement
Station = AutomapBase.classes.Station

# Create our session (link) from Python to the DB
session = Session(engine)


app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def percipitation():
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>='2017-01-01').all()
    
    all_results = []
    for measurement in results:
        result_dict = {}
        result_dict["date"] = measurement.date
        result_dict["tobs"] = measurement.tobs
        all_results.append(result_dict)
        
    return jsonify(all_results)

@app.route("/api/v1.0/stations")
def stations():
    """ Return a list of all station names
    """
    # Query all passengers
    results1 = session.query(Station.station).all()


    all_station = [record.station for record in results1]
    

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    """ Return a list of all  temperatrues from the previous year
    """
    # Query all passengers
    results2 = session.query(Measurement.tobs).filter(Measurement.date>="2017-01-01").all()


    all_tobs = [record.tobs for record in results2]
    

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start1(start):

    start_date1 = datetime.datetime.strptime(start, "%Y-%m-%d")

    result3 = session.query(func.min(Measurement.tobs).label('Min_start'), func.max(Measurement.tobs).label('Max_start'), func.avg(Measurement.tobs).label('Avg_start')).filter(Measurement.date> start_date1).first()

    return jsonify(result3)
    # return jsonify(result3.Max_start)
    # return jsonify(result3.Avg_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end1(start,end):

    start_date2 = datetime.datetime.strptime(start, "%Y-%m-%d")
    end_date2 = datetime.datetime.strptime(end, "%Y-%m-%d")
    result4 = session.query(func.min(Measurement.tobs).label('Min_start1'), func.max(Measurement.tobs).label('Max_start1'), func.avg(Measurement.tobs).label('Avg_start1')).filter(Measurement.date>=start_date2).filter(Measurement.date<= end_date2).first()
    return jsonify(result4)
    

    

if __name__ == '__main__':
    app.run(debug=True)