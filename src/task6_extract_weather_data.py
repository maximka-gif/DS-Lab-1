import csv
import re
from typing import List, Dict, Any


def clean_text(line: str) -> str:
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    line = line.replace("\xa0", " ")
    return line.encode("ascii", "ignore").decode("ascii").strip()


def extract_weather_data(text_file: str) -> List[Dict[str, Any]]:
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str): Path to the text file.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.

    Raises:
        FileNotFoundError: If the text file does not exist.
    """
    pattern = re.compile(
        r"Date:\s*(?P<date>\d{4}-\d{2}-\d{2}),\s*"
        r"Max Temp:\s*(?P<max_temp>-?\d+(?:\.\d+)?)C,\s*"
        r"Min Temp:\s*(?P<min_temp>-?\d+(?:\.\d+)?)C,\s*"
        r"Humidity:\s*(?P<humidity>\d+)%,\s*"
        r"Precipitation:\s*(?P<precipitation>\d+(?:\.\d+)?)mm"
    )

    extracted_data: List[Dict[str, Any]] = []
    with open(text_file, "r", encoding="utf-8") as f:
        for line in f:
            cleaned = clean_text(line)
            if not cleaned:
                continue
            match = pattern.search(cleaned)
            if match:
                extracted_data.append({
                    "date": match.group("date"),
                    "max_temperature": float(match.group("max_temp")),
                    "min_temperature": float(match.group("min_temp")),
                    "humidity": int(match.group("humidity")),
                    "precipitation": float(match.group("precipitation")),
                })

    return extracted_data


def save_to_csv(data: List[Dict[str, Any]], filename: str = "extracted_weather_data.csv") -> None:
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Humidity", "Precipitation"]
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in data:
            writer.writerow([
                row["date"],
                row["max_temperature"],
                row["min_temperature"],
                row["humidity"],
                row["precipitation"],
            ])


if __name__ == "__main__":
    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.join(script_dir, "weather_report.txt")
        weather_data = extract_weather_data(txt_path)

        save_to_csv(weather_data)
        print("Data has been successfully extracted and saved to extracted_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")