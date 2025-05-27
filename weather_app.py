import tkinter as tk
from tkinter import ttk, messagebox
import requests

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Weather App")
        self.root.geometry("400x250")
        self.weather_api_key = "6df058fa5e1d6d9fe872ab038f221ff1"
        self.geo_api_url = "http://ip-api.com/json/"
        self.create_widgets()
        self.detect_location()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.location_label = ttk.Label(self.main_frame, text="Detecting location...", font=('Arial', 12))
        self.location_label.pack(pady=5)

        self.temp_label = ttk.Label(self.main_frame, font=('Arial', 24))
        self.temp_label.pack(pady=10)

        self.details_frame = ttk.Frame(self.main_frame)
        self.details_frame.pack(fill=tk.X)

        ttk.Label(self.details_frame, text="Condition:").grid(row=0, column=0, sticky=tk.W)
        self.condition_label = ttk.Label(self.details_frame, text="-")
        self.condition_label.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.details_frame, text="Humidity:").grid(row=1, column=0, sticky=tk.W)
        self.humidity_label = ttk.Label(self.details_frame, text="-")
        self.humidity_label.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self.details_frame, text="Wind Speed:").grid(row=2, column=0, sticky=tk.W)
        self.wind_label = ttk.Label(self.details_frame, text="-")
        self.wind_label.grid(row=2, column=1, sticky=tk.W)

        self.refresh_btn = ttk.Button(self.main_frame, text="Refresh", command=self.refresh_weather)
        self.refresh_btn.pack(pady=10)

    def detect_location(self):
        try:
            geo_data = requests.get(self.geo_api_url, timeout=5).json()
            if geo_data.get('status') == 'success':
                self.lat = geo_data['lat']
                self.lon = geo_data['lon']
                city = geo_data.get('city', 'Unknown')
                country = geo_data.get('countryCode', '')
                self.location_label.config(text=f"Location: {city}, {country}")
                self.get_weather()
            else:
                self.location_label.config(text="Location not found")
                self.clear_weather_fields()
        except Exception as e:
            self.location_label.config(text="Location detection failed")
            self.clear_weather_fields()
            messagebox.showerror("Error", f"Location detection failed: {str(e)}")

    def get_weather(self):
        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"lat={self.lat}&lon={self.lon}&appid={self.weather_api_key}&units=metric"
            )
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get('cod') == 200:
                temp = data['main']['temp']
                condition = data['weather'][0]['description'].title()
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']

                self.temp_label.config(text=f"{temp}°C")
                self.condition_label.config(text=condition)
                self.humidity_label.config(text=f"{humidity}%")
                self.wind_label.config(text=f"{wind_speed} m/s")
            else:
                self.clear_weather_fields()
                msg = data.get('message', 'Weather data not found.')
                messagebox.showerror("Error", f"Weather API error: {msg}")
        except Exception as e:
            self.clear_weather_fields()
            messagebox.showerror("Error", f"Weather data fetch failed: {str(e)}")

    def clear_weather_fields(self):
        self.temp_label.config(text="-")
        self.condition_label.config(text="-")
        self.humidity_label.config(text="-")
        self.wind_label.config(text="-")

    def refresh_weather(self):
        self.detect_location()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
