import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open WhatsApp Web
driver.get("https://web.whatsapp.com/")
input("Scan the QR Code with WhatsApp and then press Enter")

# Names of the groups
source_group = "טסט 1"
target_group = "Test"
last_message = None

# Function to find a chat by title
def find_chat_by_title(title: str) -> list:
    chats = driver.find_elements(By.XPATH, f"//span[@title='{title}']")
    if chats:
        return chats[0]
    else:
        return None
    
def check_format(message: str) -> bool:
    # Define the required fields
    required_fields = [
        "תאריך",
        "שם מלא",
        "מספר אישי",
        "דרגה",
        "יחידה",
        "מספר רכב",
        "סוג רכב",
        "מטרת כניסה"
    ]

    # Check each field
    for field in required_fields:
        # Use regular expression to search for the field in the message
        # re.IGNORECASE makes the search case-insensitive
        if not re.search(field, message, re.IGNORECASE):
            return False

    return True

def send_message_to_group(group_name: str, message: str) -> None:
    global last_message
    try:
        # Wait for the search box and find the group
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        search_box.clear()
        search_box.send_keys(group_name)
        search_box.send_keys(Keys.ENTER)

        # Wait for the message box to become active
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='10']"))
        )
        time.sleep(2)  # Allow time for the chat to open

        # Find the message box
        message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")

        # Split the message by newline and send each part
        # Use ActionChains to press SHIFT+ENTER for newline
        for part in message.split('\n'):
            ActionChains(driver).send_keys(part).perform()
            ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()

        # Remove the last newline
        ActionChains(driver).send_keys(Keys.BACK_SPACE).perform()

        # Send the message
        message_box.send_keys(Keys.ENTER)
        time.sleep(5)  # Wait for the message to be sent
        last_message = message
        print("Message sent successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Loop to keep checking for new messages
while True:
    source_chat = find_chat_by_title(source_group)
    if source_chat:
        source_chat.click()
        time.sleep(5)  # Increased wait time for messages to load

        # Retrieve all messages
        try:
            messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in') or contains(@class, 'message-out')]")

            if messages and len(messages) > 0:
                message = messages[-1].find_element(By.XPATH, ".//span[contains(@class, 'selectable-text')]").text

                if message != last_message and check_format(message):
                    send_message_to_group(target_group, message)

        except Exception as e:
            print(f"Error while getting messages: {e}")

    # Wait before checking for new messages again
    time.sleep(2)
