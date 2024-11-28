import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import ttkbootstrap 

#function get weather info from api
def get_weather(city):
    api_key = "Your Api Key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
#parse json data
    weather = response.json()
    icon_id = weather["weather"][0]["icon"]
    temperature = weather["main"]["temp"] - 273.15
    description = weather["weather"][0]["description"]
    city = weather["name"]
    country = weather["sys"]["country"]
    
#get icon url and return all weather info
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (temperature, description, city, country, icon_url)




#funaction to search for weather information for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    
    #if not found
    temperature, description, city, country, icon_url = result
    location_label.config(text=f"{city}, {country}")
    
    #get weather icon image from url and update icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon
    
    
    #update the temperature and describe labels 
    temp_label.config(text=f"Temperature: {temperature:.2f}°C")
    description_label.config(text=f"Description: {description}")
#GUi
root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("500x600")

#enter widget => city name 
city_entry = ttkbootstrap.Entry(root, font="Helvetica 14")
city_entry.pack(pady=10)

#Button widget => to search for weather info

search_button = ttkbootstrap.Button(root, text="Search", command = search, bootstyle="warning")
search_button.pack(pady=10)

#label widget => to show city/countery name
location_label = ttkbootstrap.Label(root, text="", font="Helvetica 25")
location_label.pack(pady=20)

#lable widget = > show weather icons
icon_label = ttkbootstrap.Label(root)
icon_label.pack(pady=10)

#lable widget => to show temperature info
temp_label = ttkbootstrap.Label(root, text="", font="Helvetica 20")
temp_label.pack()
#lablel widget => to show weather description
description_label = ttkbootstrap.Label(root, text="", font="Helvetica 20")
description_label.pack()


# Start the GUI event loop
root.mainloop()