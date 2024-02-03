import streamlit as st
import os

# Define the parameter values and their configurations
parameter_values = {
    'a_e': [0.2, 0.5, 0.8],
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

# Use st.sidebar for sliders
with st.sidebar:
    st.title("Parameter Sliders")

    # Create sliders dynamically based on parameter_values
    slider_values = {}
    config_values = {}
    for param, values in parameter_values.items():
        # Only create sliders for parameters with more than one possible value
        if len(values) > 1:
            min_val, max_val = min(values), max(values)
            step = values[1] - values[0]  # Assuming values are sorted
            st.markdown(f"#### ${param}$")
            slider_values[param] = st.slider(f"${param}$", min_val, max_val, min_val, step=step, format='%g',label_visibility="hidden")
            config_values[param] = slider_values[param]
        else: config_values[param] = values[0]


# Display the image based on the selected configuration
selected_image_path_parts = []
for param, value in config_values.items():
    img_val = round(value, 3)
    selected_image_path_parts.append(f'{param}{img_val}')

selected_image_path = os.path.join(image_directory, ''.join(selected_image_path_parts))

#-> selected_image_path = os.path.join(image_directory, ''.join([f'{param}{value}' for param, value in config_values.items()]))

selected_image_path = selected_image_path.replace('.', '')
selected_image_path += '.png'

# Display the unencoded image in the main area
if os.path.exists(selected_image_path):
    st.title("Selected Image:")
    st.image(selected_image_path, use_column_width=True, caption=selected_image_path)
else:
    st.warning("Selected image not found.")

st.write(selected_image_path)

# Display the selected configuration in the main area
st.title("Selected Configuration:")
st.write(config_values)