# main.py
# Основна програма для обробки показників системи "розумний будинок"

import stats_module as sm # підключення модулю

### TODO: основну програму можна написати однією функцією main(), або окремі задачі розділити на окремі підпрограми, наприклад наступним чином:

def parse_input(input_str):
    data = input_str.split()
    dataFloat = [float(value) for value in data]
    return dataFloat

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


def process_measurements(title, data_dict, threshold):
    print ("=== Обробка показників для:", title)
    sm.show_table(data_dict, title)
    avgTemp, avgHum, avgPres = sm.get_average(data_dict)
    print (f"\nСередні значення - Температура: {avgTemp:.2f}, Вологість: {avgHum:.2f}, Тиск: {avgPres:.2f}")
    minTemp, minHum, minPres = sm.get_min(data_dict)
    print (f"Мінімальні значення - Температура: {minTemp:.2f}, Вологість: {minHum:.2f}, Тиск: {minPres:.2f}")
    maxTemp, maxHum, maxPres = sm.get_max(data_dict)
    print (f"Максимальні значення - Температура: {maxTemp:.2f}, Вологість: {maxHum:.2f}, Тиск: {maxPres:.2f}")
    medTemp, medHum, medPres = sm.get_median(data_dict)
    print (f"Медіанні значення - Температура: {medTemp:.2f}, Вологість: {medHum:.2f}, Тиск: {medPres:.2f}")
    jumps = sm.find_jumps(data_dict, threshold)
    print ("\nВиявлені стрибки значень (поріг:", threshold, "):")

def main():
    print("=== Обробка показів системи 'Розумний будинок' ===")
    temperature_input = input("Введіть показники температури (через пробіл): ")
    humidity_input = input("Введіть показники вологості (через пробіл): ")
    pressure_input = input("Введіть показники тиску (через пробіл): ")
    thresholdTemp = 7.0
    thresholdHum = 20.0
    thresholdPres = 5000
    temp_list = parse_input(temperature_input)
    temp_list = parse_input(temperature_input)
    hum_list = parse_input(humidity_input)
    pres_list = parse_input(pressure_input)
    data_dict = create_data_dict(temp_list, hum_list, pres_list)
    process_measurements("temperature", data_dict, thresholdTemp)
    process_measurements("humidity", data_dict, thresholdHum)
    process_measurements("pressure", data_dict, thresholdPres)


if __name__ == "__main__":
    main()