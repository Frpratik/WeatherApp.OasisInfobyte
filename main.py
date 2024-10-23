import requests
import tkinter as tk
from tkinter import messagebox, StringVar
from PIL import Image, ImageTk
import io
import geocoder  

def get_weather(api_key, location, unit='metric'):
    """Fetch weather data for a specified location."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={unit}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_current_location():
    """Use geocoder to get the user's current location based on IP."""
    g = geocoder.ip('me')
    print(f"Detected City: {g.city}")  
    return g.city

def display_weather(api_key, unit, location=None):
    """Display weather information based on user input or GPS location."""
    if not location:
        location = location_entry.get()

    # If no location is entered or detected, prompt for a valid input
    if not location:
        messagebox.showerror("Location Error", "Unable to detect your location. Please enter a city name or ZIP code.")
        return
    
    weather_data = get_weather(api_key, location, unit)

    if weather_data:
        main = weather_data['main']
        weather = weather_data['weather'][0]
        wind = weather_data['wind']

        temperature = main['temp']
        humidity = main['humidity']
        weather_description = weather['description']
        wind_speed = wind['speed']

        result = (
            f"Location: {weather_data['name']}\n"
            f"Temperature: {temperature}°{'C' if unit == 'metric' else 'F'}\n"
            f"Humidity: {humidity}%\n"
            f"Weather: {weather_description.capitalize()}\n"
            f"Wind Speed: {wind_speed} m/s"
        )

        weather_icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
        load_image(weather_icon_url)

        messagebox.showinfo("Weather Info", result)
    else:
        messagebox.showerror("Error", "City not found. Please check the city name or try another location.")

def load_image(url):
    """Load weather icon from URL and display it."""
    try:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        image.thumbnail((100, 100))  # Resize image
        img = ImageTk.PhotoImage(image)
        
        icon_label.config(image=img)
        icon_label.image = img  # Keep a reference
    except Exception as e:
        print("Error loading image:", e)

def use_gps_location(api_key, unit):
    """Fetch and display weather based on GPS-detected location."""
    location = get_current_location()
    if location:
        display_weather(api_key, unit, location=location)
    else:
        messagebox.showerror("Error", "Could not detect your location automatically. Please try again or enter manually.")

# Setting up the GUI
root = tk.Tk()
root.title("Weather App")

label = tk.Label(root, text="Enter city name or ZIP code or Use below button to access trough GPS:")
label.pack()

location_entry = tk.Entry(root)
location_entry.pack()

unit_choice = StringVar(value='C')  # Default to Celsius
unit_frame = tk.Frame(root)
tk.Radiobutton(unit_frame, text='Celsius (C)', variable=unit_choice, value='C').pack(side=tk.LEFT)
tk.Radiobutton(unit_frame, text='Fahrenheit (F)', variable=unit_choice, value='F').pack(side=tk.LEFT)
unit_frame.pack()

# Button to get weather manually by entering location
manual_button = tk.Button(root, text="Get Weather", command=lambda: display_weather("816ef82169eafd7d91e40b372684f15a", 'metric' if unit_choice.get() == 'C' else 'imperial'))
manual_button.pack()

# Button for automatic location detection via GPS (geocoder)
gps_button = tk.Button(root, text="Use My Location", command=lambda: use_gps_location("816ef82169eafd7d91e40b372684f15a", 'metric' if unit_choice.get() == 'C' else 'imperial'))
gps_button.pack()

icon_label = tk.Label(root)
icon_label.pack()

root.mainloop()
