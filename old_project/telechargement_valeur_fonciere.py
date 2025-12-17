import matplotlib.pyplot as plt
import pandas as pd
import polars as pl
import wget
import os


from pathlib import Path
CURRENT_FILE_PATH = Path(__file__).parent.resolve()
os.chdir(CURRENT_FILE_PATH)


from config import PATH_FICHIER_DEP_FR ,PATH_FICHIER_VAL_FONCIERE_FRANCE_CSV # FICHIER
from config import PATH_DIR_VAL_FONCIERE_DEP, PATH_DIR_VAL_FONCIERE_FRANCE # Directory/Dossier
from config import URL_VAL_FONCIERE, TYPE_COLUMN_CSV_SALE, COLUMN_FINAL, TYPE_COLUMN_CSV_PROPRE # Constante Utile
from config import PATH_FICHIER_VAL_FONCIERE_FRANCE_PARQUET, PATH_FICHIER_DF_VF



df_departement = pd.read_csv(PATH_FICHIER_DEP_FR)
df_departement = df_departement[["code_departement","nom_departement"]]


def telechargement_valeur_fronciere_departement():
    
    # Boucle sur tous les départements listes dans le fichier df_departement
    for i in range(len(df_departement["code_departement"])):  
        print(df_departement.iloc[i,0])
        # Cree un dossier par departement
        os.makedirs(PATH_DIR_VAL_FONCIERE_DEP / df_departement.iloc[i,0], exist_ok = True)
        
        # Definit le chemin de destination pour le fichier CSV du departement
        chemin_fichier = os.path.join(PATH_DIR_VAL_FONCIERE_DEP / df_departement.iloc[i,0] / (df_departement.iloc[i,0] + ".csv"))
        
        # Telecharge le fichier CSV depuis l'URL publique et le sauvegarde dans le chemin que l'on a defini
        wget.download(URL_VAL_FONCIERE + df_departement.iloc[i,0],chemin_fichier)
     
    def premier_nettoyage_donnee():
    
    
    print("NETTOYAGE VALEUR FONCIERE EN COURS")
    
    #On utilise polars car avec pandas on a des out of memory avec un ordinateur classique
    liste_data_frame = []
    for i in range(len(df_departement["code_departement"])):
            
        try :
            df = pl.read_csv(PATH_DIR_VAL_FONCIERE_DEP / df_departement.iloc[i,0] / (df_departement.iloc[i,0] + '.csv'), schema_overrides = TYPE_COLUMN_CSV_SALE)
        except pl.exceptions.NoDataError:
            print("Fichier",df_departement.iloc[i,0],".csv est vide. Auncune donnee pour Departement  : ",df_departement.iloc[i,1])
            continue
        
        
        #----------NETTOYAGE----------
        
        #Selectionne les features interessantes
        df = df.select(COLUMN_FINAL)
        
        
        #On garde que les ventes 
        df = df.filter(pl.col("nature_mutation").is_in(["Vente", 
                                                        "Vente en l'état futur d'achèvement", 
                                                        "Vente terrain à bâtir"]))
        
        # On s'interesse au maison et au appart
        df= df.filter(pl.col("type_local").fill_null("").is_in(["Appartement","Maison"]))
        
        #Supprime les valeurs nulles (Beaucoup de donnee donc oklm)
        df = df.filter(pl.col("valeur_fonciere").is_not_null()) 
        df = df.filter(pl.col("latitude").is_not_null() & pl.col("longitude").is_not_null())
        
        # ATTENTION CES LIGNES en dessous NE DOIVENT PAS ETRE EXECUTE !
        # SURFACE TERRAIN a NULL pour les APPART. 
        # On perd une grande parti des donnee des APPART si on enleve ligne surface terrain == NULL
        
        #df = df.filter(pl.col("surface_reelle_bati").is_not_null())
        #df = df.filter(pl.col("surface_terrain").is_not_null())
        
        
        # DEF  surface_reelle_bati = surface habitable
        #      surface_terrain = surface habitable plus jardin ou autre
        # SOLUTION TROUVEE : on met a zero si NULL (ou plutot 0.000001, on divisera pour avoir prix au metre carre....)
        
        #Changement de type et valeur null mis a zero.
        #Valable de faire si different [^0-9.] alors mettre a 0 ....Nous reste que valeur null ou des chiffres...
        df = df.with_columns([pl.col("surface_reelle_bati").str.replace_all(r"[^0-9.]", "0.00001").cast(pl.Float64),
                             pl.col("surface_terrain").str.replace_all(r"[^0-9.]", "0.00001").cast(pl.Float64),
                             pl.col("valeur_fonciere").str.replace_all(r"[^0-9.]", "0").cast(pl.Float64),
                             pl.col("date_mutation").str.strptime(pl.Date, "%Y-%m-%d")])

        
        
        #Rajout d'une colonne annee_mois,  Format YYYY-MM (année-mois) utile pour les plots
        df = df.with_columns([pl.col("date_mutation").dt.strftime("%Y-%m").alias("annee_mois"),
                             pl.col("date_mutation").dt.year().alias("annee")]) # Ajoute la colonne année
        
        
        # Valeur Aberantes ?
        #On traitera sa separemment. Pas encore assez de recul.
        #df = df.filter((pl.col("surface_terrain") > 5) & (pl.col("valeur_fonciere") > 100))
        
       
        # Calcul prix metre carre
        df = df.with_columns([(pl.col("valeur_fonciere") / pl.col("surface_reelle_bati")).alias("prix_par_m2_habitable"),
                             (pl.col("valeur_fonciere") / pl.col("surface_terrain")).alias("prix_par_m2_terrain")])
    
        #Supprime les doublons si existant
        df = df.unique(subset=['date_mutation','longitude', 'latitude', 'valeur_fonciere', 'surface_terrain'])
        
        liste_data_frame.append(df.clone())
        
        
    merged_df = pl.concat(liste_data_frame)
    
    # Sauvegarder dans un fichier CSV
    merged_df.write_csv(PATH_FICHIER_VAL_FONCIERE_FRANCE_CSV)
    print("Sauvegarde CSV OK")
    merged_df.write_parquet(PATH_FICHIER_VAL_FONCIERE_FRANCE_PARQUET)
    merged_df.write_parquet(PATH_FICHIER_DF_VF)
    print("Sauvegarde PARQUET OK")
    
    
    
    print("------BILAN-----")
    print("Nombre de Donnee apres netoyyage",merged_df.shape[0])
    print("Nombre de Donnee Maison",merged_df.filter(pl.col("type_local") == "Maison").shape[0])
    print("Nombre de Donnee Appart",merged_df.filter(pl.col("type_local") == "Appartement").shape[0])
    print(df.select(['valeur_fonciere','prix_par_m2_habitable','prix_par_m2_terrain']).describe())





#ATTENTION NE PLUS TOUCHE, NE PAS RUN nettoyage_donnee(), on obtient des ordres de lignes differents pour deux runs differents

if __name__ == "__main__":
    telechargement_valeur_fronciere_departement()
    # premier_nettoyage_donnee()
    print()