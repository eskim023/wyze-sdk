import os
import sys
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError

# Your credentials
WYZE_EMAIL = "quinn@coincidence.net"
WYZE_PASSWORD = "Fr33d0m2022!!"
WYZE_KEY_ID = "4541b08e-139b-4185-8bfa-8d229b655fce"
WYZE_API_KEY = "xhcqmuRHM26j36ZzERPwxGru0i8kg3JtYREMU47Hjsrjs0S7xBm8OJcCcFrc"

def main():
    # Initialize the client and get access token
    try:
        # First get the access token
        print("Authenticating with Wyze...")
        auth_response = Client().login(
            email=WYZE_EMAIL,
            password=WYZE_PASSWORD,
            key_id=WYZE_KEY_ID,
            api_key=WYZE_API_KEY
        )
        
        # Create a new client with the access token
        client = Client(token=auth_response['access_token'])
        
        # Get all devices
        print("Getting devices...")
        devices = client.devices_list()
        
        # Filter for bulbs
        bulbs = [device for device in devices if device.product.model.startswith('WLPA') or 
                device.product.model.startswith('WLPB')]
        
        if not bulbs:
            print("No lightbulbs found in your Wyze account!")
            return
        
        # Refresh status for all bulbs
        bulbs = [client.bulbs.info(device_mac=bulb.mac) for bulb in bulbs]
        
        # Print initial state
        print("\nAvailable lightbulbs:")
        for i, bulb in enumerate(bulbs, 1):
            status = "ON" if bulb.is_on else "OFF"
            print(f"{i}. {bulb.nickname} ({status})")
        
        print("\nTo control a bulb, run this script again and provide the bulb number as an argument.")
        print("Example: python3 control_lights.py 1")
        
        # Check if a bulb number was provided as argument
        if len(sys.argv) > 1:
            try:
                bulb_index = int(sys.argv[1]) - 1
                if 0 <= bulb_index < len(bulbs):
                    selected_bulb = bulbs[bulb_index]
                    
                    # Get fresh status
                    selected_bulb = client.bulbs.info(device_mac=selected_bulb.mac)
                    
                    if selected_bulb.is_on:
                        print(f"Turning OFF {selected_bulb.nickname}...")
                        client.bulbs.turn_off(
                            device_mac=selected_bulb.mac,
                            device_model=selected_bulb.product.model
                        )
                        print(f"Turned OFF {selected_bulb.nickname}")
                    else:
                        print(f"Turning ON {selected_bulb.nickname}...")
                        client.bulbs.turn_on(
                            device_mac=selected_bulb.mac,
                            device_model=selected_bulb.product.model
                        )
                        print(f"Turned ON {selected_bulb.nickname}")
                else:
                    print(f"Error: Please enter a valid bulb number between 1 and {len(bulbs)}")
            except ValueError:
                print("Error: Please provide a valid number")
                print(f"Usage: python3 {sys.argv[0]} BULB_NUMBER")

    except WyzeApiError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
