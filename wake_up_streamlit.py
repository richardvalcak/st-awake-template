from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import datetime
import time

# Tvoje appky – sem je dej
STREAMLIT_APPS = [
    "https://ubytovani.streamlit.app",
    "https://kniha-tyrsova-znojmo.streamlit.app"
]

# Nastavení Chrome pro GitHub Actions (2026 realita)
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36')

def wake_app(url):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}] Zkouším: {url}")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(60)
        
        driver.get(url)
        
        # Počkáme na načtení stránky
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Hledáme tlačítko probuzení (text se v 2026 nemění často)
        xpath = "//button[contains(., 'Yes, get this app back up') or contains(., 'get this app back up') or contains(., 'wake it back up')]"
        
        try:
            button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            button.click()
            print(f"   → Kliknuto na probuzení!")
            time.sleep(10)          # počkáme na start appky
            print(f"   → Hotovo (pravděpodobně probuzeno)")
            
        except TimeoutException:
            print("   → Tlačítko nenalezeno → app už běží")
            
    except WebDriverException as e:
        print(f"   → Problém s prohlížečem: {str(e)}")
    except Exception as e:
        print(f"   → Jiná chyba: {str(e)}")
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    print("=== Start keep-alive job ===")
    for url in STREAMLIT_APPS:
        wake_app(url)
        time.sleep(5)           # malá pauza mezi appkami
    print("=== Job dokončen ===")
