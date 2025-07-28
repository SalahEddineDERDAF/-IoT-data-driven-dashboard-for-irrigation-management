# Import essential libraries 
import streamlit as st # For creating and managing web applications (Daschboard)
import pandas as pd # For data manipulation and analysis
import plotly.express as px # For creating interactive plots
import folium # For generating interactive maps
import numpy as np # For numerical operations
import streamlit.components.v1 as components # For embedding custom HTML and javaScript in the web application
from sklearn.model_selection import train_test_split # For splitting data into training and test sets
from sklearn.ensemble import RandomForestClassifier  # For using the RandomForest algorithm for classification 
from joblib import dump, load # For saving and loading trained models
from datetime import datetime, timedelta # For handling date and time data
from streamlit_autorefresh import st_autorefresh # For automatically refreshing the dashboard
import plotly.graph_objs as go#  access to graphical object classes
# Load the data using pandas
file_path = '/content/ModelDevDataset.csv'
data_df = pd.read_csv(file_path)

# Split the data into features (X) and target (y)
X = data_df[['Soil Moisture', 'Temperature', 'Air Humidity']]  # Features
y = data_df['Pump Data']  # Target variable to be classified

# Split the data into training and testing sets with 20% of the data reserved for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)

# Save the trained model
model_filename = 'rf_model.joblib'
dump(rf_model, model_filename)

# Configure the streamlit dashboard to use the full width of the web page
st.set_page_config(layout="wide")

# Refresh the Streamlit app every 6000 milliseconds (6 seconds) using the st_autorefresh function
st_autorefresh(interval=6000, key='datarefresh')

# Use streamlit’s cache mechanism to efficiently load a machine learning model
@st.cache_resource
def load_model():
  model = load('rf_model.joblib')
  return model

# Load the SVM model from the file system
rf_model = load_model()

# Initialize or retrieve the session state index which keeps track of pagination or row index in data displays
if 'index' not in st.session_state:
    st.session_state['index'] = 0

# Create a sidebar widget for file upload, allowing users to upload CSV files for data input
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=['csv'])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data['Time'] = pd.date_range(start=datetime.now(), periods=len(data), freq='1min')
    # Use the loaded model to predict the statut of Pump based on the uploaded data
    features = data[['Soil Moisture', 'Temperature', 'Air Humidity']]
    data['Pump Data'] = rf_model.predict(features)
    data['Irrigation'] = data['Pump Data'].map({1: 'On', 0: 'Off'})
else:
    # Display an error message if no file is uploaded and halt further execution of the app
    st.error("Please upload a CSV file.For better visualization of the dashboard, please close the file upload dialog.")
    st.stop()
    

# Set the main title of the dashboard
st.title('Irrigation monotoring')

# Create two columns for 2 sections of the dashboard : Maps and table of variables
col1, col2 = st.columns([3, 2])

with col1:
    st.header("Parcel Locations")
    # Define the base map using folium centered at specific coordinates

    m = folium.Map(location=[54.887360, -2.065662], zoom_start=15)
    locations = [(54.887360, -2.065662), (54.889350, -2.067652)]
    # Loop over defined locations to place markers on the map
    

    for (lat, lon), idx in zip(locations, [0, 1]):
        parcel_data = data.iloc[st.session_state['index'] + idx]
        label = f"Parcel {idx+1}"
        popup_text = f"<strong>Parcel {idx+1}</strong><br><strong>Soil Moisture:</strong> {parcel_data['Soil Moisture']}<br><strong>Temperature:</strong> {parcel_data['Temperature']}<br><strong>Humidity:</strong> {parcel_data['Air Humidity']}<br><strong>Irrigation:</strong> {parcel_data['Irrigation']}"
        # Create a Marker with a permanent label
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                icon_size=(150,36),
                icon_anchor=(75,18),
                html=f'<div style="font-size: 12pt; color: black;">{label}</div>',
            )
        ).add_to(m)
        # Create another Marker for the popup details
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=250),
            icon=folium.Icon(icon='cloud', color='blue')  # Change to appropriate icon
        ).add_to(m)

    components.html(m._repr_html_(), height=300)

with col2:
    st.header("Irrigation Status")
    # Define custom HTML and CSS for styling a table to display weather data and irrigation recommendations

    table_style = """
    <style>
    .styled-table {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    .styled-table thead tr {
        background-color: #009879;
        color: #ffffff;
        text-align: left;
    }
    .styled-table th, .styled-table td {
        padding: 12px 15px;
        height: 60px;  /* Adjust this value to increase the height of the table rows */
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }
    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #009879;
    }
    .styled-table tbody tr.active-row {
        font-weight: bold;
        color: #009879;
    }
    </style>
    """
    # Construct the HTML for the table and populate it with data dynamically

    table_html = f"{table_style}<table class='styled-table'><thead><tr><th>Parcel Number</th><th>Soil Moisture (Ohm)</th><th>Temperature (°C)</th><th>Air Humidity (%)</th><th>Irrigation</th></tr></thead><tbody>"
    for idx in range(2):  # Display data for Parcel 1 and Parcel 2
        row = data.iloc[st.session_state['index'] + idx]
        table_html += f"<tr><td>Parcel {idx+1}</td><td>{row['Soil Moisture']} Ohm</td><td>{row['Temperature']} °C</td><td>{row['Air Humidity']} %</td><td>{row['Irrigation']}</td></tr>"
    table_html += "</tbody></table>"

    # Embed the custom HTML into the dashboard
    components.html(table_html, height=350)  

# Define metrics to be displayed in the time-series analysis

metrics = ["Soil Moisture", "Temperature", "Air Humidity"]
# Provide titles for the graphs to be displayed, adding more context for users

metric_titles = {
    "Soil Moisture": "Soil Moisture Levels (Ohm)",
    "Temperature": "Temperature Variation (°C)",
    "Air Humidity": "Air Humidity Percentage (%)"
}
# Define the units for each metric

metric_units = {
    "Soil Moisture": "Ohm",
    "Temperature": "°C",
    "Air Humidity": "%"
}

# Create columns in Streamlit for displaying each metric's graph

graph_cols = st.columns(len(metrics))

# Loop through each metric to create and display corresponding plots

for i, metric in enumerate(metrics):
    with graph_cols[i]:
        plot_data = data.iloc[:st.session_state['index'] + 2].copy()  # Create a copy of data for plotting
        plot_data['Parcel'] = np.where(plot_data.index % 2 == 0, 'Parcel 1', 'Parcel 2')  # Assign parcel numbers

        # Initialize a plotly graph object for interactive time-series plotting
        fig = go.Figure()

        # Loop through unique parcels and plot time-series data for each, coloring lines differently
        for parcel in plot_data['Parcel'].unique():
            df = plot_data[plot_data['Parcel'] == parcel]
            color = '#1B4F72' if parcel == 'Parcel 1' else '#85C1E9'
            fig.add_trace(go.Scatter(x=df['Time'], y=df[metric], mode='lines',
                                     name=parcel,
                                     line=dict(color=color, width=2)))

        # Update plot layout with title, axis labels, and annotations for mean values
        mean_values = plot_data.groupby('Parcel')[metric].mean()
        annotations = [dict(
            x=1.0, y=-0.25,  # Position for 'Average' label
            xanchor='right', yanchor='top', xref='paper', yref='paper',
            text="Avg",
            showarrow=False,
            font=dict(size=14, color='black'),
            bgcolor='rgba(255, 255, 255, 0.8)'  # Semi-transparent background for readability
        )]
        # Add annotations for mean values of each parcel
        for idx, (parcel, mean_value) in enumerate(mean_values.items()):
            annotations.append(dict(
                x=1.0, y=-0.3 - 0.07 * idx,  # Positioning for mean value labels
                xanchor='right', yanchor='top', xref='paper', yref='paper',
                text=f"{mean_value:.2f} {metric_units[metric]}",
                showarrow=False,
                font=dict(size=12),
                bgcolor='rgba(255, 255, 255, 0.5)',  # Semi-transparent background
            ))

        # Apply updates to the layout of the figure
        fig.update_layout(
            title=metric_titles[metric],  # Title of the graph
            title_x=0.3,  # Center the title
            yaxis_title=f"{metric} ({metric_units[metric]})",  # Label for the Y-axis with units
            legend=dict(
                x=0, y=-0.3, xanchor='left', yanchor='top',
                bgcolor='rgba(255, 255, 255, 0.5)',  # Background color for the legend
                borderwidth=1
            ),
            annotations=annotations,  # Add annotations to the layout
            margin=dict(l=0, r=0, t=50, b=40),  # Set margins around the plot
            plot_bgcolor='rgba(0,0,0,0)'  # Set the background color of the plot area to transparent
        )

        # Display the configured plot in the Streamlit app using the full width of the container
        st.plotly_chart(fig, use_container_width=True)

# Increment the session state index to update which rows of data are shown, looping back if the end is reached
st.session_state['index'] += 2 if st.session_state['index'] + 2 < len(data) else 0
