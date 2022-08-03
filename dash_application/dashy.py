import sqlite3

import dash
import numpy as np
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Output, Input

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

#external_stylesheets = [
#    {
#        "href": "https://fonts.googleapis.com/css?family=Inconsolata&display=swap",
#        "rel": "stylesheet",
 #   },
#]

def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dashy/",
                         external_stylesheets=['/static/dist/css/styles.css'],
                         meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                         suppress_callback_exceptions=True)
    dash_app.title = "Theatre Dashboard"

    dash_app.layout = html.Div(children=[
    html.Div(children=[
        #html.Img(img src = "/static/img/logo.png"    class ="logo"),
        html.Img(src=dash_app.get_asset_url('logo.jpeg'),
        id='logo.jpeg', style={'marginTop': '5px', 'marginBottom': '10px', 'height': '80px'})
    ], id='header', className='row flex-display', style={'textAlign': 'center'}),

    html.Div(children=[
        html.H3(children="Theatre Dashboard", style={'marginTop': '-15px', 'marginBottom': '8px',
                                                             'color': 'white'}),
        html.H6(children='SURGEONS PROCEDURES', style={'marginTop': '-15px', 'marginBottom': '10px'})
        ], id='sub_header', className='row flex-display', style={'textAlign': 'center'}),

  #########################################
    # CARDS: Number statistics

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.P("Total Surgery: "),
                html.P(f"{data['specialty'].value_counts().sum()}",
                        style={'paddingTop': '.3rem', 'color': '#00aeef'}),
            ], className="one-third column", id="title"),

            html.Div(children=[
                html.P("Top Cases: " ),
                html.P(f"{data['operation'].value_counts().nlargest(3).to_string()}",
                       style={'paddingTop': '.3rem', 'color': '#00aeef'}),
            ], className="one-third column", id="title1"),

            html.Div(children=[
                html.P("Top Surgeons: ", className='fix_label'),
                html.P(f"{data['surgeon'].value_counts().nlargest(3).to_string()}",
                       style={'paddingTop': '.3rem', 'color': '#00aeef'}),
            ], className="one-third column", id="title2"),

        ], style={'margin': '1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '90%',
                  'flex-wrap': 'wrap', 'textAlign': 'center', 'paddingBottom': '.05rem'},
        className='create_container three columns  bg-grey')]),

        ################### Filter box ######################
    html.Div(children=[
        html.Div(children=[
            html.H4('Pick a Specialty:', className='fix_label',
                   ),
            dcc.Dropdown(
                id='specialty-filter',
                options=[
                    {"label": specialty, "value": specialty}
                    for specialty in np.sort(data.specialty.unique())
                ],
                value="O&G",
                clearable=False,
                placeholder="Specialty",
                className="dcc_coupon", style={'display':True}
            ),

            html.P('Pick a Period:', style={'paddingTop': '3rem'}),
            dcc.DatePickerRange (
                id='input_date',
                min_date_allowed=data.input_date.min().date(),
                max_date_allowed=data.input_date.max().date(),
                start_date=data.input_date.min().date(),
                end_date=data.input_date.max().date(),
                style={'display':True, 'paddingTop': '2rem'},
                className='SingleDatePickerInput__withBorder bg-grey')
        ], className='create_container three column'),
    ], style={'margin': '1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '90%',
                  'flex-wrap': 'wrap', 'textAlign': 'center'},
        className="create_container three columns  bg-grey"),

    html.Div(children=[
        # Bar chart for operations done
        html.Div(children=[
            dcc.Graph(id='surgeon')
        ], className="six columns widget-box"),

        html.Div(children=[
            dcc.Graph(id='amount_paid')
        ], className="six columns widget-box")

    ], className='row flex_display'),],
        id='mainContainer',
        style={"display": "flex", "flex-direction": "column"})


# In[5]:


######### Callback for top statistics ##############################
    @dash_app.callback(
        [Output("surgeon", "figure"), Output("amount_paid", "figure")],
        [
            Input("specialty-filter", "value"),
            Input("input_date", "start_date"),
            Input("input_date", "end_date"),
        ],
    )
    ################################## I stopped here

    #def update_charts(specialty, start_date, end_date):
    #    mask = (
    #        (data.specialty == specialty)
    #        & (data.input_date >= start_date)
    #       & (data.input_date <= end_date)
    #    )
        # filter by speed limits
    #    df_update = data.loc[
    #        (specialty[0] <= data['specialty']) & (specialty[1] >= data['specialty'])]

    #    days = data.strptime(end_date, "%Y-%m-%d") - data.strptime(start_date, "%Y-%m-%d")

    #    return len(df_update), sum(df_update['Number of Surgeries']), sum(df_update['weekly operation']), days.days

    ############Bar chart table

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
                    "y": data['specialty'].value_counts(),
                    "x": filtered_data["operation"],
                    "color": "surgeon",
                    "type": "bar",



                },
            ],
            "layout": {
                "title": {
                    "text": "Total Procedures by Surgeon",
                    "color": "white",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": { "fixedrange": True},
                "colorway": ["blue"],
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
                "colorway": ["green"],
                "template": 'plotly_dark',
                "paper_bgcolor": 'rgba(0, 0, 0, 0)',
                "plot_bgcolor": 'rgba(0, 0, 0, 0)',

            },
        }
        return surgeon_chart, revenue_chart



    return dash_app
