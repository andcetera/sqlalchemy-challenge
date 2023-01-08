# Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import datetime as dt
from flask import Flask, jsonify

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table in the database
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)


# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():

    # Print request info to terminal for debugging info    
    print("Server received request for 'Home' page...")
    # List all available routes
    return "/api/v1.0/precipitation"

@app.route("/api/v1.0/precipitation")
def precip():

    # Print request info to terminal for debugging info
    print("Server received request for 'Precipitation' page...")

    # Calculate the date one year from the last date in data set.
    most_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last = dt.datetime.strptime(most_recent, "%Y-%m-%d").date()
    twelve_mo = last - dt.timedelta(days=365)

    # Perform a query to retrieve the date and precipitation scores
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= twelve_mo)

    # Convert the query results to a dictionary using date as the key and prcp as the value
    prcp = dict(data)

    # Return the JSON representation of your dictionary
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stns():

    # Print request info to terminal for debugging info    
    print("Server received request for 'Stations' page...")

    # Query the database for the station names
    stations = session.query(Station.name)
    stations = [s.name for s in stations]
    print(stations)
    # Return a JSON list of stations from the dataset
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # Print request info to terminal for debugging info
    print("Server received request for 'Temperature Observations' page...")
    # Query the dates and temperature observations of the most active station for the previous year of data
    # Return a JSON list of temperature observations (TOBS) for the previous year
    return "tobs page"

@app.route("/api/v1.0/<start>")
def start_date():

    # Print request info to terminal for debugging info
    print("Server received request for 'Start Date' search...")
    return "start"

@app.route("/api/v1.0/<start>/<end>")
def daterange():

    # Print request info to terminal for debugging info
    print("Server received request for 'Date Range' search...")
    return "range"
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive)

if __name__ == "__main__":
    app.run(debug=True)