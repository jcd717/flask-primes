Simulation d'activité humaine
=============================

Ce site à page unique permet d'être utilisé avec des outils de stress (mais aussi en manuel).

Affichage
---------

La page affiche le *hostname* de l'hôte sur lequel elle s'exécute, ainsi que son adresse *IP*.

Ceci est uile quand ce site est installé en mode "ferme".

* Concernant l'adresse IP:  
Le code fait ce qu'il peut. Lorsque l'hôte a plusieurs adresses, que l'environnement est de type "container+orchestrator", ou tout autre environnemt où l'IP est incertaine, l'API utilisé: `IP = socket.gethostbyname(socket.gethostname())` ne retourne pas forcément la bonne IP (voir échoue, c'est le cas dans *docker swarm*).

Puis elle affiche le compteur de *refresh* de la page, et la liste des nombre premiers inférieurs ou égal à ce compteur.

Le compteur et la liste sont stockés dans la session web côté serveur.

C'est ainsi qu'on peut simuler **une activité humaine**.

En effet, la liste suit une progression logarithmique, ce qui correspond au fait que, plus un humain avance dans sa journée, moins il consomme de RAM. De plus un outil de stress qui boucle sur cette page pourra faire *stresser* le CPU lors du test de primalité (à partir d'une valeur du compteur assez élevée).

Variables d'environnement
-------------------------

Elles sont deux:

* `FLASK_APP=primes` puisqu'il s'agit d'une application *flask*. Il faut la positionner si votre serveur en a besoin (c'est le cas de *werkzeug* qui est embarqué dans *flask*)

* `REDIS`: Si cette variable a une valeur du type: `IP[:port]` alors les sessions seront stockées dans ce service, si cette varible n'existe pas, elles seront stockés dans le système de fichiers.


