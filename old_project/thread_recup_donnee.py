from pathlib import Path
import os
CURRENT_FILE_PATH = Path(__file__).parent.resolve() #
os.chdir(CURRENT_FILE_PATH)



import donnee_adresse_optimisation
import concurrent.futures
import threading
import time

def thread_recup_donnee_adresse(adresse):
    dico = donnee_adresse_optimisation.recup_url_adresse(adresse)
    
    while dico is None:
        time.sleep(5)
        print("ERREUR")
        dico = donnee_adresse_optimisation.recup_url_adresse(adresse)
    
    return dico
        
    

def recup_adresses():
    adresses = [
    "10 rue de la Paix, 75002 Paris",
    "5 avenue des Champs-Élysées, 75008 Paris",
    "8 rue Raoul Dufy, 95200 Sarcelles",
    "12 rue de Rivoli, 75001 Paris",
    "1 place de l'Opéra, 75009 Paris",
    "40 rue du Faubourg Saint-Antoine, 75012 Paris",
    "5 rue de la Liberté, 69003 Lyon",
    "25 rue de la République, 13001 Marseille",
    "2 rue Victor Hugo, 59800 Lille",
    "15 rue du Général Leclerc, 31000 Toulouse"]
    return adresses

max_threads = 4
adresses = recup_adresses()
resultats = []

with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    # Code à exécuter avec l'exécuteur
    futures = [executor.submit(thread_recup_donnee_adresse, adresse) for adresse in adresses]
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        resultats.append(result)




