import time
import re
import os
from datetime import date
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chats import *
from utils.logger import *
import logging

def setup_selenium():
    load_dotenv()
    DRIVER_PATH = os.getenv("DRIVER_PATH")
    CHROME_PROFILE = os.getenv("CHROME_PROFILE")

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={CHROME_PROFILE}")
    # options.add_argument("--headless=new")          # run without opening browser window
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    # driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com/")
    return driver

def wait_for_whatsapp_loaded(driver, timeout=600):
    logging.info("Waiting for WhatsApp to load...")
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "pane-side"))
    )
    print("WhatsApp is ready!")


def search_and_open_chat(driver, chat_name):
    print(f"Searching for chat: {chat_name}")

    # Locate the search box (search tab 3)
    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        )
    )

    # Click to focus and fully clear (React-safe)
    search_box.click()
    search_box.send_keys(Keys.CONTROL + "a")
    search_box.send_keys(Keys.BACKSPACE)
    time.sleep(1)

    # Type the new chat name
    search_box.send_keys(chat_name)
    time.sleep(2)  # Wait for search results to load

    # Press Enter to open the first result
    search_box.send_keys(Keys.ENTER)
    print(f"Opened chat: {chat_name}")
    time.sleep(3)



def scrape_recent_messages(driver, limit=20):
    print("Scraping recent messages...")

    # Find all message bubbles (incoming & outgoing)
    bubbles = driver.find_elements(
        By.XPATH, "//div[contains(@class,'message-in')]"
    )
    
    if not bubbles:
        raise RuntimeError("No messages found — chat may not have loaded yet.")
    results = []
    for msg in bubbles[-limit:]:
        sender = "You" if "message-out" in msg.get_attribute("class") else "Contact"

        # Try all possible selectors for text
        message_text = msg.text
        try :
            meta_div = msg.find_element(By.XPATH, ".//div[contains(@class, 'copyable-text')]")
        except : 
            continue
        date_raw = meta_div.get_attribute("data-pre-plain-text")


        # Extract time (new DOM uses <span data-testid='msg-meta'>)
        match = re.search(r"\b(\d{1,2}/\d{1,2}/\d{4})\b", date_raw)
        if match:
            date = match.group(1)
            date = date.replace("/", "-")
        else : 
            date = None

        results.append(
            {"time": date, "message": message_text}
        )
    return results

def save_chat_results(base_dir, chat_name, chat_data_dicts):
    """
    Save a single chat's messages (list of dicts) to a JSON file named with today's date.
    
    Args:
        base_dir (str): Base folder to hold all chat subfolders.
        chat_name (str): Chat name (folder will be named after it).
        chat_data_dicts (list[dict]): List of messages (each message is a dict).
    """
    today_str = date.today().strftime("%Y-%m-%d")
    # Sanitize chat folder name (remove invalid filesystem characters)
    safe_chat_name = chat_name.replace(" ","_")
    chat_folder = os.path.join(base_dir, safe_chat_name)
    # Create folder if not exists
    os.makedirs(chat_folder, exist_ok=True)

    # Create JSON file with today's date
    json_path = os.path.join(chat_folder, f"{today_str}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(chat_data_dicts, f, ensure_ascii=False, indent=2)


@timing
def main_scraping(search_chats = None) :
    if not search_chats :
        search_chats = chats
        
    result = []

    try : 
        driver = setup_selenium()
        wait_for_whatsapp_loaded(driver)
        for chat in chats :
            search_and_open_chat(driver, chat)
            messages = scrape_recent_messages(driver, limit=20)
            result.append(messages)
            save_chat_results("data\exported_chats", chat, messages)
    finally:
        # driver.quit()
        None
    return result
