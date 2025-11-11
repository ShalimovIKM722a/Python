# stats_module.py
# Модуль із підпрограмами для статистичної обробки показників

# виконати імпорт модулів, які викорстовуються, наприклад:
import statistics

def get_average(data_dict):
    temperatureAverage = sum(data_dict["temperature"].values()) / len(data_dict)
    humidityAverage = sum(data_dict["humidity"].values()) / len(data_dict)
    pressureAverage = sum(data_dict["pressure"].values()) / len(data_dict)
    return temperatureAverage, humidityAverage, pressureAverage

     
def get_min(data_dict):
    temperatureMin = min(data_dict["temperature"].values()) 
    humidityMin = min(data_dict["humidity"].values())
    pressureMin = min(data_dict["pressure"].values())
    return temperatureMin, humidityMin, pressureMin



def get_max(data_dict):
    temperatureMax = max(data_dict["temperature"].values()) 
    humidityMax = max(data_dict["humidity"].values())
    pressureMax = max(data_dict["pressure"].values())
    return temperatureMax, humidityMax, pressureMax


def get_median(data_dict):
    temperatureMedian = statistics.median(data_dict["temperature"].values()) 
    humidityMedian = statistics.median(data_dict["humidity"].values())
    pressureMedian = statistics.median(data_dict["pressure"].values())
    return temperatureMedian, humidityMedian, pressureMedian

def find_jumps(data_dict, threshold):
    jumps = {"temperature": [], "humidity": [], "pressure": []}
    for key in data_dict:
        values = list(data_dict[key].values())
        for i in range(len(values) - 1):
            if abs(values[i+1] - values[i]) > threshold:
                jumps[key].append((i, values[i], values[i+1]))

    return jumps

def show_table(data_dict, title):
    print (f"\nТаблиця показників: {title}")
    print ("Мітка часу | Значення")
    for time_label, value in data_dict[title].items():
        print (f"   {time_label}   \t |  {value}")

