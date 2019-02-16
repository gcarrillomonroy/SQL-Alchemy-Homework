import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
#session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all measurements"""
    # Query all dates
    #session.merge()
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    all_results = []

    for result in results:
        result_dict = {}
        result_dict[result.date] = result.prcp
        all_results.append(result_dict)

    session.close()
    return jsonify(all_results)

@app.route("/api/v1.0/stations")
def station():
    """Return a list of all stations"""
    # Query all stations
    #session.merge()
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    all_results = []

    for result in results:
        result_dict = {}
        result_dict[result.station] = result.name
        all_results.append(result_dict)

    session.close()
    return jsonify(all_results)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all tobs from last year"""
    # Query all stations
    #session.merge()
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date.date

    # Calculate the date 1 year ago from the last data point in the database
    last_date = dt.date(int(last_date[0:4]), int(last_date[5:7]), int(last_date[8:10])) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_date).order_by(Measurement.date.asc()).all()

    all_results = []

    for result in results:
        result_dict = {}
        result_dict[result.date] = result.tobs
        all_results.append(result_dict)

    session.close()
    return jsonify(all_results)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    """Return temperature min, average and max for specific date"""
    # Query for specific date
    #session.merge()
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date == start_date)

    all_results = []

    for result in results:
        result_dict = {}
        result_dict['Min Temp'] = result[0]
        result_dict['Avg Temp'] = result[1]
        result_dict['Max Temp'] = result[2]
        all_results.append(result_dict)
    session.close()
    return jsonify(all_results)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    """Return temperature min, average and max for specific date"""
    # Query for specific date
    #session.merge()
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)

    all_results = []

    for result in results:
        result_dict = {}
        result_dict['Min Temp'] = result[0]
        result_dict['Avg Temp'] = result[1]
        result_dict['Max Temp'] = result[2]
        all_results.append(result_dict)
    session.close()
    return jsonify(all_results)

if __name__ == '__main__':
    app.run(debug=True)
