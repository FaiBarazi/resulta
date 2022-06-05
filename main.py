import os
import asyncio
from aiohttp import ClientSession
from dotenv import load_dotenv

# Load environemnt variables from .env file.
load_dotenv()

# Not the best way to
API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://delivery.chalk247.com'


# chalk247 does not allow to query a time interval bigger than 7 days.
# This ensures somewhat that the data size is controllable.
async def get_scoreboard(session: ClientSession, league: str, start_date: str, end_date: str):
    url = f'{BASE_URL}/scoreboard/{league}/{start_date}/{end_date}.json?api_key={API_KEY}'
    async with session.get(url) as response:
        result = await response.json()
        result = result['results']
    return result


async def get_teams_ranking(session: ClientSession, league: str, start_date: str, end_date: str):

    url = f'{BASE_URL}/team_rankings/{league}.json?api_key={API_KEY}'
    async with session.get(url) as response:
        resp_dict = await response.json()
        resp_dict = resp_dict['results']
    # Transform the data for easy look up based on the team id to avoid looping.
    data = {team['team_id']: team for team in resp_dict.get('data', [])}
    return data


async def fetch_data(league: str, start_date: str, end_date: str):
    responses = []
    async with ClientSession() as session:
        tasks = [
            get_scoreboard(session, league, start_date, end_date),
            get_teams_ranking(session, league, start_date, end_date)
        ]
        # Although the tasks are run asyncronosly, as_completed pereserves the order of the tasks.
        for task in asyncio.as_completed(tasks):
            resp = await task
            responses.append(resp)
    return responses


def transform_data(scoreboard_items, teams_ranking):
    result = []
    print(scoreboard_items)
    if not scoreboard_items:
        return result

    scoreboard = scoreboard_items.get('data', [])
    scoreboard_keys = [
            'event_id', 'away_team_id', 'away_nick_name',
            'away_city', 'home_team_id',
            'home_nick_name', 'home_city'
    ]

    for item in scoreboard:
        # Map standard keys
        data = {
            scoreboard_key: scoreboard[item][scoreboard_key] for scoreboard_key in scoreboard_keys
        }

        # Map time and date
        data['event_date'], data['event_time'] = scoreboard[item]['event_date'].split()

        # Map away rank
        away_team_data = teams_ranking[data['away_team_id']]
        data['away_rank'] = away_team_data['rank']
        data['away_rank_points'] = round(
            float(away_team_data['points']), 2
        )
        # Map home rank
        home_team_data = teams_ranking[data['home_team_id']]
        data['home_rank'] = home_team_data['rank']
        data['home_rank_points'] = round(
            float(home_team_data['points']), 2
        )
        result.append(data)
    return result


def run_main(league, start_date, end_date):
    results = []
    scorebaord, teams_ranking = asyncio.run(fetch_data(league, start_date, end_date))
    for event_date in scorebaord.keys():
        result = transform_data(scorebaord[event_date], teams_ranking)
        results += result
    return results
