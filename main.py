import os
import tkinter as tk
import requests
from datetime import datetime
import pytz
import timezonefinder
from tkinter import font

# Create the GUI
root = tk.Tk()
root.title("Weather App")


#Defining the default open size
window_width = 564
window_height= 1002
root.geometry(f"{window_width}x{window_height}")


# Default background image
defaultbg = tk.PhotoImage(file="Images/bc4d86d78f407cab596f599e52c2011c.png")
root.defaultbg = defaultbg  # Store the PhotoImage instance as an attribute of the root window

bglabel = tk.Label(root, image=root.defaultbg)
bglabel.place(relwidth=1, relheight=1)


# OpenWeather API key
api_key = "071e0ef2abeddaba3d9488779a5c7f3e"




# Function to get the timezone
def get_timezone(lat, lon):
    tf = timezonefinder.TimezoneFinder()
    tz_str = tf.timezone_at(lng=lon, lat=lat)
    return tz_str


#Getting font from google
font_link = "https://fonts.google.com/specimen/Anton?preview.size=30&category=Serif,Sans+Serif,Display,Monospace&sort=popularity"
font_label =  tk.Label(root, text="preloading", font =("Anton", 1))
font_label.pack()


#Making a font object to use
my_font = font.Font(family="Anton", size=15)

# Function to convert Unix time to 12-hour time in local time
def unix_to_normalhrs(unix_time, timezone):
    dt = datetime.fromtimestamp(unix_time, tz=pytz.timezone(timezone))
    return dt.strftime('%I:%M %p')


# Function to get the weather for a given city
def get_weather(city):
    # Make a GET request to the OpenWeather API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract latitude and longitude for getting timezone
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        timezone = get_timezone(lat, lon)

        # Extract the relevant information from the response
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure" ]/ 3.8639
        wind_speed = data["wind"]["speed" ]*2.23
        wind_direction = data["wind"]["deg"]
        sunrise = unix_to_normalhrs(data["sys"]["sunrise"], timezone)
        sunset = unix_to_normalhrs(data["sys"]["sunset"], timezone)


#making the main info frame
        info_frame = tk.Frame(root)
        info_frame.pack (pady=10)


        # Display the weather information
        tk.Label(info_frame, text=f"City: {city_name}", font=("my_font", 12, "bold")).pack(anchor="w")
        tk.Label(info_frame, text=f"Weather: {weather_desc}", font=("my_font", 10)).pack(anchor="w")
        tk.Label(info_frame, text=f"Humidity: {humidity}%", font=("my_font", 10)).pack(anchor="w")
        tk.Label(info_frame, text=f"Pressure: {pressure:.2f} inHg", font=("my_font", 10)).pack(anchor="w")
        tk.Label(info_frame, text=f"Wind Speed: {wind_speed:.2f} mph, Direction: {wind_direction}°",
                 font=("Helvetica", 10)).pack(anchor="w")
        tk.Label(info_frame, text=f"Sunrise: {sunrise}, Sunset: {sunset}", font=("Helvetica", 10)).pack(anchor="w")
    else:
        # Display an error message
        result_label.config(text="Error fetching weather information.")




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
