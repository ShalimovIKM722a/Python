import statistics
from typing import List, Optional, Dict, Any

def get_average(values) -> Optional[float]:
    """Повертає середнє значення списку."""
    return round(statistics.mean(values), 2) if values else None

def get_min(values) -> Optional[float]:
    """Повертає мінімальне значення."""
    return min(values) if values else None

def get_max(values) -> Optional[float]:
    """Повертає максимальне значення."""
    return max(values) if values else None

def get_median(values) -> Optional[float]:
    """Повертає медіану."""
    return round(statistics.median(values), 2) if values else None

def detect_jumps(values: List[float], timestamps: List[str], threshold: float) -> List[str]:
    """
    Виявляє різкі перепади між сусідніми значеннями.
    Повертає список часових міток, де відбувся перепад.
    """
    jumps = []
    for i in range(1, len(values)):
        if abs(values[i] - values[i - 1]) > threshold:
            jumps.append(timestamps[i])
    return jumps

def print_table(parameter_name, data_dict):
    """Виводить таблицю з показниками певного параметра."""
    print(f"\nПоказники для параметра: {parameter_name}")
    print("+----------------------+-------------+")
    print(f"| {'Timestamp':<20} | {parameter_name:<11} |")
    print("+----------------------+-------------+")
    for timestamp, value in data_dict.items():
        print(f"| {timestamp:<20} | {value:<11} |")
    print("+----------------------+-------------+")

def print_stats(parameter_name: str, stats: Dict[str, Any]) -> None:
    """Виводить розраховані характеристики (мін, макс, стрибки) у вигляді таблиці."""
    print(f"\nСтатистика для параметра: {parameter_name}")
    print("+----------------------+--------------------------------+")
    print(f"| {'Характеристика':<20} | {'Значення':<30} |")
    print("+----------------------+--------------------------------+")
    
    for key, value in stats.items():
        if isinstance(value, list):
            val_str = ", ".join(value) if value else "Немає"
        else:
            val_str = str(value)
            
        print(f"| {key:<20} | {val_str:<30} |")
        
    print("+----------------------+--------------------------------+")