from dash import Dash, dcc, html, Input, Output, State
import requests

sendKey = "T4CZZ5NJYHQJC0ZR"
url = "https://api.thingspeak.com/update"

app = Dash(__name__)

app.layout = html.Div([
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit')
])


@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def send_string(n_clicks, value):
    payload = {'field1': value, 'api_key': sendKey}
    try:
        # Sends an HTTP GET request
        response = requests.get(url, params=payload)
        # The library can also decode JSON responses
        response = response.json()
    except:
            print("Connection Failed")
    return 'The input value was "{}"'.format(
        value
    )


if __name__ == '__main__':
    app.run_server(debug=True)
