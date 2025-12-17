# Real Estate Data Acquisition & Price Prediction (Pipeline)



## Setup

### 2) Install dependencies
pip install -r requirements.txt

### Execution Order

#### Setup :
Open config.py and:
- Set all local paths (data folders, output files),
- Configure the OSM .pbf file path (light / medium / full),
- Make sure your system username is declared in the configuration.

## Execution Order

Each script is executed sequentially to progressively enrich and clean the real estate dataset.

>>> python telechargement_valeur_fonciere.py  
Downloads DVF transaction data (by department) and performs an initial cleaning step, producing the base DVF dataset.

>>> python traitement_open_street_map.py  
Adds geographic features from OpenStreetMap (points of interest, distances) to the DVF transactions.

>>> python fusion_vf_eco_insee.py  
Merges DVF and OSM data with socio-economic indicators from INSEE and other economic datasets.

>>> python fin_nettoyage.py  
Performs final data cleaning, handles missing values and outliers, and prepares the dataset for machine learning.

>>> python donnee_adresse_optimisation.py  
Extracts additional indicators from an external website using Selenium for a given address.

>>> python thread_recup_donnee.py  
Runs the Selenium-based address extraction in parallel to speed up data collection.

## Explanation 

**config.py** : Fichier central de configuration contenant les chemins, constantes et emplacements des fichiers d’entrée/sortie utilisés par l’ensemble du projet.  

**telechargement_valeur_fonciere.py** : Télécharge les données de transactions DVF (par département) et réalise un premier nettoyage/prétraitement des données.  
**Output** : fichiers CSV/Parquet contenant les transactions DVF nettoyées (par exemple `ValeursFoncieresFrance.csv`, `ValeursFoncieresFrance.parquet` et/ou `df_vf.parquet` selon la configuration dans `config.py`).

**traitement_open_street_map.py** : Traite un fichier OpenStreetMap `.pbf` afin de construire des variables géographiques (comptage de points d’intérêt, distances minimales) et d’enrichir les transactions DVF avec ces informations.  
**Output** : dataset enrichi au format Parquet (généralement `df_vf_osm.parquet`).

**fusion_vf_eco_insee.py** : Fusionne les données DVF + OSM avec les indicateurs socio-économiques de l’INSEE (niveau commune/département) ainsi que des variables économiques temporelles optionnelles.  
**Output** : dataset fusionné au format Parquet (généralement `df_vf_osm_eco_insee.parquet` ou un nom équivalent défini dans `config.py`).

**fin_nettoyage.py** : Effectue le nettoyage final et la préparation pour le machine learning (gestion des valeurs manquantes, suppression des outliers, transformations et encodages).  
**Output** : dataset final prêt pour le ML au format Parquet (généralement `data_set.parquet`).

**donnee_adresse_optimisation.py** : Utilise Selenium pour interroger un site externe à partir d’une adresse et extraire des indicateurs supplémentaires (enrichissement par adresse).  
**Output** : fichiers structurés (CSV/Parquet ou fichiers intermédiaires JSON/CSV) selon les modalités d’export définies dans le script ou la configuration.

**thread_recup_donnee.py** : Exécute l’extraction Selenium par adresses en parallèle (ThreadPool) afin d’accélérer la collecte sur un grand nombre d’adresses.  
**Output** : mêmes formats de sortie que `donnee_adresse_optimisation.py` (CSV/Parquet/JSON), mais générés plus rapidement pour un ensemble d’adresses.



## SOURCES & REFERENCES

Valeurs Foncières (DVF) :
- Data Gouv : "https://dvf-api.data.gouv.fr/dvf/csv/?dep="

OpenStreetMap (OSM) :
- Open Street Map "https://download.geofabrik.de/europe/france.html"