import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import desc

from flask import Flask, jsonify, request


###########################################
# Database Setup
###########################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/start?<br/>" 
        f"/api/v1.0/start?/end?"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Retrieve the last 12 months of precipitation data"""
    results = (session
               .query(Measurement.date, Measurement.prcp)
               .filter(Measurement.date > "2016-08-22")
               .order_by(Measurement.date)
               .all()
               )
    # Create dictionary
    last_12_months = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        last_12_months.append(prcp_dict)
    return jsonify(last_12_months)

@app.route("/api/v1.0/stations")
def stations():
    """Retrieve a JSON list of stations from the dataset"""
    results = (session
               .query(Measurement.station)
               .group_by((Measurement.station))
               .all()
               )
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return dates & temps from a year before last datapoint"""
    results = (session
               .query(Measurement.date, Station.tobs)
               .filter(Measurement.date > "2016-08-22")
               .order_by(Measurement.date)
               .all()
               )
     # Create dictionary
     # For some reason, this code does not work, though in theory it should be exactly the same as the precipitation code?
    last_12_temps = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        last_12_temps.append(tobs_dict)
    return jsonify(last_12_temps)


@app.route("/api/v1.0/start?start_date")
def vacation_dates_start():
    """Return JSON list of min, avg, and max temp
    for a given start or start-end range.
    For start date only, calculate for all dates >= start."""
    # How do I specify user input for this query? Do I use the dates package?
    
    start_date = request.args.get('start_date')
    results = (session
                .query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))
                .filter(Measurement.date >= start_date)
                .order_by(Measurement.date)
                .all()
                )
   
    trip_summary = [] 
    # Not sure how to specify the values that are operated on here
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        trip_summary.append(prcp_dict)
    return jsonify(trip_summary)

@app.route("/api/v1.0/api/v1.0/start?start_date/end_date")
def vacation_dates_start_end():
    """Return JSON list of min, avg, and max temp
    for a given start or start-end range.
    
    For start & end, calculate between, inclusive"""

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    results = (session
                .query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))
                .filter(Measurement.date >= start_date)
                .filter(Measurement.date <= end_date)
                .order_by(Measurement.date)
                .all()
                )
    trip_summary = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        trip_summary.append(prcp_dict)
    return jsonify(trip_summary)

if __name__ == '__main__':
    app.run(debug=False)
