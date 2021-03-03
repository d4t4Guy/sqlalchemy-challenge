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

#define start date as one year before latest date in observations, and station_id as most active station
begin_date = '2016-08-23'
station_id = 'USC00519281'




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
        f"Available Routes:<br/><br/>"
        f'<a href="/api/v1.0/precipitation">/api/v1.0/precipitation - precipitation trend </a> <br/><br/><br/>'
        f'<a href="/api/v1.0/stations">/api/v1.0/stations - basic info on stations </a> <br/><br/><br/>'
        f'<a href="/api/v1.0/tobs">/api/v1.0/tobs - observed temperature trend </a> <br/> <br/> <br/> <br/><br/><br/><br/><br/>'
        f"Interactive points, enter date in iso-format (YYYY-MM-DD) <br/><br/>"
        f"/api/v1.0/&LTstart&GT        - min/max/avg temps for all dates >= start date <br/><br/>"
        f"/api/v1.0/&LTstart&GT/&LTend&GT - min/max/avg temps for date range on closed interval (both start and end dates included)<br/><br/>"
        )



       
@app.route("/api/v1.0/precipitation")
def precipitation():
 # # JSON precipitation query
            # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation for past year
    results = session.query(Measurement.date, func.sum(Measurement.prcp).label('Daily_Prcp')) \
    .filter(Measurement.date > begin_date).group_by(Measurement.date)
    
    session.close()

    # convert results into a dictionary
    daily_prcp_dict = dict(results) 
    return jsonify(daily_prcp_dict)        
        
        
@app.route("/api/v1.0/stations")
def stations():    
        # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(
                        Station.station
                        , Station.name
                        , Station.latitude
                        , Station.longitude
                        , Station.elevation
                        ).all()
    session.close()

    # Convert results into list
    all_stations=[]
    for station, name, latitude, longitude, elevation in results:
        station_dict={}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)
    
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():   
    session = Session(engine)
    # # 1. Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(
    Measurement.date, Measurement.tobs.label('Temperature')) \
    .filter(Measurement.date > begin_date) \
    .filter(Measurement.station==station_id)

    session.close()
        # # 2. Return a JSON list of temperature observations (TOBS) for the previous year.
    
        # convert results into a dictionary
    tobs_dict = dict(results) 
    return jsonify(tobs_dict)
 
@app.route("/api/v1.0/<start_date>")
def temperature_after(start_date):
        # # min/max/avg temps for all dates >= start date


    session = Session(engine)
    temperature_aggs = session.query (func.min(Measurement.tobs).label("min_temp")
                                ,func.max(Measurement.tobs).label("max_temp")
                                ,func.avg(Measurement.tobs).label("avg_temp")
                                ).filter(Measurement.station==station_id).filter(Measurement.date >= start_date)
    session.close()                             
    # place returned data in dictionary so that it can be JSONified
    temp_dict = {}
    temp_dict["min_temp"] = temperature_aggs[0][0]
    temp_dict["max_temp"] = temperature_aggs[0][1]
    temp_dict["avg_temp"] = temperature_aggs[0][2]

    return jsonify(temp_dict) #not sure if jsonify is required here, results seem to be same as dictionary
     
@app.route("/api/v1.0/<start_date>/<end_date>")
def temperature_between(start_date, end_date):
        # # min/max/avg temps for all dates >= start date


    session = Session(engine)
    temperature_aggs = session.query (func.min(Measurement.tobs).label("min_temp")
                                ,func.max(Measurement.tobs).label("max_temp")
                                ,func.avg(Measurement.tobs).label("avg_temp")
                                ).filter(Measurement.station==station_id).filter(Measurement.date.between(start_date, end_date))
    session.close()                             

    # place returned data in dictionary so that it can be JSONified
    temp_dict = {}
    temp_dict["min_temp"] = temperature_aggs[0][0]
    temp_dict["max_temp"] = temperature_aggs[0][1]
    temp_dict["avg_temp"] = temperature_aggs[0][2]

    return jsonify(temp_dict) #not sure if jsonify is required here, results seem to be same as dictionary
     
     
     
     
     # /api/v1.0/<start>/<end>
        # # min/max/avg temps for date range on closed interval (both endpoints included)

#start the server
if __name__ == '__main__':
    app.run(debug=True)