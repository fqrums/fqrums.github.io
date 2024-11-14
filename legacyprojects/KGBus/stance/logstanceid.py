import requests
import json

# Function to fetch departure IDs from a URL
def fetch_departure_ids(departure_url):
    try:
        print(f"Fetching departure IDs from: {departure_url}")
        response = requests.get(departure_url, timeout=10)  # Add a timeout to avoid infinite wait
        response.raise_for_status()
        # Extract the content as a string and clean it
        content = response.text.strip()
        print(f"Fetched raw departure IDs: {content[:100]}...")  # Show only the first 100 characters
        # Split by commas, remove '@' prefix, and strip any whitespace
        departure_ids = [dep_id.strip().lstrip('@') for dep_id in content.split(',')]
        print(f"Processed departure IDs: {departure_ids}")
        return departure_ids
    except requests.RequestException as e:
        print(f"Error fetching departure IDs: {e}")
        return []

# Function to fetch stance IDs from a URL
def fetch_stance_ids(departure_ids, base_url, output_file):
    stance_ids = set()  # Use a set to automatically handle duplicates
    print(f"Fetching stance IDs for {len(departure_ids)} departure IDs...")

    for departure_id in departure_ids:
        url = f"{base_url}/{departure_id}"
        print(f"Fetching stance ID from: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an error for HTTP errors
            data = response.json()
            print(f"Received JSON for {departure_id}: {data}")
            if 'stanceId' in data:
                stance_ids.add(data['stanceId'])
        except requests.RequestException as e:
            print(f"Error fetching data for departureId {departure_id}: {e}")
        except json.JSONDecodeError:
            print(f"Invalid JSON response for departureId {departure_id}")

    # Save stance IDs to a text file
    print(f"Saving {len(stance_ids)} unique stance IDs to {output_file}")
    with open(output_file, 'w') as file:
        file.write(",".join(map(str, sorted(stance_ids))))
    print("Stance IDs saved successfully.")

# Example usage
if __name__ == "__main__":
    # URL to fetch departure IDs
    departure_url = "https://raw.githubusercontent.com/fqrums/fqrums.github.io/refs/heads/main/legacyprojects/KGBus/departures.txt"

    # Base URL for fetching stance IDs
    base_url = "https://gas-kg.herokuapp.com/timetable/trips"

    # Output file
    output_file = "stance_ids.txt"

    # Step 1: Fetch departure IDs
    departure_ids = fetch_departure_ids(departure_url)

    if departure_ids:
        # Step 2: Fetch and save stance IDs
        fetch_stance_ids(departure_ids, base_url, output_file)
    else:
        print("No departure IDs found.")
