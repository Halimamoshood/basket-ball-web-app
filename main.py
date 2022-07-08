from flask import Flask
from waitress import serve

from basketball_app.services import get_games_stats

app = Flask(__name__)

new_no = 0

@app.route('/')
def get_games_stats_api():
    return get_games_stats()

@app.route('/nxt')
def games_stats_nxt_api(page_no = 1):
    global new_no
    new_no+=page_no

    return get_games_stats(new_no)

@app.route('/prv')
def games_stats_prv_api(page_no = 1):
    global new_no
    if new_no <= 1:
        new_no = 1
    else:
        new_no-=page_no

    return get_games_stats(new_no)

if __name__ == '__main__':
    # app.run(debug=True)
    serve(app)

