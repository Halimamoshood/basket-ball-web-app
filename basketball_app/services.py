
import json
import os
import threading
import urllib.request

import matplotlib
import matplotlib.pyplot as plot
import pandas
from flask import render_template

matplotlib.use('Agg')


def gen_barchart(dataframe):

    # api_url = f'https://www.balldontlie.io/api/v1/games/?page={page_no}'
    # res = urllib.request.urlopen(api_url)
    # data = res.read()
    # json_data = json.loads(data)
    # dataframe = pandas.DataFrame(json_data['data'])

    home_team_score = []
    home_team = []

    for i in dataframe['home_team_score']:
        home_team_score.append(i)
        # print(i)

    for i in dataframe['home_team']:
        home_team.append(i['abbreviation'])
        # print(i['abbreviation'])

    plot.figure(figsize=(10, 10))

    # plot.bar(home_team_score, home_team)
    plot.bar(home_team, home_team_score)

    plot.xlabel('Home Team')
    plot.ylabel('Home Team Score')

    
    plot.savefig(f'static/img/chart.png')

    home_team_score.clear()
    home_team.clear()
# gen_barchart(6)

def get_games_stats(page_no = 1):

    api_url = f'https://www.balldontlie.io/api/v1/games/?page={page_no}'
    res = urllib.request.urlopen(api_url)
    data = res.read()
    json_data = json.loads(data)
    dataframe = pandas.DataFrame(json_data['data'])


    image_path = os.path.exists('static/img/chart.png')

    if image_path == True:
        os.remove('static/img/chart.png')
    # # #####################

    barchart_thread = threading.Thread(target=gen_barchart(dataframe))
    barchart_thread.start()
    # barchart_thread.join()

    # # ############################

    tot_no_home_team_score = dataframe['home_team_score'].sum()
    tot_no_visitor_team_score = dataframe['visitor_team_score'].sum()
    team_score_diff = tot_no_home_team_score - tot_no_visitor_team_score
    mean_home_team_score = tot_no_home_team_score/len(dataframe['home_team_score'].index)
    mean_visitor_team_score = tot_no_visitor_team_score/len(dataframe['visitor_team_score'].index)

    result = {'Total Home Team Scores':tot_no_home_team_score, 'Total Visitor Team Scores':tot_no_visitor_team_score, 'Teams Scores Difference':team_score_diff, 'Mean for Home Teams Scores':mean_home_team_score, 'Mean for Visitor Teams Scores':mean_visitor_team_score}

    return render_template('index.html', games=result)
