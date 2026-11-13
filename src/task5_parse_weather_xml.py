import xml.etree.ElementTree as ET
import csv
from typing import List, Dict, Any


def parse_weather_xml(xml_file: str) -> List[Dict[str, Any]]:
    """
    Parse weather data from an XML file.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        list of dict: A list of dictionaries with parsed weather data.

    Raises:
        FileNotFoundError: If the XML file does not exist.
        ET.ParseError: If the XML file is malformed.
    """
    with open(xml_file, "r", encoding="utf-8") as f:
        xml_content = f.read()

    root = ET.fromstring(xml_content)
    parsed_data: List[Dict[str, Any]] = []

    for day in root.findall("day"):
        date = day.findtext("date", default="").strip()
        temperature = float(day.findtext("temperature", default="0").strip())
        humidity = int(day.findtext("humidity", default="0").strip())
        precipitation = float(day.findtext("precipitation", default="0").strip())

        parsed_data.append({
            "date": date,
            "temperature": temperature,
            "humidity": humidity,
            "precipitation": precipitation,
        })

    return parsed_data


def save_to_csv(data: List[Dict[str, Any]], filename: str = "parsed_weather_data.csv") -> None:
    """
    Save parsed weather data to a CSV file.

    Args:
        data (list of dict): Parsed weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    headers = ["Date", "Temperature", "Humidity", "Precipitation"]
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in data:
            writer.writerow([
                row["date"],
                row["temperature"],
                row["humidity"],
                row["precipitation"],
            ])


if __name__ == "__main__":
    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(script_dir, "weather_data.xml")
        weather_data = parse_weather_xml(xml_path)

        save_to_csv(weather_data)
        print("Data has been successfully parsed and saved to parsed_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")