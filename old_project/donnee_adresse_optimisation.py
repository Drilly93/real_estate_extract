import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException




def get_url_adresse(adresse,driver,wait):
    # Accéder à la page cible
    
    bouton = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/button[2]'))) #driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/button[2]')
    bouton.click()
    
    time.sleep(1)
    input_element = driver.find_element(By.XPATH, "//*[@id='rc_select_0']")
    input_element.send_keys(adresse)
    time.sleep(1)
    input_element.send_keys(Keys.RETURN)
    
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='rc_select_1']"))) #driver.find_element(By.XPATH, "//*[@id='rc_select_1']")
    dropdown.click()
    
    
    option = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='rc_select_1' and @aria-activedescendant = 'rc_select_1_list_0']"))) #driver.find_element(By.XPATH, "//*[@id='rc_select_1' and @aria-activedescendant = 'rc_select_1_list_0']")
    option.send_keys(Keys.RETURN)
    
    
    bouton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="input1"]/div[2]/button'))) #driver.find_element(By.XPATH, '//*[@id="input1"]/div[2]/button')
    bouton.click()
    
    
    button = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/main/div/div[1]/div[2]/button'))) #driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div[1]/div[2]/button')
    button.click()
    
    
    
    
def get_donnee_socio_economique(driver,wait):   
    bouton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="liveIn"]/div[8]/div/div[1]'))) #driver.find_element(By.XPATH, '//*[@id="liveIn"]/div[8]/div/div[1]')
    bouton.click() 
    
    liste = []
    time.sleep(1.5)
    elem = driver.find_element(By.XPATH, '//*[@id="liveIn"]/div[8]/div/div[2]')
    
    liste.append(elem.text)
    print(elem.text)
    
    return liste

def get_donnee_ecole(driver,wait):
    
    liste = []
    
    for i in range(1,6):
        if i == 1 :
            bouton = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="educ"]/div/div[1]/label['+str(i)+']'))) #driver.find_element(By.XPATH,'//*[@id="educ"]/div/div[1]/label['+str(i)+']') 
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bouton)
            bouton.click()
        else:
            bouton = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="educ"]/div/div[1]/label['+str(i)+']'))) #driver.find_element(By.XPATH,'//*[@id="educ"]/div/div[1]/label['+str(i)+']') 
            bouton.click()
            
        elem = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="educ"]/div/div[2]' ))) #driver.find_element(By.XPATH,'//*[@id="educ"]/div/div[2]')
        liste.append(elem.text)                   
    return liste



def get_donnee_securite(driver,wait):
    liste = []
    elem = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="liveIn"]/div[5]/div/div/div[1]/div/div'))) #driver.find_element(By.XPATH,'//*[@id="liveIn"]/div[5]/div/div/div[1]/div/div/strong')
    liste.append(elem.text)                   
    return liste

def get_donnee_mobilite(driver,wait):
    
    liste = []
    
    for i in range(1,10):
        
        try:
            if i == 1:
                bouton = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="liveIn"]/div[4]/div[1]/label['+str(i)+']'))) #driver.find_element(By.XPATH, '//*[@id="liveIn"]/div[4]/div[1]/label['+str(i)+']') 
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bouton)
                bouton.click()
            else:
                bouton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="liveIn"]/div[4]/div[1]/label['+str(i)+']'))) #driver.find_element(By.XPATH, '//*[@id="liveIn"]/div[4]/div[1]/label['+str(i)+']') 
                bouton.click()
                
            elem =  wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="liveIn"]/div[4]/div[2]'))) #driver.find_element(By.XPATH,'//*[@id="liveIn"]/div[4]/div[2]')
            liste.append(elem.text)    
    
        except TimeoutException or NoSuchElementException:      
            break
        
    
    return liste

def get_donnee_risque(driver,wait):

    liste = []
    
    #Polution
    elem = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/main/div[2]/div/div[2]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div[1]/div/span/span'))) #driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/div[2]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div[1]/div/span/span') 
    liste.append(elem.text)

    #Eau
    elem = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/main/div[2]/div/div[2]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div[2]/div/span/span'))) #driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/div[2]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div[2]/div/span/span') 
    liste.append(elem.text)


    #Autre
    
    for i in range(1,4):
        try:
            elem = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="rc-tabs-1-tab-'+str(i)+'"]/div/span[2]'))) #driver.find_element(By.XPATH,'//*[@id="rc-tabs-1-tab-'+str(i)+'"]/div/span[2]')
            elem_titre = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="rc-tabs-1-tab-'+str(i)+'"]/div/span[1]'))) #driver.find_element(By.XPATH,'//*[@id="rc-tabs-1-tab-'+str(i)+'"]/div/span[1]')
            liste.append(elem_titre.text+' '+ elem.text)                    
        except TimeoutException or NoSuchElementException:
            pass

    
    return liste

    

def traiter_donnee(l1):
    dico = {1:l1}
    return dico
    

def recup_url_adresse(adresse):
    try :
        chrome_options = Options()
        # Configuration de base
        #chrome_options.add_argument("--headless=new")  # Mode sans interface
        chrome_options.add_argument("--disable-gpu")  # Désactive l'accélération GPU
        chrome_options.add_argument("--no-sandbox")  # Nécessaire pour Docker/CI
        
        # Optimisation des performances
        chrome_options.add_argument("--disable-dev-shm-usage")  # Évite les crashs mémoire
        chrome_options.add_argument("--single-process")  # Mode mono-processus (Linux)
        chrome_options.add_argument("--window-size=1280x720")  # Taille de fenêtre fixe
        
        # Furtivité
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        #Attention a bien ecrire l'adresse
        # Configuration du service ChromeDriver
        
        driver = webdriver.Chrome(options = chrome_options) 
        wait = WebDriverWait(driver, 2)  
        wait_long = WebDriverWait(driver, 30) 
        
        
        # Accéder à la page cible
        url = "https://emplacement.immo/formulaire"
        driver.get(url) 
        
        
        get_url_adresse(adresse,driver,wait)
        
        bouton = wait_long.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/button[2]/div'))) #driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/button[2]/div') #QUARTIER
        bouton.click()
        
        
        liste_socio_economique = get_donnee_socio_economique(driver,wait)
        #liste_securite = get_donnee_securite(driver,wait)
        #liste_ecole = get_donnee_ecole(driver,wait)
        #liste_mobilite = get_donnee_mobilite(driver,wait)
        
        
        #bouton = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/main/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/button[3]'))) #driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/button[3]') #RISQUE
        #bouton.click()
        
        #liste_risque = get_donnee_risque(driver,wait)
        #driver.quit()
    except Exception as e:
        print(str(e))
        return None
    
    #dico = traiter_donnee(liste_socio_economique,
     #              liste_securite,
     #              liste_ecole,
     #              liste_mobilite,
     #              liste_risque) 
    #print(dico)
    
    driver.quit()
    dico = traiter_donnee(liste_socio_economique)
    return dico



adresses = [
"10 rue de la Paix Paris",
"5 avenue des Champs-Élysées Paris",
"8 rue Raoul Dufy Sarcelles",
"12 rue de Rivoli Paris",
"1 place de l'Opéra Paris",
"40 rue du Faubourg Saint-Antoine Paris",
"5 rue de la Liberté Lyon",
"25 boulevard de la République Marseille",
"2 rue Victor Hugo Lille",
"15 rue du Général Leclerc Toulouse"]

for i in adresses :
    recup_url_adresse(i)





