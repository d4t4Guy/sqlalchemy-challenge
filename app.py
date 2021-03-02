# Homework 10 part two: Flask app

#d/b and ORM support
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    # List all available api routes.
    return (
        f"Available Routes:<br/>"
        f'<a href="/api/v1.0/precipitation">/api/v1.0/precipitation - precipitation trend </a> <br/>'
        f'<a href="/api/v1.0/stations">/api/v1.0/stations - basic info on stations </a> <br/>'
        f'<a href="/api/v1.0/tobs">/api/v1.0/tobs - observed temperature trend </a> <br/> <br/> <br/> <br/>'
        f"Interactive points, enter date in iso-format (YYYY-MM-DD) <br/>"
        f"/api/v1.0/&LTstart&GT        - min/max/avg temps for all dates >= start date <br/>"
        f"/api/v1.0/&LTstart&GT/&end&GT - min/max/avg temps for date range on closed interval (both start and end dates included)<br/>"
        )



       
@app.route("/api/v1.0/precipitation")
def precipitation():
 # # JSON precipitation query
            # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation
    results = session.query(Measurement.date, func.sum(Measurement.prcp).label('Daily_Prcp')) \
    .group_by(Measurement.date) \
    
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)    
        
        
        
@app.route("/api/v1.0/stations")
def stations():    
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Passenger.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def tobs():    # /api/v1.0/tobs
    return
        # # 1. Query the dates and temperature observations of the most active station for the last year of data.
        # # 2. Return a JSON list of temperature observations (TOBS) for the previous year.
        
#@app.route("/api/v1.0/<start_date>")
# def temperature_after():
        # # min/max/avg temps for all dates >= start date
     
     # /api/v1.0/<start>/<end>
        # # min/max/avg temps for date range on closed interval (both endpoints included)

#start the server
if __name__ == '__main__':
    app.run(debug=True)