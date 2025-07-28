# IoT-data-driven-dashboard-for-irrigation-management
This project presents the development of a Streamlit-based dashboard for irrigation management, designed to demonstrate how machine learning can support water-efficient farming practices. The dashboard uses datasets collected from IoT sensors (measuring soil moisture, air temperature, and humidity) to simulate real-time decision-making for irrigation.
It allows users to:

📊 Visualize environmental data through dynamic graphs and tables

🌍 View parcel locations and irrigation status on an interactive map

🤖 Receive irrigation recommendations (pump ON/OFF) powered by a Random Forest Classifier

📈 Analyze trends in soil moisture and weather conditions for better planning

While the dashboard itself is not connected directly to IoT devices, it demonstrates how IoT-collected data can be leveraged to train ML models and inform irrigation strategies, supporting more sustainable agriculture and efficient water use.

-Step 1: Install Required Libraries
Run these commands in a Colab code cell:

!pip install streamlit -q
!pip install plotly
!pip install folium
!pip install streamlit-autorefresh

-Step 2: Create the Dashboard File
In Colab, create a new file called irrigation_dashboard.py.

This file will contain the Streamlit code for the dashboard.

-Step 3: Import the Dataset
Upload the training dataset ModelDevDataset.csv into the Colab environment.

This dataset will be used to train and evaluate the ML model.

-Step 4: Add the Dashboard Code
Copy and paste your dashboard code into irrigation_dashboard.py.

This defines the layout and functionality of the dashboard.

-Step 5: Obtain the Public IP Address
Run the following command in Colab:

!wget -q -O - ipv4.icanhazip.com
➡️ This retrieves the public IP address of your Colab session.

-Step 6: Launch the Streamlit App
Run:
!streamlit run irrigation_dashboard.py & npx localtunnel --port 8501
This starts the Streamlit app.

Localtunnel generates a public URL to access the dashboard.

-Step 7: Access the Dashboard
Copy the public URL from the Colab output (e.g. https://35.237.141.55:8501) and open it in your browser.

-Step 8: Upload the Test Dataset
Upload the testDataset.csv file into Colab.

This dataset simulates real-time IoT sensor data for testing the dashboard.

-Step 9: Close the Dataset Import Tab
Close the dataset import tab in Streamlit to improve the visualization experience.
