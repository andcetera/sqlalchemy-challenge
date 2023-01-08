
# Import Dependencies
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

# Define function to get annual data
def twelve_mo()->dt.date:

    # Create new session link
    session = Session(engine)

    # Get the most recent date in the dataset
    most_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Close session once query is complete
    session.close()

    # Calculate the date one year from the last date in data set
    last = dt.datetime.strptime(most_recent, "%Y-%m-%d").date()
    year = last - dt.timedelta(days=365)

    return year



# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():

    # Print request info to terminal for debugging info    
    print("Server received request for 'Home' page...")
    # List all available routes
    return """  AVAILABLE ROUTES:
                /api/v1.0/precipitation (annual measurment data) -- 
                /api/v1.0/stations (station name list) -- 
                /api/v1.0/tobs (temperature observations) -- 
                FOR QUERIES BY DATE:
                /api/v1.0/*start-date -- 
                /api/v1.0/*start-date/*end-date
                """

@app.route("/api/v1.0/precipitation")
def precip():

    # Print request info to terminal for debugging info
    print("Server received request for 'Precipitation' page...")

    # Create new session link
    session = Session(engine)

    # Perform a query to retrieve the date and precipitation scores
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= twelve_mo())

    # Close session once query is complete
    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    prcp = dict(data)

    # Return the JSON representation of your dictionary
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stns():

    # Print request info to terminal for debugging info    
    print("Server received request for 'Stations' page...")

    # Create new session link
    session = Session(engine)

    # Query the database for the station names
    stn_query = session.query(Station.name)

    # Close session once query is complete
    session.close()

    # Convert results to list format
    stations = [s.name for s in stn_query]

    # Return a JSON list of stations from the dataset
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # Print request info to terminal for debugging info
    print("Server received request for 'Temperature Observations' page...")

    # Create new session link
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the previous year of data
    # Get info for the most active station
    most_active = session.query(func.count(Measurement.station).label('count'), Measurement.station)\
        .group_by(Measurement.station).order_by(desc('count')).first()

    station_info = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active.station).filter(Measurement.date >= twelve_mo())

    # Close session once queries are complete
    session.close()

    tobs = dict(station_info)

    # Return a JSON list of temperature observations (TOBS) for the previous year
    return jsonify(tobs)

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