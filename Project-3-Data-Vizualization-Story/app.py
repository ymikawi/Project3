#################################################
# Hi Project Team!!
# This is a PLACEHOLDER for our Flask App.
#################################################


import os

import pandas as pd
import numpy as np

#import sqlalchemy
#from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import Session
#from sqlalchemy import create_engine

# from flask import Flask, jsonify, render_template
#from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()

from config import remote_db_endpoint, remote_db_port, remote_dbname, remote_dbuser, remote_dbpwd

from flask import Flask, jsonify, render_template, request, flash, redirect, json
app = Flask(__name__)

#################################################
# Database Setup
#################################################

# AWS Database Connection
engine = create_engine(f"mysql://{remote_dbuser}:{remote_dbpwd}@{remote_db_endpoint}:{remote_db_port}/{remote_dbname}")

# Create a remote database engine connection
conn = engine.connect()

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
# db = pd.read_csv("LatandLng2.csv")

# reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# # Save references to each table
# Samples_Metadata = Base.classes.sample_metadata
# Samples = Base.classes.samples

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return foreclosure list."""
    
    # # Use Pandas to perform the sql query
    # stmt = db.session.query(Samples).statement
    # df = pd.read_sql_query(stmt, db.session.bind)
    # Return a list of the column names (sample names)
    data_df = pd.read_sql("SELECT * FROM foreclosure_data_final", conn)
    
    names = data_df.to_dict('records')
    
    print(names)
    return jsonify(names)

@app.route("/foreclosure_data")
def foreclosure_data():
    """Return foreclosure list."""
    

    # # Use Pandas to perform the sql query
    # stmt = db.session.query(Samples).statement
    # df = pd.read_sql_query(stmt, db.session.bind)


    # Return a list of the column names (sample names)

    data_df = pd.read_sql("SELECT * FROM foreclosure_data_final", conn)


    # OPTION 1 -- return json
    data_json = data_df.to_json()
    return data_json

    # OPTION 2 -- return json records; list of dicts
    #data_json = data_df.to_json(orient='records')
    #return data_json

    # OPTION 3 -- jsonify dictionary
    #data_dict = data_df.to_dict()
    #return jsonify(data_dict)
    # WARNING: This approach contains the keys. If you want to get only the values, use
    # Object.values() in your JS file

# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""
#     sel = [
#         Samples_Metadata.sample,
#         Samples_Metadata.ETHNICITY,
#         Samples_Metadata.GENDER,
#         Samples_Metadata.AGE,
#         Samples_Metadata.LOCATION,
#         Samples_Metadata.BBTYPE,
#         Samples_Metadata.WFREQ,
#     ]

#     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

#     # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         sample_metadata["sample"] = result[0]
#         sample_metadata["ETHNICITY"] = result[1]
#         sample_metadata["GENDER"] = result[2]
#         sample_metadata["AGE"] = result[3]
#         sample_metadata["LOCATION"] = result[4]
#         sample_metadata["BBTYPE"] = result[5]
#         sample_metadata["WFREQ"] = result[6]

#     print(sample_metadata)
#     return jsonify(sample_metadata)


# @app.route("/samples/<sample>")
# def samples(sample):
#     """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Filter the data based on the sample number and
#     # only keep rows with values above 1
#     sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
#     # Format the data to send as json
#     data = {
#         "otu_ids": sample_data.otu_id.values.tolist(),
#         "sample_values": sample_data[sample].values.tolist(),
#         "otu_labels": sample_data.otu_label.tolist(),
#     }
#     return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
