from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    # List all available routes
    return "home page"

@app.route("/api/v1.0/precipitation")
def precip():
    print("Server received request for 'Precipitation' page")
    # Convert the query results to a dictionary using date as the key and prcp as the value
    # Return the JSON representation of your dictionary
    return "prcp page"

@app.route("/api/v1.0/stations")
def stns():
    print("Server received request for 'Stations' page")
    # Return a JSON list of stations from the dataset
    return "stns page"

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature Observations' page")
    # Query the dates and temperature observations of the most active station for the previous year of data
    # Return a JSON list of temperature observations (TOBS) for the previous year
    return "tobs page"

@app.route("/api/v1.0/<start>")

@app.route("/api/v1.0/<start>/<end>")

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive)



if __name__ == "__main__":
    app.run(debug=True)