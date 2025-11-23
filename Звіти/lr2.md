Ось ваш код, переформатований у Markdown з використанням хештегів для структуризації, як ви просили. Я розділив його на два логічні блоки (модуль та головний файл), щоб виправити контекст використання `sm.` (звернення до імпортованого модуля).

# Файл stats_module.py

## Імпорт модуля

```python
import statistics
```

## Функція повертає середнє значення

```python
def get_average(values):
    average = sum(values) / len(values)
    return average
```

## Функція повертає мінімальне значення

```python
def get_min(values):
    minimum = min(values)
    return minimum
```

## Функція повертає максимальне значення

```python
def get_max(values):
    maximum = max(values) 
    return maximum
```

## Функція повертає медіану

```python
def get_median(values):
    median = statistics.median(values) 
    return median
```

## Функція знаходить різкі перепади між сусідніми значеннями

```python
def find_jumps(values, threshold):
    # Виправлено помилку в ключі "value 1" -> "value1" для відповідності коду
    jumps = {"index": [], "value1": [], "value2": []}
    for i in range(1, len(values)-1):
        if abs(values[i+1] - values[i]) > threshold:
            jumps["index"].append(i)
            jumps["value1"].append(values[i])
            jumps["value2"].append(values[i+1])
    return jumps
```

## Функція виводить таблицю значень

```python
def show_table(data_dict, title):
    print (f"\nТаблиця показників: {title}")
    print ("Мітка часу | Значення")
    for time_label, value in data_dict[title].items():
        print (f"   {time_label}   \t |  {value}")
```

## Функція перетворює текстовий ввід на список чисел

```python
def parse_input(input_str):
    data = input_str.split()
    dataFloat = [float(value) for value in data]
    return dataFloat
```

## Функція формує словник даних

```python
def create_data_dict(temp_list, hum_list, pres_list):
    data_dict = {
        "temperature": {},
        "humidity": {},
        "pressure": {}
    }
    for i in range(len(temp_list)):
        time = f"T{i+1}"
        data_dict["temperature"][time] = temp_list[i]
        data_dict["humidity"][time] = hum_list[i]
        data_dict["pressure"][time] = pres_list[i]

    return data_dict
```

-----

# Головний файл (main.py)

## Імпорт та функція обробки

```python
import stats_module as sm

def process_measurements(title, data_dict, threshold):
    print (f"=== Обробка показників для:{title}===")
    value = list(data_dict[title].values())
    sm.show_table(data_dict, title)
    
    avg = sm.get_average(value)
    print (f"Середні значення: {avg:.2f}")
    
    min_val = sm.get_min(value)
    print (f"Мінімальні значення: {min_val:.2f}")
    
    max_val = sm.get_max(value)
    print (f"Максимальні значення: {max_val:.2f}")
    
    med = sm.get_median(value)
    print (f"Медіанні значення: {med:.2f}")
    
    jumps = sm.find_jumps(value, threshold)
    if jumps["index"]:
        print("Виявлені стрибки:")
        for i in range(len(jumps["index"])):
            print(f"  Між T{jumps['index'][i]+1} і T{jumps['index'][i]+2}: "
                  f"{jumps['value1'][i]} → {jumps['value2'][i]}")
    else:
        print("Стрибків не виявлено.")
```

## Головна функція

```python
def main():
    print("=== Обробка показів системи 'Розумний будинок' ===")
    temperature_input = input("Введіть показники температури (через пробіл): ")
    humidity_input = input("Введіть показники вологості (через пробіл): ")
    pressure_input = input("Введіть показники тиску (через пробіл): ")
    
    # Ця змінна запитується, але не використовується в поточній логіці
    title = input("Введіть назву (опціонально): ") 
    
    temp_list = sm.parse_input(temperature_input)
    hum_list = sm.parse_input(humidity_input)
    pres_list = sm.parse_input(pressure_input)
    
    data_dict = sm.create_data_dict(temp_list, hum_list, pres_list)
    
    process_measurements("temperature", data_dict, threshold=7)
    process_measurements("humidity", data_dict, threshold=20)
    process_measurements("pressure", data_dict, threshold=5000)

if __name__ == "__main__":
    main()
```
# Файл sensors/__init__.py
 забезпечує використання модулів у складі пакета sensors дозволяє отримувати доступ до функцій модуля stats_module напряму без необхідності використання import sensors.stats_module, а потім sensors.stats_module.get_average(...) або import sensors.stats_module as sm, а потім sm.get_average(...) також можна: from sensors import stats_module → stats_module.get_average(...) також можна: from sensors.stats_module import get_average → get_average(...)
 ``` python
from .stats_module import (
    get_average,
    get_min,
    get_max,
    get_median,
    find_jumps,
    show_table
)
```

 визначає, що можна імпортувати, а що - заборонено (службові елементи) при використанні варіанту конструкції: from sensors import *

``` python
__all__ = [
    "get_average",
    "get_min",
    "get_max",
    "get_median",
    "find_jumps",
    "show_table"
]
```