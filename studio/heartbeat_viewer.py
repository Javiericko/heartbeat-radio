import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from datetime import datetime
import time

from studio.serializers import SensorSerializer, HeartbeatSerializer
from studio.models import Sensor, Heartbeat

app = DjangoDash('HeartbeatRadio', external_stylesheets=[dbc.themes.BOOTSTRAP])


card_main = dbc.Card(id='sensor', color="success", inverse=True)

app.layout = html.Div([
    html.H1(children='HeartBeat Radio'),
    dbc.Row([dbc.Col(card_main, width=3)], justify="center"),
])


@app.callback(
    Output("sensor", "children"),
    [Input('sensor', 'children')]
)
def update_heartbeat(value):
    # Get heartbeats from the database
    heartbeat = Heartbeat.objects.latest("date_created")
    serializer = HeartbeatSerializer(heartbeat, many=False)
    if serializer.is_valid:
        # Parse the fields from this hearbeat so we can query for the sensor data
        serial_number = serializer.data['serial_number']
        date_created = serializer.data['date_created']
        date_created = datetime.strptime(date_created, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m/%d/%y at %H:%M:%S') # Format date

        # Get the sensor related to this heartbeat
        sensor = Sensor.objects.get(serial_number=serial_number)
        serializer = SensorSerializer(sensor, many=False)
        if serializer.is_valid:
            name = serializer.data['name']
            location = serializer.data['location']

    card = dbc.CardBody([
                html.H4(f"Sensor: {name}", className="card-title"),
                html.P(f"Location: {location}", className="card-text"),
                html.P(f"Last heartbeat: {date_created}", className="card-text"),
            ]
        )

    return card