import csv
import json
import configparser
import sys
import argparse
import stats_utils as su
import tomllib

# Стандартні пороги різких перепадів
DEFAULT_THRESHOLDS = {
    "temperature": 7,
    "humidity": 20,
    "pressure": 5000
}

def parse_arguments():
    """
    Налаштовує парсер аргументів командного рядка.
    Отримує назву файлу (позиційний аргумент) та опції порогів.
    """
    parser = argparse.ArgumentParser(description="Аналіз даних сенсорів з CSV файлу.")
    
    # Додаємо аргумент filename прямо сюди. 
    # nargs="?" означає, що цей аргумент необов'язковий.
    parser.add_argument("filename", nargs="?", help="Шлях до CSV файлу")
    
    parser.add_argument("-t", "--temp", type=float, help="Поріг для температури")
    parser.add_argument("-H", "--hum", type=float, help="Поріг для вологості")
    parser.add_argument("-p", "--press", type=float, help="Поріг для тиску")
    
    return parser.parse_args()

def read_csv(filename):
    """Зчитує дані з CSV і повертає словник з показниками."""
    data = {"temperature": {}, "humidity": {}, "pressure": {}}
    try:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamp = row["timestamp"]
                data["temperature"][timestamp] = float(row["temperature"])
                data["humidity"][timestamp] = float(row["humidity"])
                data["pressure"][timestamp] = float(row["pressure"])
        return data
    except FileNotFoundError:
        print(f"Помилка: Файл '{filename}' не знайдено.")
        return None
    except Exception as e:
        print(f"Помилка при зчитуванні файлу: {e}")
        return None

def read_config(filename):
    """
    Зчитує файл конфігурації TOML.
    Повертає словники для General налаштувань та статистики.
    """
    stats_settings = {}
    general_settings = {}

    try:
        # tomllib вимагає відкриття файлу у бінарному режимі "rb"
        with open(filename, "rb") as f:
            config_data = tomllib.load(f)

        # Розбираємо завантажений словник
        for section, content in config_data.items():
            if section == "General":
                general_settings = content
            else:
                # У TOML "stats" вже є списком, сплітіння не потрібне!
                stats_settings[section] = content.get("stats", [])
                
        return general_settings, stats_settings

    except FileNotFoundError:
        print(f"Попередження: Конфігураційний файл '{filename}' не знайдено.")
        return {}, {}
    except tomllib.TOMLDecodeError:
        print(f"Помилка: Невірний формат файлу '{filename}'.")
        sys.exit(1)

def get_filename(cli_filename, config_filename_option):
    """
    Визначає пріоритет: 1. CLI -> 2. Config -> 3. Input
    """
    if cli_filename:
        return cli_filename
    
    if config_filename_option:
        return config_filename_option

    filename = input("Введіть шлях до CSV файлу: ").strip()
    return filename.strip('"').strip("'")

def get_current_thresholds(args):
    """Оновлює пороги, якщо користувач задав їх через консоль."""
    thresholds = DEFAULT_THRESHOLDS.copy()
    
    if args.temp is not None:
        thresholds["temperature"] = args.temp
    if args.hum is not None:
        thresholds["humidity"] = args.hum
    if args.press is not None:
        thresholds["pressure"] = args.press
        
    return thresholds

def main():
    # 1. Спочатку парсимо аргументи командного рядка!
    args = parse_arguments()

    # 2. Зчитування налаштувань з файлу
    general_conf, stats_conf = read_config("config.toml")
    
    # 3. Визначення фінального імені файлу
    # args.filename береться з argparse
    csv_file_path = get_filename(args.filename, general_conf.get("filename"))
    print(f"Використовується файл даних: {csv_file_path}")

    # 4. Визначення актуальних порогів
    current_thresholds = get_current_thresholds(args)

    # 5. Зчитування даних
    data = read_csv(csv_file_path)
    if data is None:
        return
    
    results = {}

    # 6. Обробка кожного параметра
    for param, values_dict in data.items():
        if not values_dict:
            continue

        timestamps = list(values_dict.keys())
        values = list(values_dict.values())
        results[param] = {}

        # Виведення таблиці
        su.print_table(param, values_dict)

        # Виконання розрахунків (Використовуємо stats_conf, а не config!)
        if param in stats_conf:
            for stat in stats_conf[param]:
                if stat == "average":
                    results[param]["average"] = su.get_average(values)
                elif stat == "min":
                    results[param]["min"] = su.get_min(values)
                elif stat == "max":
                    results[param]["max"] = su.get_max(values)
                elif stat == "median":
                    results[param]["median"] = su.get_median(values)
                elif stat == "jumps":
                    # Використовуємо оновлені пороги current_thresholds
                    results[param]["jumps"] = su.detect_jumps(values, timestamps, current_thresholds.get(param, 0))
            
            # Виведення статистики
            su.print_stats(param, results[param])

    # 7. Збереження результатів у JSON
    try:
        with open("results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print("\nРезультати збережено у файлі results.json")
    except Exception as e:
        print(f"Помилка при збереженні результатів: {e}")

if __name__ == "__main__":
    main()