import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from dash.dependencies import Output, Input
import sqlite3

##### Import functions for db from myfunctions.py
# from myfunctions import run_query, run_command

conn = sqlite3.connect('qiudata.db')
data = pd.read_sql_query('SELECT input_date, surgeon, specialty, operation, amount_paid FROM patients',
                         conn,
                         parse_dates=['input_date'])


#data = pd.read_csv("/home/hod/Desktop/patients_data.csv")

#data["input_date"] = pd.to_datetime(data["input_date"])
#data.sort_values('input_date', inplace=True)
#sfig = data['specialty'].value_counts().plot(kind='bar', figsize=(14,6))
#md = data.groupby(['specialty'])['amount_paid'].sum()
#md = md.plot(kind='bar', figsize=(15,7), title = 'Number of Cases by Specialty',xlabel='Specialty',
#             ylabel = 'Number of Cases')

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css?family=Inconsolata&display=swap",
        "rel": "stylesheet",
    },
]



def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dashy/",
                         external_stylesheets=external_stylesheets)

    dash_app.title = "Theatre Dashboard"

    dash_app.layout = html.Div(
        children=[

            html.Div(children=[
                    html.Img(src=dash_app.get_asset_url('logo.jpeg'),
                    id='logo.jpeg', style={'marginTop': '5px', 'marginBottom': '10px', 'height': '80px'})
                ], style={'textAlign': 'center'}),

            html.Div(
                children=[
                    html.P(children="logo.jpeg", className="header-logo"),
                    html.H1(
                        children="SURGEONS PROCEDURE", className="header-title"
                    ),
                    html.P(
                        children="DETAILS OF PROCEDURES",
                        className="header-description",
                    ),
                ], style={'textAlign': 'center'}
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children="Specialty", className="menu-title"),
                            dcc.Dropdown(
                                id="specialty-filter",
                                options=[
                                    {"label": specialty, "value": specialty}
                                    for specialty in np.sort(data.specialty.unique())
                                ],
                                value="O&G",
                                clearable=False,
                                className="dropdown",
                            ),
                        ]
                    ),

                    html.Div(
                        children=[
                            html.Div(
                                children="Date",
                                className="menu-title"
                                ),
                            dcc.DatePickerRange(
                                id="input_date",
                                min_date_allowed=data.input_date.min().date(),
                                max_date_allowed=data.input_date.max().date(),
                                start_date=data.input_date.min().date(),
                                end_date=data.input_date.max().date(),
                            ),
                        ]
                    ),
                ],
                className="menu",
            ),
            html.Div(
                children=[
                    html.Div(
                        children=dcc.Graph(
                            id="surgeon", config={"displayModeBar": False},
                        ),
                        className="card",
                    ),
                    html.Div(
                        children=dcc.Graph(
                            id="amount_paid", config={"displayModeBar": False},
                        ),
                        className="card",
                    ),
                ],
                className="wrapper",
            ),
        ]
    )


    @dash_app.callback(
        [Output("surgeon", "figure"), Output("amount_paid", "figure")],
        [
            Input("specialty-filter", "value"),
            Input("input_date", "start_date"),
            Input("input_date", "end_date"),
        ],
    )
    def update_charts(specialty, start_date, end_date):
        mask = (
            (data.specialty == specialty)
            & (data.input_date >= start_date)
            & (data.input_date <= end_date)
        )
        filtered_data = data.loc[mask, :]
        surgeon_chart = {
            "data": [
                {
                    "y": filtered_data["operation"].value_counts(),
                    "x": filtered_data["operation"],
                    "color": "surgeon",
                    "type": "bar",



                },
            ],
            "layout": {
                "title": {
                    "text": "Total Procedures by Surgeon",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": { "fixedrange": True},
                "colorway": ["#17B897"],
                "template": 'plotly_dark',
                "paper_bgcolor": 'rgba(0, 0, 0, 0)',
                "plot_bgcolor": 'rgba(0, 0, 0, 0)',
            },
        }

        revenue_chart = {
            "data": [
                {
                    "x": filtered_data["surgeon"],
                    "y": filtered_data["amount_paid"],
                    "type": "bar",
                    "hovertemplate": "₦%{y:.2f}<extra></extra>",
                    "template": "plotly_dark",
                    "autosize": True,
                },
            ],
            "layout": {
                "title": {"text": "Revenue by Surgeon", "x": 0.05, "xanchor": "left"},
                "xaxis": {"fixedrange": True},
                "yaxis": {"fixedrange": True},
                "colorway": ["#E12D39"],
                "template": 'plotly_dark',
                "paper_bgcolor": 'rgba(0, 0, 0, 0)',
                "plot_bgcolor": 'rgba(0, 0, 0, 0)',
            },
        }
        return surgeon_chart, revenue_chart

    return dash_app
