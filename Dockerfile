# image tag: site-primes:python3.7.8-alpine
# donc:
# docker build -t site-primes:python3.7.8-alpine .

# Si la variable d'environnement REDIS est positionné avec comme valeur ADDRESS:PORT, 
# alors ce serveur est utilisé pour les sessions
# Rappel: le port classique de Redis est: 6379

FROM python:3.7.8-alpine

EXPOSE 5000
ENV FLASK_APP=primes

WORKDIR /app

# le moteur flask
COPY README.md pip-packages.txt /app/
RUN pip install -r pip-packages.txt

# la variable d’environnement SECRET_KEY injecté de manière "sécurisé" (jusqu'à preuve du contraire)
# si l'image est sur Docker Hub, tout le monde voit la clef dans l'image
# Donc pour une prod, il faut toujours construire soit même cette image

RUN \
mkdir instance 2>/dev/null && \
echo SECRET_KEY=\"$(python -c "import string,random; print(''.join(random.choice(string.ascii_letters+string.digits+'-_:./+%£') for i in range(32)))")\" >instance/config.py

# gunicorn
ENV \
  WORKERS=1 \
  ACCESS_LOG_FORMAT='client="%(h)s" forwarder="%({x-forwarded-for}i)s" user="%(u)s" %(t)s "%(r)s" %(s)s len="%(b)s" "%(f)s" "%(a)s" %(L)ss'
SHELL [ "/bin/sh","-c" ]
CMD gunicorn "primes:create_app()" --workers ${WORKERS} --bind "0.0.0.0:5000" --access-logfile - --access-logformat "${ACCESS_LOG_FORMAT}"

# le code source
COPY . /app/
