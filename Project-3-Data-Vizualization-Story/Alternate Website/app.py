import argparse

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as pg


from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()

from config import remote_db_endpoint, remote_db_port, remote_dbname, remote_dbuser, remote_dbpwd

#################################################
# Database Setup
#################################################

# AWS Database Connection
engine = create_engine(f"mysql://{remote_dbuser}:{remote_dbpwd}@{remote_db_endpoint}:{remote_db_port}/{remote_dbname}")

# Create a remote database engine connection
conn = engine.connect()
data = pd.read_sql("SELECT * FROM foreclosure_data_final", conn)

# parser = argparse.ArgumentParser()
# parser.add_argument("input")
# args = parser.parse_args()
# data = pd.read_excel(args.input, index_col=0)
app = dash.Dash()
app.layout = html.Div(
    children=[
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(
                    label="Map",
                    children=[
                        dcc.Graph(
                            id="map",
                            figure=pg.Figure(
                                [
                                    pg.Scattergeo(
                                        locationmode="USA-states",
                                        lon=data["lgn"],
                                        lat=data["lat"],
                                        text=(
                                            "Region name: " + data["region_name"]
                                            + "<br>Principal amount: " + data["principal_amount"].astype(str)
                                            + "<br>Auction location: " + data["auction_location"].astype(str)
                                            + "<br>Date of auction: " + data["date_of_auction"].astype(str)
                                            + "<br>Auction time: " + data["auction_time"].astype(str)
                                            + "<br>Deposit: " + data["deposit"].astype(str)
                                            + "<br>Z street address: " + data["zstreet_address"].astype(str)
                                        ),
                                        hoverinfo="text",
                                        mode="markers",
                                    )
                                ],
                                pg.Layout(
                                    autosize=True,
                                    geo=dict(
                                        scope="north america", # USA
                                        center=dict(
                                            lat=data["lat"].mean(), lon=data["lgn"].mean()
                                        ),
                                        projection=dict( type='albers usa', scale=5 ),
                                        framewidth=50,
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5,
                                    ),
                                )
                            )
                        )
                    ]
                ),
                dcc.Tab(
                    label="Table",
                    children=[
                        dash_table.DataTable(
                            id="table",
                            columns=[
                                {"name": col, "id": col, "deletable": False}
                                for col in data.columns
                            ],
                            data=(
                                data
                                    .astype({"date_of_auction": str})
                                    .to_dict("rows")
                            ),
                            sorting=True,
                            sorting_type="multi"
                        )
                    ]
                )
            ]
        )

    ]
)


if __name__ == "__main__":
    app.run_server()


        # dcc.Graph(
        #     figure=pg.Figure(
        #         [
        #             pg.Scattergeo(
        #                 locationmode="USA-states",
        #                 lon=data["lgn"],
        #                 lat=data["lat"],
        #                 text=(
        #                     "Region name: " + data["region_name"]
        #                     + "<br>Principal amount: " + data["principal_amount"].astype(str)
        #                     + "<br>Auction location: " + data["auction_location"].astype(str)
        #                     + "<br>Date of auction: " + data["date_of_auction"].astype(str)
        #                     + "<br>Auction time: " + data["auction_time"].astype(str)
        #                     + "<br>Deposit: " + data["deposit"].astype(str)
        #                     + "<br>Z street address: " + data["zstreet_address"].astype(str)
        #                 ),
        #                 hoverinfo="text",
        #                 mode="markers"
        #             )
        #         ],
        #         pg.Layout(
        #             geo=dict(
        #                 scope="usa",
        #                 center=dict(
        #                     lat=data["lat"].mean(), lon=data["lgn"].mean()
        #                 ),
        #             )
        #         )
        #     )
        # ),
        # dash_table.DataTable(
        #     columns=[
        #         {"name": col, "id": col, "deletable": False}
        #         for col in data.columns
        #     ],
        #     data=(
        #         data
        #             .astype({"date_of_auction": str})
        #             .to_dict("rows")
        #     ),
        #     sorting=True,
        #     sorting_type="multi"
        # )
