import time
import requests
from settings import token

api_url = f"https://api.telegram.org/bot{token}/"

def send_message(text: str, update):
    chat_id = update["message"]["chat"]["id"]
    params = {"text": text, "chat_id": chat_id}
    requests.get(url=api_url+"sendMessage", params=params)

def updater():
    '''One updater to rule them all'''
    def get_updates():
        '''Requests updates from Telegram API using token, returns JSON.'''
        response = requests.get(api_url + "getUpdates").json()
        if response["ok"]:
            return response["result"]
        else:
            return False

    def updates_parser():
        '''Splits JSON in separate uptades and parses its fields'''
        if get_updates:
            for update in get_updates():
                update_id = update["update_id"]
                message = update["message"]
                chat_id = message["chat"]["id"]
                # To mark as read
                requests.get(url=api_url+"getUpdates",\
                    params={"offset": update_id + 1})

                if "entities" in message:
                    print("Got a command!")
                    for entity in message["entities"]:
                        if entity["type"] == "bot_command":
                            print("parsed the command")
                
                #if "text" in message:
                #    send_message(message["text"], update)
            
                print(f"There's an update with ID {update_id}")
        
        else:
            print("Error retrieving updates")
    
    updates_parser()

while True:
    time.sleep(1)
    updater()
