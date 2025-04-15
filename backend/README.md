## Dépendances
- Python
- Podman (ou Docker - si vous utilisez Docker, remplacez `podman` par `docker` dans toutes les commandes ci-dessous)

# Premier lancement

## Serveur web Python

Setup :
```bash
python3 -m venv ./.venv          # environnement virtuel
source ./.venv/bin/activate      # activer l'environnement virtuel
pip install -r requirements.txt  # installer les dépendances
```

Lancer le serveur :
```bash
python3 ./src/server.py --graphdb "http://localhost:7200" 
```
Il est possible d'utiliser `--fake-api` pour simuler une fausse connexion à GraphDB.
Ou encore spécifier l'adresse et le port sur lequel tourne le serveur python avec `--host` et `--port`.
Pour plus d'informations :
```bash
python3 ./src/server.py --help
```

## Serveur GraphDB

Créer les volumes pour stocker les données :
```bash
podman volume create graphdb-data
podman volume create graphdb-import
```

Lancer le serveur :
```bash
podman run -it -p 7200:7200 \
  --name dhfc-graphdb \
  -v graphdb-data:/opt/graphdb/home \
  -v graphdb-import:/root/graphdb-import \
  -v ./graphdb.license:/opt/graphdb/home/conf/graphdb.license \
  docker.io/ontotext/graphdb:11.0.0
```

# Relancer après arrêt

## Serveur web Python
```bash
source ./.venv/bin/activate
python3 ./src/server.py
```

## Serveur GraphDB
Redémarrer le serveur (ajoutez `-a` pour y attacher le shell) :
```bash
podman start dhfc-graphdb
```

# Informations supplémentaires

Accès à l'interface web de GraphDB par :
```
http://localhost:7200
```

## Commandes supplémentaires

Ouvrir l'accès à un shell bash si besoin :
```bash
podman exec -it dhfc-graphdb bash
```

Attacher le shell au conteneur :
```bash
podman attach dhfc-graphdb
```

Pour les autres commandes, voir la documentation :
```bash
man podman
```