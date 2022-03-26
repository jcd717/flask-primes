from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

import os

#from werkzeug.exceptions import abort

import socket




bp = Blueprint('primes', __name__)


def isPrime(n,primes):
    """
    Retourne: 
      1) si 'n' est premier  
      2) la nouvelle valeur éventuelle de la liste 'primes' qui contient les premiers <'n' 
    """
    if n==1:
        return False, primes
    for p in primes:
        if n % p ==0:
            return False, primes
    primes.append(n)
    return True,primes


@bp.route('/')
def index():
    if not session.get('compteur'): # 1ère connexion: la session n'existe pas encore
        session['compteur']=0
        session['primes']=list()
    session['compteur'] += 1
    g.isPrime, session['primes'] = isPrime(session['compteur'],session['primes'])

    g.hostname = socket.gethostname()
    if os.environ.get('NO_IP'):
        g.IP='127.0.0.1'
    else:
        try:
            # plante dans swarm et probablement d'autres orchestrator
            g.IP = socket.gethostbyname(g.hostname)
        except:
            g.IP='127.0.0.1' # c'est pas faux

    def pluriel():
        return '' if len(session['primes'])<2 else 's'
    
    g.source='index'

    return render_template('primes.j2',pluriel=pluriel)


@bp.route('/informations')
def infos():
    g.source='infos'

    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../README.md')
    with open(filename) as f:
        g.md=f.read()
    
    return render_template('infos.j2')
