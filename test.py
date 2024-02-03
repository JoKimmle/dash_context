import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os
import base64


app = dash.Dash(__name__)

# Define the parameter values and their configurations
parameter_values = {'a_e': [0.2, 0.5, 0.8],
  'v_c': [125.60000000000001, 157, 188.4],
  'f_z': [0.0208, 0.026, 0.0312],
  'a_p': [1, 2],
  'd': [5],
  'flutes': [2],
  'direct': [0, 1]
  }

# Define the image directory
image_directory = 'images'
image_list = [f for f in os.listdir(image_directory) if f.endswith('.png')]

app.layout = html.Div([
    html.H1("Parameter Dashboard"),

    # Create sliders dynamically based on parameter_values
    *[dcc.Slider(
        id=f'{param}_slider',
        min=min(values),
        max=max(values),
        step=None,  # Disables continuous sliding
        marks={val: str(val) for val in values},
        value=min(values),
        tooltip={'placement': 'bottom', 'always_visible': True}
    ) for param, values in parameter_values.items()],

    # Display the selected configuration
    html.Div(id='selected-configuration'),

    # Display the image based on the selected configuration
    html.Img(id='selected-image'),

])

# Callback to update the selected configuration
@app.callback(
    Output('selected-configuration', 'children'),
    [Input(f'{param}_slider', 'value') for param in parameter_values.keys()]
)
def update_selected_configuration(*values):
    return f"Selected Configuration: {dict(zip(parameter_values.keys(), values))}"

# Callback to update the selected image
@app.callback(
    Output('selected-image', 'src'),
    [Input(f'{param}_slider', 'value') for param in parameter_values.keys()]
)
def update_selected_image(*values):
    # Create a filename based on the selected configuration
    filename = ''.join([f'{param}:{value}' for param, value in zip(parameter_values.keys(), values)]) + '.png'
    image_path = os.path.join(image_directory, filename)

    # Read and encode the image
    encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode('ascii')

    # Construct the data URI
    data_uri = f'data:image/png;base64,{encoded_image}'

    return data_uri

if __name__ == '__main__':
    app.run_server(debug=True)
