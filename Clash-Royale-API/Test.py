import openpyxl
import requests
import json
import time
from tqdm import tqdm

def combine_player_data(player_tag, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(f"https://api.clashroyale.com/v1/players/{player_tag}", headers=headers)
        player_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data for player tag {player_tag}: {e}")
        return None

    # Extract data from player_data
    best = clean_result(json.dumps(player_data.get("bestPathOfLegendSeasonResult")))
    last = clean_result(json.dumps(player_data.get("lastPathOfLegendSeasonResult")))

    Classic12WinsCout = 0
    Grand12WinsCout = 0
    starPoints = player_data.get("starPoints", 0)
    totalExpPoints = player_data.get("totalExpPoints", 0)

    for badge in player_data.get("badges", []):
        if badge["name"] == "Classic12Wins":
            Classic12WinsCout = badge["progress"]
        elif badge["name"] == "Grand12Wins":
            Grand12WinsCout = badge["progress"]
        # Process other badges as needed

    return {
        "name": player_data.get("name", ""),
        "best": best,
        "last": last,
        "Classic12Wins": Classic12WinsCout,
        "Grand12Wins": Grand12WinsCout,
        "starPoints": starPoints,
        "totalExpPoints": totalExpPoints
    }

def clean_result(result):
    if not result:
        return ""
    return result[result.rfind(" ") + 1:].split("}")[0]

def main():
    # Enter your API key
    api_key = ""

    # Enter player tags
    player_tags = ["%2322R920J00", "%23V99082R9C"]

    # Calculate starting time
    start_time = time.time()

    # Create workbooks and worksheets
    wb1 = openpyxl.Workbook()
    ws1 = wb1.active

    ws1["A1"] = "Tag"
    ws1["B1"] = "BEST"
    ws1["C1"] = "LAST"

    wb2 = openpyxl.Workbook()
    ws2 = wb2.active

    ws2["A1"] = "Tag"
    ws2["B1"] = "Classic12Wins"
    ws2["C1"] = "Grand12Wins"
    ws2["D1"] = "YearsPlayed"  # Assuming you added YearsPlayed badge
    ws2["E1"] = "EmoteCollection"
    ws2["F1"] = "BannerCollection"
    ws2["G1"] = "starPoints"
    ws2["H1"] = "totalExpPoints"

    # Iterate over players and collect data
    for player_tag in tqdm(player_tags):
        combined_data = combine_player_data(player_tag, api_key)
        if combined_data:
            ws1.append([combined_data["name"], combined_data["best"], combined_data["last"]])
            ws2.append([combined_data["name"],
                        combined_data["Classic12Wins"],
                        combined_data["Grand12Wins"],
                        combined_data.get("YearsPlayed", 0),  # Handle missing badge
                        combined_data.get("EmoteCollection", 0),  # Handle missing badge
                        combined_data.get("BannerCollection", 0),  # Handle missing badge
                        combined_data["starPoints"],
                        combined_data["totalExpPoints"]])

    # Save workbooks
    wb1.save("Player.xlsx")
    wb2.save("PlayerProfile.xlsx")

    # Calculate end time
    end_time = time.time()
    print(f"Time：{end_time - start_time}")

if __name__ == "__main__":
    main()
