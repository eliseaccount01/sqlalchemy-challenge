import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station 

# Flask Setup

app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query precipitation 
    sel = [Measurement.date, Measurement.prcp]
    date = dt.datetime(2016,8,23)
    precipitation = session.query(*sel).filter(Measurement.date >= date).all()

    #Close session
    session.close()

    #Change tuple into a normal list 
    precipitation_list= list(np.ravel(precipitation))

    #Create a dictionary 
    precipitation_dict = {
        "date":precipitation_list
        }

    #return JSON 
    return jsonify(precipitation_dict)
    

@app.route("/api/v1.0/stations")
def stations():
# Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all Stations
    station_names = session.query(Station.station)

    #Close session 
    session.close()

    # Convert list of tuples into normal list
    station_list = [station for station in station_names]
    print(station_list)

    #Return JSON 
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
# Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the dates and temperature observations from a year from the last data point
    date = dt.datetime(2016,8,23)
    temperatures = session.query(Measurement.tobs).filter(Measurement.date >= date).all()
    
    session.close()

    # Convert list of tuples into normal list
    temperatures = [temp[0] for temp in temperatures]
    print(temperatures)

    #Return JSON 
    return jsonify(temperatures)


@app.route("/api/v1.0/<start>")
def start(start):

 # Create our session (link) from Python to the DB
    session = Session(engine)
    start = start.replace("","")
#Return JSON 
    stats =(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all())

    #Close Session 
    session.close()

    return jsonify(stats)

@app.route("/api/v1.0/<start>/<end>")
# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def start_end(start, end):

     # Create our session (link) from Python to the DB
    session = Session(engine)
    start = start.replace("","")
    end= end.replace("","")
    
    #Return JSON 
    stats = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all())

#Close session    
    session.close()

#Function usage 
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True) 


