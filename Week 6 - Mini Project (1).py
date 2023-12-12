from tkinter import *
from tkinter.ttk import Combobox
import requests
from datetime import datetime

# region API Data code

weather_station_api = "https://environment.data.gov.uk/flood-monitoring/id/stations?parameter=rainfall&_limit=50"

weather_station_data = requests.get(weather_station_api)

data = weather_station_data.json()
    
readings = data["items"]

# gets the station measurement
def station_measurements(station_id_h_r):
     try:
          station_measurements_api = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id_h_r}"

          station_measurements_data = requests.get(station_measurements_api)

          station_measure_data = station_measurements_data.json()
          
          latest_reading = station_measure_data["items"]["measures"]["latestReading"]
          latest_reading_unit = station_measure_data["items"]["measures"]

          measurement_value = latest_reading.get("value")
          measurement_unit = latest_reading_unit.get("unitName")

          return measurement_unit 
     except Exception as e:
          station_measurements_api = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id_h_r}"

          station_measurements_data = requests.get(station_measurements_api)

          station_measure_data = station_measurements_data.json()
          
          latest_reading = station_measure_data["items"]["measures"][0]["latestReading"]
          measurement_unit = station_measure_data["items"]["measures"][0]["unitName"]

          measurement_value = latest_reading.get("value")

          return measurement_unit          

# weather station region
def weather_station_region(station_id_h_r, reading):
     station_info_api = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id_h_r}"

     station_info_data = requests.get(station_info_api)

     station_info_json = station_info_data.json()
     
     station_info = station_info_json["items"]

     station_label = station_info.get("label")
     station_id = station_info.get("stationReference")
     station_region = station_info.get("eaRegionName")

     station_label = str(station_label)
     station_region = str(station_region)

     if reading == "reference":
        return station_label
     elif reading == "region":
         return station_region

# initialising for functions
latestReading_list = []
l_readings = None
measurement_unit_10 = None
l_readings_dt_f = None


# high/low prep
def high_low_readings_prep(station_id):   
     
     try:
          station_measurements_api_10 = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id}"
          station_measurements_data_10 = requests.get(station_measurements_api_10)
          station_measure_data_10 = station_measurements_data_10.json()
          measurement_unit_10 = station_measure_data_10["items"]["measures"]["unitName"]


          station_latest_readings_api = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id}/readings?_sorted&_limit=10"
          station_latest_readings_data = requests.get(station_latest_readings_api)
          station_latest_readings_json = station_latest_readings_data.json()

          station_latest_readings = station_latest_readings_json["items"]   
     except Exception as e:
          station_measurements_api_10 = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id}"
          station_measurements_data_10 = requests.get(station_measurements_api_10)
          station_measure_data_10 = station_measurements_data_10.json()
          measurement_unit_10 = station_measure_data_10["items"]["measures"][0]["unitName"]


          station_latest_readings_api = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id}/readings?_sorted&_limit=10"
          station_latest_readings_data = requests.get(station_latest_readings_api)
          station_latest_readings_json = station_latest_readings_data.json()

          station_latest_readings = station_latest_readings_json["items"]            

     for i in range(10):
          l_readings = station_latest_readings[i]["value"]  
          l_readings_dt_f = station_latest_readings[i]["dateTime"]

          latestReading_list.append(l_readings)

# all 10 latest readings - readings
def latest_readings(station_id, index, returning):
     
     try:
          station_measurements_api_10 = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id}"
          station_measurements_data_10 = requests.get(station_measurements_api_10)
          station_measure_data_10 = station_measurements_data_10.json()
          measurement_unit_10 = station_measure_data_10["items"]["measures"]["unitName"]


          station_latest_readings_api = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id}/readings?_sorted&_limit=10"
          station_latest_readings_data = requests.get(station_latest_readings_api)
          station_latest_readings_json = station_latest_readings_data.json()

          station_latest_readings = station_latest_readings_json["items"]   

     except Exception as e:
          station_measurements_api_10 = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id}"
          station_measurements_data_10 = requests.get(station_measurements_api_10)
          station_measure_data_10 = station_measurements_data_10.json()
          measurement_unit_10 = station_measure_data_10["items"]["measures"][0]["unitName"]


          station_latest_readings_api = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id}/readings?_sorted&_limit=10"
          station_latest_readings_data = requests.get(station_latest_readings_api)
          station_latest_readings_json = station_latest_readings_data.json()

          station_latest_readings = station_latest_readings_json["items"]             

     if returning == "reading":
         l_readings = station_latest_readings[index]["value"]

            #  latestReading_list.append(f"{l_readings}{measurement_unit_10}")
         return str(l_readings) + measurement_unit_10
     elif returning == "time":
         l_readings = station_latest_readings[index]["value"]  
         l_readings_dt = station_latest_readings[index]["dateTime"]
         l_reading_t = datetime.strptime(l_readings_dt, "%Y-%m-%dT%H:%M:%SZ")

         return l_reading_t.strftime("%H:%M:%S")
     elif returning == "date":
         l_readings = station_latest_readings[index]["value"]  
         l_readings_dt = station_latest_readings[index]["dateTime"]
         l_reading_t = datetime.strptime(l_readings_dt, "%Y-%m-%dT%H:%M:%SZ")

         return l_reading_t.strftime("%Y-%m-%d")
         


# highest reading - reading
def highest_reading(station_id_h_r):
     high_low_readings_prep(station_id_h_r)
     highest_reading =max(latestReading_list)

     measurement_unit = station_measurements(station_id_h_r)

     return str(highest_reading) + str(measurement_unit)

# highest reading - number only
def highest_reading_number_only(station_id_h_r):
     high_low_readings_prep(station_id_h_r)
     highest_reading =max(latestReading_list)

     measurement_unit = station_measurements(station_id_h_r)

     return float(highest_reading)

# lowest reading - number only
def lowest_reading_number_only(station_id_h_r):
     high_low_readings_prep(station_id_h_r)
     lowest_reading =min(latestReading_list)

     measurement_unit = station_measurements(station_id_h_r)

     return float(lowest_reading)

# lowest reading - reading
def lowest_reading(station_id_h_r):
     high_low_readings_prep(station_id_h_r)
     non_zero_readings = [reading for reading in latestReading_list if reading != 0.00]
    
     if non_zero_readings:
        lowest_non_zero_reading = min(non_zero_readings)
        measurement_unit = station_measurements(station_id_h_r)
        return str(lowest_non_zero_reading) + str(measurement_unit)
     else:
        return "No non-zero readings available"

def find_time_for_reading(station_id, target_reading):
    station_latest_readings_api = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id}/readings?_sorted&_limit=10"
    station_latest_readings_data = requests.get(station_latest_readings_api)
    station_latest_readings_json = station_latest_readings_data.json()
    station_latest_readings = station_latest_readings_json["items"]

    for reading in station_latest_readings:
        reading_value = reading["value"]
        if reading_value == target_reading:
            reading_time = reading["dateTime"]
            reading_time_f = datetime.strptime(reading_time, "%Y-%m-%dT%H:%M:%SZ")

            return reading_time_f
        elif target_reading == "No non-zero readings available":
            return "N/A"


#endregion


# region UI code 

# define your weather station ids
station_id_h_r_1 = "3680"
station_id_h_r_2 = "E8520"
station_id_h_r_3 = "000181TP"
station_id_h_r_4 = "3680"
station_id_h_r_5 = "276316TP"

root = Tk(className="Rainfall Program")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.geometry("1280x720")

frame = Frame(root, bg="#ffccde", height=720 , width=1280 )
frame.grid(row=0, column=0, sticky="nsew")

def on_enter(e):
   homeButton.config(background="white", foreground= "black", font=("Yu Gothic UI Semibold", 18, "underline"))

def on_leave(e):
   homeButton.config(background= "#ffccde", foreground= 'black', font=("Yu Gothic UI Semibold", 18))

current_frame = frame 

def show_frame(new_frame):
    global current_frame 
  
    if current_frame is not None:
        current_frame.grid_forget()
  
    new_frame.grid(row=0, column=0, sticky="nsew")
    current_frame = new_frame

show_frame(frame)

def ws1():
    root_ws1 = Tk(className="Weather Station 1")
    root_ws1.grid_rowconfigure(0, weight=1)
    root_ws1.grid_columnconfigure(0, weight=1)
    root_ws1.geometry("1280x720")

    frame_ws1 = Frame(root_ws1, bg="#ffccde", height=720 , width=1280 )
    frame_ws1.grid(row=0, column=0, sticky="nsew")

    def go_back_to_home():
        root_ws1.destroy()  
        show_frame(frame)  


    homeButton_ws1 = Button(frame_ws1, bg="#ffccde", bd="0", activebackground="white", font=("Yu Gothic UI Semibold", 18), text= "< Home", command=go_back_to_home)
    homeButton_ws1.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    rainfall_title_ws1 = Label(frame_ws1, background="#ffccde", font=("Yu Gothic UI Semibold", 60), text="Rainfall")
    rainfall_title_ws1.grid(row=0, column=0, pady=0, padx=500, sticky="n")

    rainfall_subtitle_ws1 = Label(frame_ws1, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text="Weather Station 1")
    rainfall_subtitle_ws1.grid(row=1, column=0, pady=0, padx=500, sticky="n")

    ws1_info = Label(frame_ws1, background="white",anchor=CENTER, font=("Yu Gothic UI Semibold", 16), text=f"Weather Station ID: {station_id_h_r_1}                {weather_station_region(station_id_h_r_1, 'reference')}                                Region: {weather_station_region(station_id_h_r_1, 'region')}  ")
    ws1_info.grid(row=2, column=0, pady=0, padx=0, sticky="n")

    combobox = Combobox(frame_ws1, height=50, background="white", font=("Yu Gothic UI Semibold", 16), values=["Highest/Lowest readings","Latest Reading 1","Latest Reading 2","Latest Reading 3","Latest Reading 4","Latest Reading 5","Latest Reading 6","Latest Reading 7","Latest Reading 8","Latest Reading 9","Latest Reading 10"])
    combobox.grid(row=3, column=0, padx=10, pady=20, sticky="w")

    h_r_n_o = float(highest_reading_number_only(station_id_h_r_1))

    if h_r_n_o == 0.00:
        high_text = "N/A"
        low_text = "N/A"
    else:
        h_r_n_o_dt = find_time_for_reading(station_id_h_r_1,h_r_n_o)
        h_r_n_o_dt_tf = h_r_n_o_dt.strftime("%H:%M:%S")
        h_r_n_o_dt_df = h_r_n_o_dt.strftime("%Y-%m-%d")
        high_text = f"On {h_r_n_o_dt_df} at {h_r_n_o_dt_tf}"

        l_r_n_o = float(lowest_reading_number_only(station_id_h_r_1))
        l_r_n_o_dt = find_time_for_reading(station_id_h_r_1,l_r_n_o)
        l_r_n_o_dt_tf = l_r_n_o_dt.strftime("%H:%M:%S")
        l_r_n_o_dt_df = l_r_n_o_dt.strftime("%Y-%m-%d")
        low_text = f"On {l_r_n_o_dt_df} at {l_r_n_o_dt_tf}"
    

    def dropdown_ws1(event):
        selected_option_ws1 = combobox.get()
        if selected_option_ws1 == "Highest/Lowest readings":
            rainfall_l1_ws1.config(text="The highest reading was:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l2_ws1.config(text=highest_reading(station_id_h_r_1), font=("Yu Gothic UI Semibold", 32))
            rainfall_l3_ws1.config(text=high_text, font=("Yu Gothic UI Semibold", 25))
            rainfall_l4_ws1.config(text="The lowest reading was:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l5_ws1.config(text=lowest_reading(station_id_h_r_1), font=("Yu Gothic UI Semibold", 32))
            rainfall_l6_ws1.config(text=low_text, font=("Yu Gothic UI Semibold", 25))
        elif selected_option_ws1 == "Latest Reading 1":
            rainfall_l1_ws1.config(text="On:")
            rainfall_l2_ws1.config(text=latest_readings(station_id_h_r_1, 0, "date"))
            rainfall_l3_ws1.config(text="At:")
            rainfall_l4_ws1.config(text=latest_readings(station_id_h_r_1, 0, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws1.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws1.config(text=latest_readings(station_id_h_r_1, 0, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws1 == "Latest Reading 2":
            rainfall_l1_ws1.config(text="On:")
            rainfall_l2_ws1.config(text=latest_readings(station_id_h_r_1, 1, "date"))
            rainfall_l3_ws1.config(text="At:")
            rainfall_l4_ws1.config(text=latest_readings(station_id_h_r_1, 1, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws1.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws1.config(text=latest_readings(station_id_h_r_1, 1, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws1 == "Latest Reading 3":
            rainfall_l1_ws1.config(text="On:")
            rainfall_l2_ws1.config(text=latest_readings(station_id_h_r_1, 2, "date"))
            rainfall_l3_ws1.config(text="At:")
            rainfall_l4_ws1.config(text=latest_readings(station_id_h_r_1, 2, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws1.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws1.config(text=latest_readings(station_id_h_r_1, 2, "reading"), font=("Yu Gothic UI Semibold", 32))   
        elif selected_option_ws1 == "Latest Reading 4":
            rainfall_l1_ws1.config(text="On:")
            rainfall_l2_ws1.config(text=latest_readings(station_id_h_r_1, 3, "date"))
            rainfall_l3_ws1.config(text="At:")
            rainfall_l4_ws1.config(text=latest_readings(station_id_h_r_1, 3, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws1.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws1.config(text=latest_readings(station_id_h_r_1, 3, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws1 == "Latest Reading 5":
            rainfall_l1_ws1.config(text="On:")
            rainfall_l2_ws1.config(text=latest_readings(station_id_h_r_1, 4, "date"))
            rainfall_l3_ws1.config(text="At:")
            rainfall_l4_ws1.config(text=latest_readings(station_id_h_r_1, 4, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws1.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws1.config(text=latest_readings(station_id_h_r_1, 4, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws1 == "Latest Reading 6":
            rainfall_l1_ws1.config(text="On:")
            rainfall_l2_ws1.config(text=latest_readings(station_id_h_r_1, 5, "date"))
            rainfall_l3_ws1.config(text="At:")
            rainfall_l4_ws1.config(text=latest_readings(station_id_h_r_1, 5, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws1.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws1.config(text=latest_readings(station_id_h_r_1, 5, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws1 == "Latest Reading 7":
            rainfall_l1_ws1.config(text="On:")
            rainfall_l2_ws1.config(text=latest_readings(station_id_h_r_1, 6, "date"))
            rainfall_l3_ws1.config(text="At:")
            rainfall_l4_ws1.config(text=latest_readings(station_id_h_r_1, 6, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws1.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws1.config(text=latest_readings(station_id_h_r_1, 6, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws1 == "Latest Reading 8":
            rainfall_l1_ws1.config(text="On:")
            rainfall_l2_ws1.config(text=latest_readings(station_id_h_r_1, 7, "date"))
            rainfall_l3_ws1.config(text="At:")
            rainfall_l4_ws1.config(text=latest_readings(station_id_h_r_1, 7, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws1.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws1.config(text=latest_readings(station_id_h_r_1, 7, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws1 == "Latest Reading 9":
            rainfall_l1_ws1.config(text="On:")
            rainfall_l2_ws1.config(text=latest_readings(station_id_h_r_1, 8, "date"))
            rainfall_l3_ws1.config(text="At:")
            rainfall_l4_ws1.config(text=latest_readings(station_id_h_r_1, 8, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws1.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws1.config(text=latest_readings(station_id_h_r_1, 8, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws1 == "Latest Reading 10":
            rainfall_l1_ws1.config(text="On:")
            rainfall_l2_ws1.config(text=latest_readings(station_id_h_r_1, 9, "date"))
            rainfall_l3_ws1.config(text="At:")
            rainfall_l4_ws1.config(text=latest_readings(station_id_h_r_1, 9, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws1.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws1.config(text=latest_readings(station_id_h_r_1, 9, "reading"), font=("Yu Gothic UI Semibold", 32))

    combobox.bind("<<ComboboxSelected>>", dropdown_ws1)
    combobox.set("Highest/Lowest readings")


    rainfall_l1_ws1 = Label(frame_ws1, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text="The highest reading was:")
    rainfall_l1_ws1.grid(row=3, column=0, pady=0, padx=0, sticky="n")

    rainfall_l2_ws1 = Label(frame_ws1, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text=highest_reading(station_id_h_r_1))
    rainfall_l2_ws1.grid(row=4, column=0, pady=0, padx=10, sticky="n")

    rainfall_l3_ws1 = Label(frame_ws1, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text=high_text)
    rainfall_l3_ws1.grid(row=5, column=0, pady=10, padx=10, sticky="n")

    rainfall_l4_ws1 = Label(frame_ws1, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text="The lowest reading was:")
    rainfall_l4_ws1.grid(row=6, column=0, pady=10, padx=10, sticky="n")

    rainfall_l5_ws1 = Label(frame_ws1, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text=lowest_reading(station_id_h_r_1))
    rainfall_l5_ws1.grid(row=7, column=0, pady=10, padx=10, sticky="n")

    rainfall_l6_ws1 = Label(frame_ws1, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text=low_text)
    rainfall_l6_ws1.grid(row=8, column=0, pady=10, padx=10, sticky="n")


    root_ws1.mainloop()

def ws2():
    root_ws2 = Tk(className="Weather Station 2")
    root_ws2.grid_rowconfigure(0, weight=1)
    root_ws2.grid_columnconfigure(0, weight=1)
    root_ws2.geometry("1280x720")

    frame_ws2 = Frame(root_ws2, bg="#ffccde", height=720 , width=1280 )
    frame_ws2.grid(row=0, column=0, sticky="nsew")

    def go_back_to_home():
        root_ws2.destroy()  
        show_frame(frame)  


    homeButton_ws2 = Button(frame_ws2, bg="#ffccde", bd="0", activebackground="white", font=("Yu Gothic UI Semibold", 18), text= "< Home", command=go_back_to_home)
    homeButton_ws2.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    rainfall_title_ws2 = Label(frame_ws2, background="#ffccde", font=("Yu Gothic UI Semibold", 60), text="Rainfall")
    rainfall_title_ws2.grid(row=0, column=0, pady=0, padx=500, sticky="n")

    rainfall_subtitle_ws2 = Label(frame_ws2, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text="Weather Station 2")
    rainfall_subtitle_ws2.grid(row=1, column=0, pady=0, padx=500, sticky="n")

    ws2_info = Label(frame_ws2, background="white",anchor=CENTER, font=("Yu Gothic UI Semibold", 16), text=f"Weather Station ID: {station_id_h_r_2}                {weather_station_region(station_id_h_r_2, 'reference')}                                Region: {weather_station_region(station_id_h_r_2, 'region')}  ")
    ws2_info.grid(row=2, column=0, pady=10, padx=0, sticky="n")

    combobox = Combobox(frame_ws2, height=50, background="white", font=("Yu Gothic UI Semibold", 16), values=["Highest/Lowest readings","Latest Reading 1","Latest Reading 2","Latest Reading 3","Latest Reading 4","Latest Reading 5","Latest Reading 6","Latest Reading 7","Latest Reading 8","Latest Reading 9","Latest Reading 10"])
    combobox.grid(row=3, column=0, padx=10, pady=20, sticky="w")

    h_r_n_o = float(highest_reading_number_only(station_id_h_r_2))

    if h_r_n_o == 0.00:
        high_text = "N/A"
        low_text = "N/A"
    else:
        h_r_n_o_dt = find_time_for_reading(station_id_h_r_2,h_r_n_o)
        h_r_n_o_dt_tf = h_r_n_o_dt.strftime("%H:%M:%S")
        h_r_n_o_dt_df = h_r_n_o_dt.strftime("%Y-%m-%d")
        high_text = f"On {h_r_n_o_dt_df} at {h_r_n_o_dt_tf}"

        l_r_n_o = float(lowest_reading_number_only(station_id_h_r_2))
        l_r_n_o_dt = find_time_for_reading(station_id_h_r_2,l_r_n_o)
        l_r_n_o_dt_tf = l_r_n_o_dt.strftime("%H:%M:%S")
        l_r_n_o_dt_df = l_r_n_o_dt.strftime("%Y-%m-%d")
        low_text = f"On {l_r_n_o_dt_df} at {l_r_n_o_dt_tf}"
    
    def dropdown_ws2(event):
        selected_option_ws2 = combobox.get()
        if selected_option_ws2 == "Highest/Lowest readings":
            rainfall_l1_ws2.config(text="The highest reading was:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l2_ws2.config(text=highest_reading(station_id_h_r_2), font=("Yu Gothic UI Semibold", 32))
            rainfall_l3_ws2.config(text=high_text, font=("Yu Gothic UI Semibold", 25))
            rainfall_l4_ws2.config(text="The lowest reading was:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l5_ws2.config(text=lowest_reading(station_id_h_r_2), font=("Yu Gothic UI Semibold", 32))
            rainfall_l6_ws2.config(text=low_text, font=("Yu Gothic UI Semibold", 25))
        elif selected_option_ws2 == "Latest Reading 1":
            rainfall_l1_ws2.config(text="On:")
            rainfall_l2_ws2.config(text=latest_readings(station_id_h_r_2, 0, "date"))
            rainfall_l3_ws2.config(text="At:")
            rainfall_l4_ws2.config(text=latest_readings(station_id_h_r_2, 0, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws2.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws2.config(text=latest_readings(station_id_h_r_2, 0, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws2 == "Latest Reading 2":
            rainfall_l1_ws2.config(text="On:")
            rainfall_l2_ws2.config(text=latest_readings(station_id_h_r_2, 1, "date"))
            rainfall_l3_ws2.config(text="At:")
            rainfall_l4_ws2.config(text=latest_readings(station_id_h_r_2, 1, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws2.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws2.config(text=latest_readings(station_id_h_r_2, 1, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws2 == "Latest Reading 3":
            rainfall_l1_ws2.config(text="On:")
            rainfall_l2_ws2.config(text=latest_readings(station_id_h_r_2, 2, "date"))
            rainfall_l3_ws2.config(text="At:")
            rainfall_l4_ws2.config(text=latest_readings(station_id_h_r_2, 2, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws2.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws2.config(text=latest_readings(station_id_h_r_2, 2, "reading"), font=("Yu Gothic UI Semibold", 32))   
        elif selected_option_ws2 == "Latest Reading 4":
            rainfall_l1_ws2.config(text="On:")
            rainfall_l2_ws2.config(text=latest_readings(station_id_h_r_2, 3, "date"))
            rainfall_l3_ws2.config(text="At:")
            rainfall_l4_ws2.config(text=latest_readings(station_id_h_r_2, 3, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws2.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws2.config(text=latest_readings(station_id_h_r_2, 3, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws2 == "Latest Reading 5":
            rainfall_l1_ws2.config(text="On:")
            rainfall_l2_ws2.config(text=latest_readings(station_id_h_r_2, 4, "date"))
            rainfall_l3_ws2.config(text="At:")
            rainfall_l4_ws2.config(text=latest_readings(station_id_h_r_2, 4, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws2.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws2.config(text=latest_readings(station_id_h_r_2, 4, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws2 == "Latest Reading 6":
            rainfall_l1_ws2.config(text="On:")
            rainfall_l2_ws2.config(text=latest_readings(station_id_h_r_2, 5, "date"))
            rainfall_l3_ws2.config(text="At:")
            rainfall_l4_ws2.config(text=latest_readings(station_id_h_r_2, 5, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws2.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws2.config(text=latest_readings(station_id_h_r_2, 5, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws2 == "Latest Reading 7":
            rainfall_l1_ws2.config(text="On:")
            rainfall_l2_ws2.config(text=latest_readings(station_id_h_r_2, 6, "date"))
            rainfall_l3_ws2.config(text="At:")
            rainfall_l4_ws2.config(text=latest_readings(station_id_h_r_2, 6, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws2.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws2.config(text=latest_readings(station_id_h_r_2, 6, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws2 == "Latest Reading 8":
            rainfall_l1_ws2.config(text="On:")
            rainfall_l2_ws2.config(text=latest_readings(station_id_h_r_2, 7, "date"))
            rainfall_l3_ws2.config(text="At:")
            rainfall_l4_ws2.config(text=latest_readings(station_id_h_r_2, 7, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws2.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws2.config(text=latest_readings(station_id_h_r_2, 7, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws2 == "Latest Reading 9":
            rainfall_l1_ws2.config(text="On:")
            rainfall_l2_ws2.config(text=latest_readings(station_id_h_r_2, 8, "date"))
            rainfall_l3_ws2.config(text="At:")
            rainfall_l4_ws2.config(text=latest_readings(station_id_h_r_2, 8, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws2.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws2.config(text=latest_readings(station_id_h_r_2, 8, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws2 == "Latest Reading 10":
            rainfall_l1_ws2.config(text="On:")
            rainfall_l2_ws2.config(text=latest_readings(station_id_h_r_2, 9, "date"))
            rainfall_l3_ws2.config(text="At:")
            rainfall_l4_ws2.config(text=latest_readings(station_id_h_r_2, 9, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws2.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws2.config(text=latest_readings(station_id_h_r_2, 9, "reading"), font=("Yu Gothic UI Semibold", 32))

    combobox.bind("<<ComboboxSelected>>", dropdown_ws2)
    combobox.set("Highest/Lowest readings")


    rainfall_l1_ws2 = Label(frame_ws2, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text="The highest reading was:")
    rainfall_l1_ws2.grid(row=3, column=0, pady=0, padx=0, sticky="n")

    rainfall_l2_ws2 = Label(frame_ws2, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text=highest_reading(station_id_h_r_2))
    rainfall_l2_ws2.grid(row=4, column=0, pady=0, padx=10, sticky="n")

    rainfall_l3_ws2 = Label(frame_ws2, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text=high_text)
    rainfall_l3_ws2.grid(row=5, column=0, pady=10, padx=10, sticky="n")

    rainfall_l4_ws2 = Label(frame_ws2, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text="The lowest reading was:")
    rainfall_l4_ws2.grid(row=6, column=0, pady=10, padx=10, sticky="n")

    rainfall_l5_ws2 = Label(frame_ws2, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text=lowest_reading(station_id_h_r_2))
    rainfall_l5_ws2.grid(row=7, column=0, pady=10, padx=10, sticky="n")

    rainfall_l6_ws2 = Label(frame_ws2, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text=low_text)
    rainfall_l6_ws2.grid(row=8, column=0, pady=10, padx=10, sticky="n")


    root_ws2.mainloop()

def ws3():
    root_ws3 = Tk(className="Weather Station 3")
    root_ws3.grid_rowconfigure(0, weight=1)
    root_ws3.grid_columnconfigure(0, weight=1)
    root_ws3.geometry("1280x720")

    frame_ws3 = Frame(root_ws3, bg="#ffccde", height=720 , width=1280 )
    frame_ws3.grid(row=0, column=0, sticky="nsew")

    def go_back_to_home():
        root_ws3.destroy()  
        show_frame(frame)  


    homeButton_ws3 = Button(frame_ws3, bg="#ffccde", bd="0", activebackground="white", font=("Yu Gothic UI Semibold", 18), text= "< Home", command=go_back_to_home)
    homeButton_ws3.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    rainfall_title_ws3 = Label(frame_ws3, background="#ffccde", font=("Yu Gothic UI Semibold", 60), text="Rainfall")
    rainfall_title_ws3.grid(row=0, column=0, pady=0, padx=500, sticky="n")

    rainfall_subtitle_ws3 = Label(frame_ws3, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text="Weather Station 3")
    rainfall_subtitle_ws3.grid(row=1, column=0, pady=0, padx=500, sticky="n")

    ws3_info = Label(frame_ws3, background="white",anchor=CENTER, font=("Yu Gothic UI Semibold", 16), text=f"Weather Station ID: {station_id_h_r_3}                {weather_station_region(station_id_h_r_3, 'reference')}                                Region: {weather_station_region(station_id_h_r_3, 'region')}  ")
    ws3_info.grid(row=2, column=0, pady=10, padx=0, sticky="n")

    combobox = Combobox(frame_ws3, height=50, background="white", font=("Yu Gothic UI Semibold", 16), values=["Highest/Lowest readings","Latest Reading 1","Latest Reading 2","Latest Reading 3","Latest Reading 4","Latest Reading 5","Latest Reading 6","Latest Reading 7","Latest Reading 8","Latest Reading 9","Latest Reading 10"])
    combobox.grid(row=3, column=0, padx=10, pady=20, sticky="w")

    h_r_n_o = float(highest_reading_number_only(station_id_h_r_3))

    
    print(h_r_n_o)

    if h_r_n_o == 0.00:
        high_text = "N/A"
        low_text = "N/A"
    else:
        h_r_n_o_dt = find_time_for_reading(station_id_h_r_3,h_r_n_o)
        h_r_n_o_dt_tf = h_r_n_o_dt.strftime("%H:%M:%S")
        h_r_n_o_dt_df = h_r_n_o_dt.strftime("%Y-%m-%d")
        high_text = f"On {h_r_n_o_dt_df} at {h_r_n_o_dt_tf}"

        l_r_n_o = float(lowest_reading_number_only(station_id_h_r_3))
        l_r_n_o_dt = find_time_for_reading(station_id_h_r_3,l_r_n_o)
        l_r_n_o_dt_tf = l_r_n_o_dt.strftime("%H:%M:%S")
        l_r_n_o_dt_df = l_r_n_o_dt.strftime("%Y-%m-%d")
        low_text = f"On {l_r_n_o_dt_df} at {l_r_n_o_dt_tf}"
    

    def dropdown_ws3(event):
        selected_option_ws3 = combobox.get()
        if selected_option_ws3 == "Highest/Lowest readings":
            rainfall_l1_ws3.config(text="The highest reading was:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l2_ws3.config(text=highest_reading(station_id_h_r_3), font=("Yu Gothic UI Semibold", 32))
            rainfall_l3_ws3.config(text=high_text, font=("Yu Gothic UI Semibold", 25))
            rainfall_l4_ws3.config(text="The lowest reading was:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l5_ws3.config(text=lowest_reading(station_id_h_r_3), font=("Yu Gothic UI Semibold", 32))
            rainfall_l6_ws3.config(text=low_text, font=("Yu Gothic UI Semibold", 25))
        elif selected_option_ws3 == "Latest Reading 1":
            rainfall_l1_ws3.config(text="On:")
            rainfall_l2_ws3.config(text=latest_readings(station_id_h_r_3, 0, "date"))
            rainfall_l3_ws3.config(text="At:")
            rainfall_l4_ws3.config(text=latest_readings(station_id_h_r_3, 0, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws3.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws3.config(text=latest_readings(station_id_h_r_3, 0, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws3 == "Latest Reading 2":
            rainfall_l1_ws3.config(text="On:")
            rainfall_l2_ws3.config(text=latest_readings(station_id_h_r_3, 1, "date"))
            rainfall_l3_ws3.config(text="At:")
            rainfall_l4_ws3.config(text=latest_readings(station_id_h_r_3, 1, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws3.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws3.config(text=latest_readings(station_id_h_r_3, 1, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws3 == "Latest Reading 3":
            rainfall_l1_ws3.config(text="On:")
            rainfall_l2_ws3.config(text=latest_readings(station_id_h_r_3, 2, "date"))
            rainfall_l3_ws3.config(text="At:")
            rainfall_l4_ws3.config(text=latest_readings(station_id_h_r_3, 2, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws3.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws3.config(text=latest_readings(station_id_h_r_3, 2, "reading"), font=("Yu Gothic UI Semibold", 32))   
        elif selected_option_ws3 == "Latest Reading 4":
            rainfall_l1_ws3.config(text="On:")
            rainfall_l2_ws3.config(text=latest_readings(station_id_h_r_3, 3, "date"))
            rainfall_l3_ws3.config(text="At:")
            rainfall_l4_ws3.config(text=latest_readings(station_id_h_r_3, 3, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws3.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws3.config(text=latest_readings(station_id_h_r_3, 3, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws3 == "Latest Reading 5":
            rainfall_l1_ws3.config(text="On:")
            rainfall_l2_ws3.config(text=latest_readings(station_id_h_r_3, 4, "date"))
            rainfall_l3_ws3.config(text="At:")
            rainfall_l4_ws3.config(text=latest_readings(station_id_h_r_3, 4, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws3.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws3.config(text=latest_readings(station_id_h_r_3, 4, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws3 == "Latest Reading 6":
            rainfall_l1_ws3.config(text="On:")
            rainfall_l2_ws3.config(text=latest_readings(station_id_h_r_3, 5, "date"))
            rainfall_l3_ws3.config(text="At:")
            rainfall_l4_ws3.config(text=latest_readings(station_id_h_r_3, 5, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws3.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws3.config(text=latest_readings(station_id_h_r_3, 5, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws3 == "Latest Reading 7":
            rainfall_l1_ws3.config(text="On:")
            rainfall_l2_ws3.config(text=latest_readings(station_id_h_r_3, 6, "date"))
            rainfall_l3_ws3.config(text="At:")
            rainfall_l4_ws3.config(text=latest_readings(station_id_h_r_3, 6, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws3.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws3.config(text=latest_readings(station_id_h_r_3, 6, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws3 == "Latest Reading 8":
            rainfall_l1_ws3.config(text="On:")
            rainfall_l2_ws3.config(text=latest_readings(station_id_h_r_3, 7, "date"))
            rainfall_l3_ws3.config(text="At:")
            rainfall_l4_ws3.config(text=latest_readings(station_id_h_r_3, 7, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws3.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws3.config(text=latest_readings(station_id_h_r_3, 7, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws3 == "Latest Reading 9":
            rainfall_l1_ws3.config(text="On:")
            rainfall_l2_ws3.config(text=latest_readings(station_id_h_r_3, 8, "date"))
            rainfall_l3_ws3.config(text="At:")
            rainfall_l4_ws3.config(text=latest_readings(station_id_h_r_3, 8, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws3.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws3.config(text=latest_readings(station_id_h_r_3, 8, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws3 == "Latest Reading 10":
            rainfall_l1_ws3.config(text="On:")
            rainfall_l2_ws3.config(text=latest_readings(station_id_h_r_3, 9, "date"))
            rainfall_l3_ws3.config(text="At:")
            rainfall_l4_ws3.config(text=latest_readings(station_id_h_r_3, 9, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws3.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws3.config(text=latest_readings(station_id_h_r_3, 9, "reading"), font=("Yu Gothic UI Semibold", 32))

    combobox.bind("<<ComboboxSelected>>", dropdown_ws3)
    combobox.set("Highest/Lowest readings")


    rainfall_l1_ws3 = Label(frame_ws3, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text="The highest reading was:")
    rainfall_l1_ws3.grid(row=3, column=0, pady=0, padx=0, sticky="n")

    rainfall_l2_ws3 = Label(frame_ws3, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text=highest_reading(station_id_h_r_3))
    rainfall_l2_ws3.grid(row=4, column=0, pady=0, padx=10, sticky="n")

    rainfall_l3_ws3 = Label(frame_ws3, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text=high_text)
    rainfall_l3_ws3.grid(row=5, column=0, pady=10, padx=10, sticky="n")

    rainfall_l4_ws3 = Label(frame_ws3, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text="The lowest reading was:")
    rainfall_l4_ws3.grid(row=6, column=0, pady=10, padx=10, sticky="n")

    rainfall_l5_ws3 = Label(frame_ws3, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text=lowest_reading(station_id_h_r_3))
    rainfall_l5_ws3.grid(row=7, column=0, pady=10, padx=10, sticky="n")

    rainfall_l6_ws3 = Label(frame_ws3, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text=low_text)
    rainfall_l6_ws3.grid(row=8, column=0, pady=10, padx=10, sticky="n")


    root_ws3.mainloop()

def ws4():
    root_ws4 = Tk(className="Weather Station 4")
    root_ws4.grid_rowconfigure(0, weight=1)
    root_ws4.grid_columnconfigure(0, weight=1)
    root_ws4.geometry("1280x720")

    frame_ws4 = Frame(root_ws4, bg="#ffccde", height=720 , width=1280 )
    frame_ws4.grid(row=0, column=0, sticky="nsew")

    def go_back_to_home():
        root_ws4.destroy()  
        show_frame(frame)  


    homeButton_ws4 = Button(frame_ws4, bg="#ffccde", bd="0", activebackground="white", font=("Yu Gothic UI Semibold", 18), text= "< Home", command=go_back_to_home)
    homeButton_ws4.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    rainfall_title_ws4 = Label(frame_ws4, background="#ffccde", font=("Yu Gothic UI Semibold", 60), text="Rainfall")
    rainfall_title_ws4.grid(row=0, column=0, pady=0, padx=500, sticky="n")

    rainfall_subtitle_ws4 = Label(frame_ws4, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text="Weather Station 4")
    rainfall_subtitle_ws4.grid(row=1, column=0, pady=0, padx=500, sticky="n")

    ws4_info = Label(frame_ws4, background="white",anchor=CENTER, font=("Yu Gothic UI Semibold", 16), text=f"Weather Station ID: {station_id_h_r_4}                {weather_station_region(station_id_h_r_4, 'reference')}                                Region: {weather_station_region(station_id_h_r_4, 'region')}  ")
    ws4_info.grid(row=2, column=0, pady=10, padx=0, sticky="n")

    combobox = Combobox(frame_ws4, height=50, background="white", font=("Yu Gothic UI Semibold", 16), values=["Highest/Lowest readings","Latest Reading 1","Latest Reading 2","Latest Reading 3","Latest Reading 4","Latest Reading 5","Latest Reading 6","Latest Reading 7","Latest Reading 8","Latest Reading 9","Latest Reading 10"])
    combobox.grid(row=3, column=0, padx=10, pady=20, sticky="w")

    h_r_n_o = float(highest_reading_number_only(station_id_h_r_4))

    if h_r_n_o == 0.00:
        high_text = "N/A"
        low_text = "N/A"
    else:
        h_r_n_o_dt = find_time_for_reading(station_id_h_r_4,h_r_n_o)
        h_r_n_o_dt_tf = h_r_n_o_dt.strftime("%H:%M:%S")
        h_r_n_o_dt_df = h_r_n_o_dt.strftime("%Y-%m-%d")
        high_text = f"On {h_r_n_o_dt_df} at {h_r_n_o_dt_tf}"

        l_r_n_o = float(lowest_reading_number_only(station_id_h_r_4))
        l_r_n_o_dt = find_time_for_reading(station_id_h_r_4,l_r_n_o)
        l_r_n_o_dt_tf = l_r_n_o_dt.strftime("%H:%M:%S")
        l_r_n_o_dt_df = l_r_n_o_dt.strftime("%Y-%m-%d")
        low_text = f"On {l_r_n_o_dt_df} at {l_r_n_o_dt_tf}"
    

    def dropdown_ws4(event):
        selected_option_ws4 = combobox.get()
        if selected_option_ws4 == "Highest/Lowest readings":
            rainfall_l1_ws4.config(text="The highest reading was:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l2_ws4.config(text=highest_reading(station_id_h_r_4), font=("Yu Gothic UI Semibold", 32))
            rainfall_l3_ws4.config(text=high_text, font=("Yu Gothic UI Semibold", 25))
            rainfall_l4_ws4.config(text="The lowest reading was:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l5_ws4.config(text=lowest_reading(station_id_h_r_4), font=("Yu Gothic UI Semibold", 32))
            rainfall_l6_ws4.config(text=low_text, font=("Yu Gothic UI Semibold", 25))
        elif selected_option_ws4 == "Latest Reading 1":
            rainfall_l1_ws4.config(text="On:")
            rainfall_l2_ws4.config(text=latest_readings(station_id_h_r_4, 0, "date"))
            rainfall_l3_ws4.config(text="At:")
            rainfall_l4_ws4.config(text=latest_readings(station_id_h_r_4, 0, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws4.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws4.config(text=latest_readings(station_id_h_r_4, 0, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws4 == "Latest Reading 2":
            rainfall_l1_ws4.config(text="On:")
            rainfall_l2_ws4.config(text=latest_readings(station_id_h_r_4, 1, "date"))
            rainfall_l3_ws4.config(text="At:")
            rainfall_l4_ws4.config(text=latest_readings(station_id_h_r_4, 1, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws4.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws4.config(text=latest_readings(station_id_h_r_4, 1, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws4 == "Latest Reading 3":
            rainfall_l1_ws4.config(text="On:")
            rainfall_l2_ws4.config(text=latest_readings(station_id_h_r_4, 2, "date"))
            rainfall_l3_ws4.config(text="At:")
            rainfall_l4_ws4.config(text=latest_readings(station_id_h_r_4, 2, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws4.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws4.config(text=latest_readings(station_id_h_r_4, 2, "reading"), font=("Yu Gothic UI Semibold", 32))   
        elif selected_option_ws4 == "Latest Reading 4":
            rainfall_l1_ws4.config(text="On:")
            rainfall_l2_ws4.config(text=latest_readings(station_id_h_r_4, 3, "date"))
            rainfall_l3_ws4.config(text="At:")
            rainfall_l4_ws4.config(text=latest_readings(station_id_h_r_4, 3, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws4.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws4.config(text=latest_readings(station_id_h_r_4, 3, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws4 == "Latest Reading 5":
            rainfall_l1_ws4.config(text="On:")
            rainfall_l2_ws4.config(text=latest_readings(station_id_h_r_4, 4, "date"))
            rainfall_l3_ws4.config(text="At:")
            rainfall_l4_ws4.config(text=latest_readings(station_id_h_r_4, 4, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws4.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws4.config(text=latest_readings(station_id_h_r_4, 4, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws4 == "Latest Reading 6":
            rainfall_l1_ws4.config(text="On:")
            rainfall_l2_ws4.config(text=latest_readings(station_id_h_r_4, 5, "date"))
            rainfall_l3_ws4.config(text="At:")
            rainfall_l4_ws4.config(text=latest_readings(station_id_h_r_4, 5, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws4.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws4.config(text=latest_readings(station_id_h_r_4, 5, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws4 == "Latest Reading 7":
            rainfall_l1_ws4.config(text="On:")
            rainfall_l2_ws4.config(text=latest_readings(station_id_h_r_4, 6, "date"))
            rainfall_l3_ws4.config(text="At:")
            rainfall_l4_ws4.config(text=latest_readings(station_id_h_r_4, 6, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws4.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws4.config(text=latest_readings(station_id_h_r_4, 6, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws4 == "Latest Reading 8":
            rainfall_l1_ws4.config(text="On:")
            rainfall_l2_ws4.config(text=latest_readings(station_id_h_r_4, 7, "date"))
            rainfall_l3_ws4.config(text="At:")
            rainfall_l4_ws4.config(text=latest_readings(station_id_h_r_4, 7, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws4.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws4.config(text=latest_readings(station_id_h_r_4, 7, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws4 == "Latest Reading 9":
            rainfall_l1_ws4.config(text="On:")
            rainfall_l2_ws4.config(text=latest_readings(station_id_h_r_4, 8, "date"))
            rainfall_l3_ws4.config(text="At:")
            rainfall_l4_ws4.config(text=latest_readings(station_id_h_r_4, 8, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws4.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws4.config(text=latest_readings(station_id_h_r_4, 8, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws4 == "Latest Reading 10":
            rainfall_l1_ws4.config(text="On:")
            rainfall_l2_ws4.config(text=latest_readings(station_id_h_r_4, 9, "date"))
            rainfall_l3_ws4.config(text="At:")
            rainfall_l4_ws4.config(text=latest_readings(station_id_h_r_4, 9, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws4.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws4.config(text=latest_readings(station_id_h_r_4, 9, "reading"), font=("Yu Gothic UI Semibold", 32))

    combobox.bind("<<ComboboxSelected>>", dropdown_ws4)
    combobox.set("Highest/Lowest readings")


    rainfall_l1_ws4 = Label(frame_ws4, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text="The highest reading was:")
    rainfall_l1_ws4.grid(row=3, column=0, pady=0, padx=0, sticky="n")

    rainfall_l2_ws4 = Label(frame_ws4, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text=highest_reading(station_id_h_r_4))
    rainfall_l2_ws4.grid(row=4, column=0, pady=0, padx=10, sticky="n")

    rainfall_l3_ws4 = Label(frame_ws4, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text=high_text)
    rainfall_l3_ws4.grid(row=5, column=0, pady=10, padx=10, sticky="n")

    rainfall_l4_ws4 = Label(frame_ws4, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text="The lowest reading was:")
    rainfall_l4_ws4.grid(row=6, column=0, pady=10, padx=10, sticky="n")

    rainfall_l5_ws4 = Label(frame_ws4, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text=lowest_reading(station_id_h_r_4))
    rainfall_l5_ws4.grid(row=7, column=0, pady=10, padx=10, sticky="n")

    rainfall_l6_ws4 = Label(frame_ws4, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text=low_text)
    rainfall_l6_ws4.grid(row=8, column=0, pady=10, padx=10, sticky="n")


    root_ws4.mainloop()

def ws5():
    root_ws5 = Tk(className="Weather Station 5")
    root_ws5.grid_rowconfigure(0, weight=1)
    root_ws5.grid_columnconfigure(0, weight=1)
    root_ws5.geometry("1280x720")

    frame_ws5 = Frame(root_ws5, bg="#ffccde", height=720 , width=1280 )
    frame_ws5.grid(row=0, column=0, sticky="nsew")

    def go_back_to_home():
        root_ws5.destroy()  
        show_frame(frame)  


    homeButton_ws5 = Button(frame_ws5, bg="#ffccde", bd="0", activebackground="white", font=("Yu Gothic UI Semibold", 18), text= "< Home", command=go_back_to_home)
    homeButton_ws5.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    rainfall_title_ws5 = Label(frame_ws5, background="#ffccde", font=("Yu Gothic UI Semibold", 60), text="Rainfall")
    rainfall_title_ws5.grid(row=0, column=0, pady=0, padx=500, sticky="n")

    rainfall_subtitle_ws5 = Label(frame_ws5, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text="Weather Station 5")
    rainfall_subtitle_ws5.grid(row=1, column=0, pady=0, padx=500, sticky="n")

    ws5_info = Label(frame_ws5, background="white",anchor=CENTER, font=("Yu Gothic UI Semibold", 16), text=f"Weather Station ID: {station_id_h_r_5}                {weather_station_region(station_id_h_r_5, 'reference')}                                Region: {weather_station_region(station_id_h_r_5, 'region')}  ")
    ws5_info.grid(row=2, column=0, pady=10, padx=0, sticky="n")

    combobox = Combobox(frame_ws5, height=50, background="white", font=("Yu Gothic UI Semibold", 16), values=["Highest/Lowest readings","Latest Reading 1","Latest Reading 2","Latest Reading 3","Latest Reading 4","Latest Reading 5","Latest Reading 6","Latest Reading 7","Latest Reading 8","Latest Reading 9","Latest Reading 10"])
    combobox.grid(row=3, column=0, padx=10, pady=20, sticky="w")

    h_r_n_o = float(highest_reading_number_only(station_id_h_r_5))

    if h_r_n_o == 0.00:
        high_text = "N/A"
        low_text = "N/A"
    else:
        h_r_n_o_dt = find_time_for_reading(station_id_h_r_5,h_r_n_o)
        h_r_n_o_dt_tf = h_r_n_o_dt.strftime("%H:%M:%S")
        h_r_n_o_dt_df = h_r_n_o_dt.strftime("%Y-%m-%d")
        high_text = f"On {h_r_n_o_dt_df} at {h_r_n_o_dt_tf}"

        l_r_n_o = float(lowest_reading_number_only(station_id_h_r_5))
        l_r_n_o_dt = find_time_for_reading(station_id_h_r_5,l_r_n_o)
        l_r_n_o_dt_tf = l_r_n_o_dt.strftime("%H:%M:%S")
        l_r_n_o_dt_df = l_r_n_o_dt.strftime("%Y-%m-%d")
        low_text = f"On {l_r_n_o_dt_df} at {l_r_n_o_dt_tf}"
    

    def dropdown_ws5(event):
        selected_option_ws5 = combobox.get()
        if selected_option_ws5 == "Highest/Lowest readings":
            rainfall_l1_ws5.config(text="The highest reading was:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l2_ws5.config(text=highest_reading(station_id_h_r_5), font=("Yu Gothic UI Semibold", 32))
            rainfall_l3_ws5.config(text=high_text, font=("Yu Gothic UI Semibold", 25))
            rainfall_l4_ws5.config(text="The lowest reading was:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l5_ws5.config(text=lowest_reading(station_id_h_r_5), font=("Yu Gothic UI Semibold", 32))
            rainfall_l6_ws5.config(text=low_text, font=("Yu Gothic UI Semibold", 25))
        elif selected_option_ws5 == "Latest Reading 1":
            rainfall_l1_ws5.config(text="On:")
            rainfall_l2_ws5.config(text=latest_readings(station_id_h_r_5, 0, "date"))
            rainfall_l3_ws5.config(text="At:")
            rainfall_l4_ws5.config(text=latest_readings(station_id_h_r_5, 0, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws5.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws5.config(text=latest_readings(station_id_h_r_5, 0, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws5 == "Latest Reading 2":
            rainfall_l1_ws5.config(text="On:")
            rainfall_l2_ws5.config(text=latest_readings(station_id_h_r_5, 1, "date"))
            rainfall_l3_ws5.config(text="At:")
            rainfall_l4_ws5.config(text=latest_readings(station_id_h_r_5, 1, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws5.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws5.config(text=latest_readings(station_id_h_r_5, 1, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws5 == "Latest Reading 3":
            rainfall_l1_ws5.config(text="On:")
            rainfall_l2_ws5.config(text=latest_readings(station_id_h_r_5, 2, "date"))
            rainfall_l3_ws5.config(text="At:")
            rainfall_l4_ws5.config(text=latest_readings(station_id_h_r_5, 2, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws5.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws5.config(text=latest_readings(station_id_h_r_5, 2, "reading"), font=("Yu Gothic UI Semibold", 32))   
        elif selected_option_ws5 == "Latest Reading 4":
            rainfall_l1_ws5.config(text="On:")
            rainfall_l2_ws5.config(text=latest_readings(station_id_h_r_5, 3, "date"))
            rainfall_l3_ws5.config(text="At:")
            rainfall_l4_ws5.config(text=latest_readings(station_id_h_r_5, 3, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws5.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws5.config(text=latest_readings(station_id_h_r_5, 3, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws5 == "Latest Reading 5":
            rainfall_l1_ws5.config(text="On:")
            rainfall_l2_ws5.config(text=latest_readings(station_id_h_r_5, 4, "date"))
            rainfall_l3_ws5.config(text="At:")
            rainfall_l4_ws5.config(text=latest_readings(station_id_h_r_5, 4, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws5.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws5.config(text=latest_readings(station_id_h_r_5, 4, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws5 == "Latest Reading 6":
            rainfall_l1_ws5.config(text="On:")
            rainfall_l2_ws5.config(text=latest_readings(station_id_h_r_5, 5, "date"))
            rainfall_l3_ws5.config(text="At:")
            rainfall_l4_ws5.config(text=latest_readings(station_id_h_r_5, 5, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws5.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws5.config(text=latest_readings(station_id_h_r_5, 5, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws5 == "Latest Reading 7":
            rainfall_l1_ws5.config(text="On:")
            rainfall_l2_ws5.config(text=latest_readings(station_id_h_r_5, 6, "date"))
            rainfall_l3_ws5.config(text="At:")
            rainfall_l4_ws5.config(text=latest_readings(station_id_h_r_5, 6, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws5.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws5.config(text=latest_readings(station_id_h_r_5, 6, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws5 == "Latest Reading 8":
            rainfall_l1_ws5.config(text="On:")
            rainfall_l2_ws5.config(text=latest_readings(station_id_h_r_5, 7, "date"))
            rainfall_l3_ws5.config(text="At:")
            rainfall_l4_ws5.config(text=latest_readings(station_id_h_r_5, 7, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws5.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws5.config(text=latest_readings(station_id_h_r_5, 7, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws5 == "Latest Reading 9":
            rainfall_l1_ws5.config(text="On:")
            rainfall_l2_ws5.config(text=latest_readings(station_id_h_r_5, 8, "date"))
            rainfall_l3_ws5.config(text="At:")
            rainfall_l4_ws5.config(text=latest_readings(station_id_h_r_5, 8, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws5.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws5.config(text=latest_readings(station_id_h_r_5, 8, "reading"), font=("Yu Gothic UI Semibold", 32))
        elif selected_option_ws5 == "Latest Reading 10":
            rainfall_l1_ws5.config(text="On:")
            rainfall_l2_ws5.config(text=latest_readings(station_id_h_r_5, 9, "date"))
            rainfall_l3_ws5.config(text="At:")
            rainfall_l4_ws5.config(text=latest_readings(station_id_h_r_5, 9, "time"), font=("Yu Gothic UI Semibold", 32))
            rainfall_l5_ws5.config(text="The rainfall reading was recorded as:", font=("Yu Gothic UI Semibold", 25))
            rainfall_l6_ws5.config(text=latest_readings(station_id_h_r_5, 9, "reading"), font=("Yu Gothic UI Semibold", 32))

    combobox.bind("<<ComboboxSelected>>", dropdown_ws5)
    combobox.set("Highest/Lowest readings")


    rainfall_l1_ws5 = Label(frame_ws5, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text="The highest reading was:")
    rainfall_l1_ws5.grid(row=3, column=0, pady=0, padx=0, sticky="n")

    rainfall_l2_ws5 = Label(frame_ws5, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text=highest_reading(station_id_h_r_5))
    rainfall_l2_ws5.grid(row=4, column=0, pady=0, padx=10, sticky="n")

    rainfall_l3_ws5 = Label(frame_ws5, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text=high_text)
    rainfall_l3_ws5.grid(row=5, column=0, pady=10, padx=10, sticky="n")

    rainfall_l4_ws5 = Label(frame_ws5, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text="The lowest reading was:")
    rainfall_l4_ws5.grid(row=6, column=0, pady=10, padx=10, sticky="n")

    rainfall_l5_ws5 = Label(frame_ws5, background="#ffccde", font=("Yu Gothic UI Semibold", 32), text=lowest_reading(station_id_h_r_5))
    rainfall_l5_ws5.grid(row=7, column=0, pady=10, padx=10, sticky="n")

    rainfall_l6_ws5 = Label(frame_ws5, background="#ffccde", font=("Yu Gothic UI Semibold", 25), text=low_text)
    rainfall_l6_ws5.grid(row=8, column=0, pady=10, padx=10, sticky="n")


    root_ws5.mainloop()

homeButton = Button(frame, bg="#ffccde", bd="0", activebackground="white", font=("Yu Gothic UI Semibold", 18), text= "< Home")
homeButton.pack_forget()

rainfall_title = Label(frame, background="#ffccde", font=("Yu Gothic UI Semibold", 60), text="Rainfall")
rainfall_title.grid(row=0, column=0, pady=10, padx=500, sticky="n")

ws1Button = Button(frame, bg="#ffccde", bd="1", activebackground="white", font=("Yu Gothic UI Semibold", 25), text="Weather Station 1", command=ws1)
ws1Button.grid(row=1, column=0, pady=20, padx=500, sticky="n")

ws2Button = Button(frame, bg="#ffccde", bd="1", activebackground="white", font=("Yu Gothic UI Semibold", 25), text="Weather Station 2", command=ws2)
ws2Button.grid(row=2, column=0, pady=20, padx=500, sticky="n")

ws3Button = Button(frame, bg="#ffccde", bd="1", activebackground="white", font=("Yu Gothic UI Semibold", 25), text="Weather Station 3", command=ws3)
ws3Button.grid(row=3, column=0, pady=20, padx=500, sticky="n")

ws4Button = Button(frame, bg="#ffccde", bd="1", activebackground="white", font=("Yu Gothic UI Semibold", 25), text="Weather Station 4", command=ws4)
ws4Button.grid(row=4, column=0, pady=20, padx=500, sticky="n")

ws5Button = Button(frame, bg="#ffccde", bd="1", activebackground="white", font=("Yu Gothic UI Semibold", 25), text="Weather Station 5", command=ws5)
ws5Button.grid(row=5, column=0, pady=20, padx=500, sticky="n")

homeButton.bind('<Enter>', on_enter)
homeButton.bind('<Leave>', on_leave)

root.mainloop()

#endregion

## endddd