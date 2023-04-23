import tkinter as tk
import requests

# OpenWeather API key
api_key = "071e0ef2abeddaba3d9488779a5c7f3e"

# Function to get the weather for a given city
def get_weather(city):
    # Make a GET request to the OpenWeather API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the relevant information from the response
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        # Display the weather information
        result_label.config(text=f"The weather in {city_name} is {temp:.1f}°C and {weather_desc}.")
    else:
        # Display an error message
        result_label.config(text="Error fetching weather information.")

# Create the GUI
root = tk.Tk()
root.title("Weather App")

# Create the input field and button
input_label = tk.Label(root, text="Enter a city:")
input_label.pack(pady=10)
input_entry = tk.Entry(root)
input_entry.pack()
button = tk.Button(root, text="Get Weather", command=lambda: get_weather(input_entry.get()))
button.pack(pady=10)

# Create the label to display the weather information
result_label = tk.Label(root, text="")
result_label.pack()

# Start the GUI
root.mainloop()
