# stats_module.py
# Модуль із підпрограмами для статистичної обробки показників
# виконати імпорт модулів, які викорстовуються, наприклад:
import statistics

def get_average(data_dict):
    average = sum(data_dict) / len(data_dict)
    return average

def get_min(data_dict,title):
    minimum = min(data_dict)
    return minimum

def get_max(data_dict):
    maximum = max(data_dict) 
    return maximum

def get_median(data_dict):
    median = statistics.median(data_dict) 
    return median

def find_jumps(data_dict, threshold):
    jumps = {"category": [], "value 1": [], "value2": []}
    for i in range(1, data_dict):
        if abs(data_dict[i+1] - data_dict[i]) > threshold:
            jumps[i].append((i, data_dict[i], data_dict[i+1]))
    return jumps

def show_table(data_dict, title):
    print (f"\nТаблиця показників: {title}")
    print ("Мітка часу | Значення")
    for time_label, value in data_dict[title].items():
        print (f"   {time_label}   \t |  {value}")

