from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json
import logging
from dotenv import load_dotenv # NOUVEAU : Importe la fonction pour charger les variables d'environnement

load_dotenv() # NOUVEAU : Charge les variables d'environnement du fichier .env

# Récupère les options de vote depuis les variables d'environnement
option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

def get_redis():
    if not hasattr(g, 'redis'):
        # NOUVEAU : Récupère l'hôte Redis depuis les variables d'environnement
        redis_host = os.getenv('REDIS_HOST', 'redis')
        g.redis = Redis(host=redis_host, db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        app.logger.info('Received vote for %s', vote)
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp


if __name__ == "__main__":
    # NOUVEAU : Récupère le port Flask depuis les variables d'environnement
    flask_port = int(os.getenv('PORT_FLASK', 80))
    app.run(host='0.0.0.0', port=flask_port, debug=True, threaded=True)
