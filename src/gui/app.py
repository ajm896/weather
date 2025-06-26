import tkinter as tk
from tkinter import StringVar, ttk
from tkinter.scrolledtext import ScrolledText

from weather import api


def show_forcast(forecast, fc):
    fc_dict = fc.getForecast() if fc else None
    if fc_dict:
        for p in fc_dict["periods"]:
            forecast.insert(tk.END, f"{p['name']}: {p['detailedForecast']}\n")
            forecast.insert(
                tk.END, f"Temperature: {p['temperature']}°{p['temperatureUnit']}\n"
            )
            forecast.insert(tk.END, f"Wind: {p['windSpeed']} {p['windDirection']}\n")
            forecast.insert(tk.END, f"Short Forecast: {p['shortForecast']}\n\n")
    else:
        forecast.insert(tk.END, "No weather data available.\n")


def search_weather(search_box, forecast, location_state):
    query = search_box.get()
    forecast.delete(1.0, tk.END)
    fc = api.load_cached_data(f"{query}_CACHED_FORECAST_DATA.json")
    location_state.set(query)
    show_forcast(forecast, fc)
    search_box.delete(0, tk.END)


def main():
    root = tk.Tk()
    frm = ttk.Frame(root, padding=10)
    location_state = StringVar(root)
    frm.pack(fill=tk.BOTH, expand=True)
    location_state.set("home")  # Default location
    label = ttk.Label(frm, textvariable=location_state, font=("Arial", 24))
    label.pack(pady=10)

    search_box = ttk.Entry(
        frm,
        width=30,
    )
    search_box.pack(pady=10)

    forecast = ScrolledText(frm, wrap=tk.WORD, width=80, height=320)
    fc = api.load_cached_data(f"{location_state.get()}_CACHED_FORECAST_DATA.json")

    root.bind(
        "<Return>",
        lambda event: search_weather(
            search_box, forecast, location_state=location_state
        ),
    )
    show_forcast(forecast, fc)
    forecast.pack(pady=10)
    root.mainloop()


if __name__ == "__main__":
    main()
