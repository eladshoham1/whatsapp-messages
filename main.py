from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open WhatsApp Web
driver.get("https://web.whatsapp.com/")
input("Scan the QR Code with WhatsApp and then press Enter")

# Function to send a message to a group
def send_message_to_group(group_name, message):
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

        # Find the message box and type the message
        message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
        message_box.send_keys(message)
        time.sleep(2)  # Allow time for the message to be typed

        # Send the message
        message_box.send_keys(Keys.ENTER)

        time.sleep(5)  # Wait for the message to be sent
        print("Message sent successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'YOUR_GROUP_NAME' with the name of your WhatsApp group
group_title = 'טסט 1'

try:

    while True:
        # Locate the group
        group = driver.find_element(By.XPATH, f"//span[@title='{group_title}']")
        group.click()
        
        # Find all messages in the group
        messages = driver.find_elements(By.CLASS_NAME, 'message-in')

        if messages:
            last_message = messages[-1].find_element(By.CSS_SELECTOR, 'span.selectable-text').text
            print(last_message)

        # Wait for a bit before checking for new messages
        time.sleep(1)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()

# group_name = "טסט 1"
# while True:
#     last_messages = get_last_messages(driver, group_name)
    
#     # Print the messages
#     for msg in last_messages:
#         print(msg)
#     time.sleep(2)

# Example usage
# group_name = "Test"
# message = "Hello, this is a test message from Python!"
# send_message_to_group(group_name, message)

