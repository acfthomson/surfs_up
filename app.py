# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask
from flask import Flask, jsonify

# Set up database engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create variables for each of the classes so they can be referenced later
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to database
session = Session(engine)

# Set up Flask app
app = Flask(__name__)

# Define routes
# Root route
@app.route("/")

# Add routing information for each of the other routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Add precipitation route
@app.route("/api/v1.0/precipitation")

# Create precipitation function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create stations route
@app.route("/api/v1.0/stations")

# Create a stations function
def stations():
    results = session.query(Station.station).all()
    # Unravel results into a one-dimensional array and convert to a list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Create temperature observations route
@app.route("/api/v1.0/tobs")

# Create a temp_monthly function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query primary station for all tobs from the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= prev_year).all()
    # Unravel results into a one-dimensional array
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create route for summary statistics
@app.route("/api/v1.0/temp/start")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create a stats function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


