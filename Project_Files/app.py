
# Import Dependencies
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Reflect existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table in the database
Measurement = Base.classes.measurement
Station = Base.classes.station


# Define function to get annual data
def twelve_mo(session:Session)->dt.date:

    # Get the most recent date in the Measurement table
    most_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Calculate the date one year from the last date in dataset
    last = dt.datetime.strptime(most_recent, "%Y-%m-%d").date()
    year_ago = last - dt.timedelta(days=365)

    return year_ago


# Define function to check if user entered dates are usable
def validate(date:str)->None:

    # Convert user input to datetime to see if it fits our required format
    try:
        dt.datetime.strptime(date, '%Y-%m-%d')

    # If not, return a descriptive error go let user know what to do
    except ValueError:
        raise ValueError('Incorrect date format, should be YYYY-MM-DD')


# Flask Setup
app = Flask(__name__)


# FLASK ROUTES

@app.route("/")
def home():

    # Print request info to terminal for tracking    
    print("Server received request for 'Home' page...")

    # List all available routes
    return jsonify(['AVAILABLE ROUTES', 
    {'Annual Precipitation Data (All Stations)': '/api/v1.0/precipitation'}, 
    {'Station Name List': '/api/v1.0/stations'}, 
    {'Temperature Observations (Most Active Station)': '/api/v1.0/tobs'}, 
    'FOR TEMPERATURE QUERIES BY DATE', {'Returns: Min, Avg, Max': '*** YYYY-MM-DD FORMAT ONLY ***'}, 
    {'Results from start-date until end of dataset:': '/api/v1.0/<start-date>'}, 
    {'Results from start-date thru end-date:': '/api/v1.0/<start-date>/<end-date>'}])


@app.route("/api/v1.0/precipitation")
def precip():

    # Print request info to terminal for tracking
    print("Server received request for 'Precipitation' page...")

    # Create new session link
    session = Session(engine)

    # Perform a query to retrieve the date and precipitation measures
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= twelve_mo(session))

    # Close session once query is complete
    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    prcp = dict(data)

    # Return the JSON representation of our dictionary
    return jsonify(prcp)


@app.route("/api/v1.0/stations")
def stns():

    # Print request info to terminal for tracking    
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

    # Print request info to terminal for tracking
    print("Server received request for 'Temperature Observations' page...")

    # Create new session link
    session = Session(engine)

    # Get info for the most active station
    most_active = session.query(func.count(Measurement.station), Measurement.station)\
        .group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()

    # Query the dates and temperature observations of the most active station for the previous year of data
    station_info = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active.station).filter(Measurement.date >= twelve_mo(session))

    # Close session once queries are complete
    session.close()

    # Convert results to dictionary format
    tobs = dict(station_info)

    # Return a JSON list of temperature observations (TOBS) for the previous year
    return jsonify(tobs)


@app.route("/api/v1.0/<start>")
def start_date(start):

    # Print request info to terminal for tracking
    print("Server received request for 'Start Date' search...")

    validate(start)

    # Create new session link
    session = Session(engine)

    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
    .filter(Measurement.date >= start).all()

    # Close session once queries are complete
    session.close()

    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range
    return jsonify({'min': temps[0][0], 'avg': round(temps[0][1], 1), 'max': temps[0][2]})


@app.route("/api/v1.0/<start>/<end>")
def daterange(start, end):

    # Print request info to terminal for tracking
    print("Server received request for 'Date Range' search...")

    validate(start)
    validate(end)

    # Create new session link
    session = Session(engine)

    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive)
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
    .filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Close session once queries are complete
    session.close()

    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range
    return jsonify({'min': temps[0][0], 'avg': round(temps[0][1], 1), 'max': temps[0][2]})

# Run the code when the app name is called in the terminal
if __name__ == "__main__":
    app.run(debug=True)
