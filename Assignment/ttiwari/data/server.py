from flask import Flask
import processing
from flask_cors import CORS, cross_origin
app=Flask(__name__)
cors = CORS(app)
@app.route("/staticvisualdata")
@cross_origin()
#for i in range(len(processing.avg_rent_county)):

def staticvisualdata():
    return processing.county_details

@app.route("/interactivevisualdata")
@cross_origin()
#for i in range(len(processing.avg_rent_county)):

def interactivevisualdata():
    return processing.interactive
if __name__=="__main__":
    app.run(debug=True)
