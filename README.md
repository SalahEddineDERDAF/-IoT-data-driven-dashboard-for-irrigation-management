# IoT-data-driven-dashboard-for-irrigation-management
This project presents the development of a Streamlit-based dashboard for irrigation management, designed to demonstrate how machine learning can support water-efficient farming practices. The dashboard uses datasets collected from IoT sensors (measuring soil moisture, air temperature, and humidity) to simulate real-time decision-making for irrigation.
It allows users to:

📊 Visualize environmental data through dynamic graphs and tables

🌍 View parcel locations and irrigation status on an interactive map

🤖 Receive irrigation recommendations (pump ON/OFF) powered by a Random Forest Classifier

📈 Analyze trends in soil moisture and weather conditions for better planning

While the dashboard itself is not connected directly to IoT devices, it demonstrates how IoT-collected data can be leveraged to train ML models and inform irrigation strategies, supporting more sustainable agriculture and efficient water use.

✅ Step 3: Create the Dashboard File
In Colab, create a new file called irrigation_dashboard.py.

This file will contain the Streamlit code for the dashboard.

✅ Step 4: Import the Dataset
Upload the training dataset ModelDevDataset.csv into the Colab environment.

This dataset will be used to train and evaluate the ML model.

✅ Step 5: Add the Dashboard Code
Copy and paste your dashboard code into the irrigation_dashboard.py file.

This will define the layout and functionality of the dashboard.

✅ Step 6: Obtain the Public IP Address
Run the following command in Colab:

bash
Copy
Edit
!wget -q -O - ipv4.icanhazip.com
This retrieves the public IP address of your Colab session.

✅ Step 7: Launch the Streamlit App
Run:

bash
Copy
Edit
!streamlit run irrigation_dashboard.py & npx localtunnel --port 8501
This will start the Streamlit app.

Localtunnel will create a public URL to access it.

✅ Step 8: Access the Dashboard
Copy the public URL from the Colab output (e.g. https://35.237.141.55:8501) and open it in your browser.

✅ Step 9: Upload Test Dataset
Upload the test dataset testDataset.csv into Colab.

This dataset simulates real-time IoT sensor data for testing the dashboard.

✅ Step 10: Close the Dataset Import Tab
Close the dataset import tab in Streamlit to improve the dashboard visualization experience.

