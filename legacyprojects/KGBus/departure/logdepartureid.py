import requests
import json

# Array of numbers to determine which URL to use
url_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 24, 25, 26, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613]

# Dictionary to map each number to a URL format string
url_map = {
    1: "https://gas-kg.herokuapp.com/timetable/lines/1/departures?day={}",
    2: "https://gas-kg.herokuapp.com/timetable/lines/393/departures?day={}",
    3: "https://gas-kg.herokuapp.com/timetable/lines/748/departures?day={}",
    4: "https://gas-kg.herokuapp.com/timetable/lines/887/departures?day={}",
    5: "https://gas-kg.herokuapp.com/timetable/lines/967/departures?day={}",
    6: "https://gas-kg.herokuapp.com/timetable/lines/1138/departures?day={}",
    7: "https://gas-kg.herokuapp.com/timetable/lines/12688/departures?day={}",
    8: "https://gas-kg.herokuapp.com/timetable/lines/11302/departures?day={}",
    9: "https://gas-kg.herokuapp.com/timetable/lines/1401/departures?day={}",
    10: "https://gas-kg.herokuapp.com/timetable/lines/1521/departures?day={}",
    11: "https://gas-kg.herokuapp.com/timetable/lines/1657/departures?day={}",
    13: "https://gas-kg.herokuapp.com/timetable/lines/1734/departures?day={}",
    14: "https://gas-kg.herokuapp.com/timetable/lines/1853/departures?day={}",
    15: "https://gas-kg.herokuapp.com/timetable/lines/1934/departures?day={}",
    16: "https://gas-kg.herokuapp.com/timetable/lines/2166/departures?day={}",
    17: "https://gas-kg.herokuapp.com/timetable/lines/2365/departures?day={}",
    18: "https://gas-kg.herokuapp.com/timetable/lines/2530/departures?day={}",
    19: "https://gas-kg.herokuapp.com/timetable/lines/2589/departures?day={}",
    20: "https://gas-kg.herokuapp.com/timetable/lines/2721/departures?day={}",
    24: "https://gas-kg.herokuapp.com/timetable/lines/2858/departures?day={}",
    25: "https://gas-kg.herokuapp.com/timetable/lines/2976/departures?day={}",
    26: "https://gas-kg.herokuapp.com/timetable/lines/10777/departures?day={}",
    600: "https://gas-kg.herokuapp.com/timetable/lines/3222/departures?day={}",
    601: "https://gas-kg.herokuapp.com/timetable/lines/3287/departures?day={}",
    602: "https://gas-kg.herokuapp.com/timetable/lines/3346/departures?day={}",
    603: "https://gas-kg.herokuapp.com/timetable/lines/3453/departures?day={}",
    604: "https://gas-kg.herokuapp.com/timetable/lines/3534/departures?day={}",
    605: "https://gas-kg.herokuapp.com/timetable/lines/3623/departures?day={}",
    606: "https://gas-kg.herokuapp.com/timetable/lines/3693/departures?day={}",
    607: "https://gas-kg.herokuapp.com/timetable/lines/3795/departures?day={}",
    608: "https://gas-kg.herokuapp.com/timetable/lines/4889/departures?day={}",
    609: "https://gas-kg.herokuapp.com/timetable/lines/3878/departures?day={}",
    610: "https://gas-kg.herokuapp.com/timetable/lines/3955/departures?day={}",
    611: "https://gas-kg.herokuapp.com/timetable/lines/4049/departures?day={}",
    612: "https://gas-kg.herokuapp.com/timetable/lines/4146/departures?day={}",
    613: "https://gas-kg.herokuapp.com/timetable/lines/12437/departures?day={}"
}

# Possible day types to cycle through
day_types = ["saturday", "work_day", "sunday"]

# File name to save departure IDs
output_file = "departure_ids.txt"

# List to accumulate all departure IDs
all_departure_ids = []

# Loop through each number and day type
for url_id in url_ids:
    url_template = url_map.get(url_id)
    if not url_template:
        print(f"No URL found for ID {url_id}. Skipping...")
        continue  # Skip if the ID doesn't have a corresponding URL
    
    for day in day_types:
        url = url_template.format(day)
        
        try:
            # Fetching the JSON data from the URL
            response = requests.get(url)
            response.raise_for_status()  # Ensure we got a valid response
            
            # Load JSON data
            data = response.json()
            
            # Extract departure IDs from both directionA and directionB
            for direction in ['directionA', 'directionB']:
                if direction in data:
                    print("collected data")
                    all_departure_ids.extend(str(dep['departureId']) for dep in data[direction] if 'departureId' in dep)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data for URL ID {url_id} ({day}): {e}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON data for URL ID {url_id} ({day}).")
        except Exception as e:
            print(f"An unexpected error occurred for URL ID {url_id} ({day}): {e}")

# Write all collected departure IDs to the output file in a single line
if all_departure_ids:
    formatted_departure_ids = "@" + ", @".join(all_departure_ids)
    with open(output_file, "w") as file:
        file.write(formatted_departure_ids)
    print(f"All departure IDs have been written to {output_file}")
else:
    print("No departure IDs were found.")
