from flask import (
    Blueprint, g, redirect, render_template, session, url_for
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


def updateSession():
    """
    Met à jour la liste session['primes'] & session['compteur']
    et retoune un dict contenant:
    'isPrime': boolean pour dire si la nouvelle valeur du compteur est un nombre premier
    'hostname': le hostname
    'IP': l'IP du hostname
    """
    if not session.get('compteur'): # 1ère connexion: la session n'existe pas encore
        session['compteur']=0
        session['primes']=list()
    session['compteur'] += 1
    resultIsPrime, session['primes'] = isPrime(session['compteur'],session['primes'])
    hostname = socket.gethostname()
    if os.environ.get('NO_IP'):
        IP='127.0.0.1'
    else:
        try:
            # plante dans swarm et probablement d'autres orchestrator
            IP = socket.gethostbyname(hostname)
        except:
            IP='127.0.0.1' # c'est pas faux
    return {
        'isPrime': resultIsPrime,
        'hostname': hostname,
        'IP': IP
    }

@bp.route('/')
def index():
    def pluriel():
        return '' if len(session['primes'])<2 else 's'
    
    g.source='index'
    next=updateSession()
    g.isPrime=next['isPrime']
    g.hostname=next['hostname']
    g.IP=next['IP']

    return render_template('primes.j2',pluriel=pluriel)


@bp.route('/reset')
def resetCounter():
    session['compteur']=0
    session['primes']=list()
    return redirect(url_for('primes.index'))


@bp.route('/informations')
def infos():
    g.source='infos'

    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../README.md')
    with open(filename) as f:
        g.md=f.read()
    
    return render_template('infos.j2')


@bp.route('/api/allAndNext')
def allAndNext():
    next=updateSession()
    next.update({'listPrimes':session['primes'],'counter':session['compteur']})
    return next


@bp.route('/api/next')
def next():
    next=updateSession()
    next.update({'counter':session['compteur']})
    return next
