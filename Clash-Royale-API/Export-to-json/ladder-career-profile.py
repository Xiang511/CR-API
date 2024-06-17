import requests
import json
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

    # 天梯資料

    best = json.dumps(player_data.get("bestPathOfLegendSeasonResult"))
    last = json.dumps(player_data.get("lastPathOfLegendSeasonResult"))

    best2 = clean_result(best)
    last2 = clean_result(last)
     
    best2 = best2 if best2 != "null" else "10000"
    last2 = last2 if last2 != "null" else "10000"

    best3 = get_numbers_by_position_and_delete(keep_numbers(best), 2, 6)
    last3 = get_numbers_by_position_and_delete(keep_numbers(last), 2, 6)

    best3 = best3 if best3 else "0"
    last3 = last3 if last3 else "0"





    # 生涯資料

    win = player_data["wins"]
    losses =player_data["losses"]
    z=win/(win+losses)
    winrate = '{:%}'.format(z)

    rank = 10000 
    tr = json.dumps(player_data.get("leagueStatistics"))
    
    if tr  != "null":
        if 'bestSeason' in tr:
            bestSeason = eval(tr)["bestSeason"]
            if 'rank' in bestSeason:
                rank = bestSeason["rank"]
            else:
                rank="10000"
    else:
        rank="10000"
   

    battleCount = player_data.get("battleCount")
    threeCrownWins = player_data.get("threeCrownWins")
    totalDonations = player_data.get("totalDonations")
    tournamentBattleCount = player_data.get("tournamentBattleCount")

    YearsPlayedCout = 0
    EmoteCollectionCout = 0 
    BannerCollectionCout =0
    
    for YearsPlayed in player_data["badges"]:
       if YearsPlayed["name"] == "YearsPlayed":
        YearsPlayedCout = YearsPlayed["progress"]

    for EmoteCollection in player_data["badges"]:
       
       if EmoteCollection["name"] == "EmoteCollection":
        EmoteCollectionCout = EmoteCollection["progress"]

    for BannerCollection in player_data["badges"]:
       
       if BannerCollection["name"] == "BannerCollection":
        BannerCollectionCout = BannerCollection["progress"]




    # 個人成就資料

    Classic12WinsCout = 0
    Grand12WinsCout = 0
    starPoints = player_data.get("starPoints", 0)
    totalExpPoints = player_data.get("totalExpPoints", 0)

    for badge in player_data.get("badges", []):
        if badge["name"] == "Classic12Wins":
            Classic12WinsCout = badge["progress"]
        elif badge["name"] == "Grand12Wins":
            Grand12WinsCout = badge["progress"]

    return {
        "name": player_data.get("name", ""),
        "best2": best2,
        "best3": best3,
        "last2": last2,
        "last3": last3,
        "Classic12Wins": Classic12WinsCout,
        "Grand12Wins": Grand12WinsCout,
        "starPoints": starPoints,
        "totalExpPoints": totalExpPoints,     
        "rank":rank, 
        "battleCount":battleCount,
        "threeCrownWins":threeCrownWins,
        "totalDonations":totalDonations,
        "tournamentBattleCount":tournamentBattleCount,
        "winrate":winrate,
        "YearsPlayedCout":YearsPlayedCout,
        "EmoteCollectionCout":EmoteCollectionCout,
        "BannerCollectionCout":BannerCollectionCout,
    }

def clean_result(result):
    if result is None:
        return ""
    return result[result.rfind(" ") + 1:].split("}")[0]

def keep_numbers(string):
  
  filtered_string = filter(str.isdigit, string)
  return "".join(filtered_string)

def get_numbers_by_position_and_delete(variable, start_position, end_position):

  numbers = str(variable)[start_position:end_position]
  filtered_numbers = filter(str.isdigit, numbers)
  return "".join(filtered_numbers)

ladder_results = []

career_results = []

profile_results = []

def main():
    # Enter your API key
    api_key = ""

    # Enter player tags
    player_tags = ["%2322R920J00"]

    # Iterate over players and collect data
    for player_tag in tqdm(player_tags):
        combined_data = combine_player_data(player_tag, api_key)
        if combined_data:

            ladder = [
            "", 
            combined_data.get("name", "Unknown"),  # 使用 'Unknown' 當作預設值
            combined_data.get("best2", None),
            combined_data.get("best3", None),
            combined_data.get("last2", None),
            combined_data.get("last3", None)
            ]

            career = [
            "", 
            combined_data.get("name", "Unknown"),  # 使用 'Unknown' 當作預設值
            combined_data.get("rank", None),
            combined_data.get("battleCount", None),
            combined_data.get("threeCrownWins", None),
            combined_data.get("totalDonations", None),
            combined_data.get("tournamentBattleCount", None),
            ]

            profile = [
            "", 
            combined_data.get("name", "Unknown"),  # 使用 'Unknown' 當作預設值
            combined_data.get("Classic12Wins", None),
            combined_data.get("Grand12Wins", None),
            combined_data.get("YearsPlayedCout", None),
            combined_data.get("EmoteCollectionCout", None),
            combined_data.get("BannerCollectionCout", None),
            combined_data.get("starPoints", None),
            combined_data.get("totalExpPoints", None)
            ]

        ladder_results.append({"data": ladder})
        ladder_results_json = json.dumps(ladder_results)
        with open("player.json", "w") as file:
            file.write(ladder_results_json)

        career_results.append({"data": career})
        career_results_json = json.dumps(career_results)
        with open("career.json", "w") as file:
            file.write(career_results_json)

        profile_results.append({"data": profile})
        profile_results_json = json.dumps(profile_results)
        with open("profile.json", "w") as file:
            file.write(profile_results_json)

        # print(ladder_results_json)
        # print(career_results_json)
        # print(profile_results_json)


if __name__ == "__main__":
    main()
