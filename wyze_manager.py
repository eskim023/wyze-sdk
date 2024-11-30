"""Wyze device management module."""
from typing import List, Optional, Dict
import logging
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError
from config import wyze_config

logger = logging.getLogger(__name__)

class WyzeManager:
    def __init__(self):
        """Initialize the Wyze Manager."""
        self._client: Optional[Client] = None
        self._token: Optional[str] = None
        self.devices = None
        self.bulb_info = {}
        self._refresh_devices()

    def _refresh_devices(self):
        """Get fresh device list from API."""
        try:
            self._authenticate()
            self.devices = self.client.devices_list()
            # Reset bulb info cache
            self.bulb_info = {}
        except Exception as e:
            logger.error(f"Error refreshing devices: {e}")
            raise

    @property
    def client(self) -> Client:
        """Get or create an authenticated Wyze client."""
        if not self._client:
            self._authenticate()
        return self._client

    def _authenticate(self) -> None:
        """Authenticate with Wyze API."""
        try:
            logger.info("Authenticating with Wyze...")
            auth_response = Client().login(
                email=wyze_config.email,
                password=wyze_config.password,
                key_id=wyze_config.key_id,
                api_key=wyze_config.api_key
            )
            self._token = auth_response['access_token']
            self._client = Client(token=self._token)
            logger.info("Authentication successful")
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise

    def get_bulb_names(self) -> List[Dict]:
        """Get basic info about all Wyze bulbs without status."""
        try:
            if not self.devices:
                self._refresh_devices()
            
            bulbs = []
            for device in self.devices:
                if device.product.model.startswith(('WLPA', 'WLPB')):
                    bulbs.append({
                        'name': device.nickname,
                        'mac': device.mac,
                        'is_online': device.is_online
                    })
            
            return bulbs
        except Exception as e:
            logger.error(f"Error getting bulbs: {e}")
            raise

    def get_bulb_status(self, mac: str) -> Dict:
        """Get the current status of a specific bulb."""
        try:
            # Use cached bulb info if available
            if mac in self.bulb_info:
                return self.bulb_info[mac]

            if not self.devices:
                self._refresh_devices()

            # Find device in our list
            device = next((d for d in self.devices if d.mac == mac), None)
            if not device:
                raise Exception(f"Bulb {mac} not found")

            status = {
                'is_online': device.is_online,
                'is_on': False,
                'brightness': 0  # Add default brightness
            }

            # Only get detailed info if online
            if device.is_online:
                try:
                    bulb = self.client.bulbs.info(device_mac=mac)
                    status['is_on'] = bulb.is_on
                    status['brightness'] = bulb.brightness  # Add brightness info
                except Exception as e:
                    logger.error(f"Error getting bulb info for {mac}: {e}")

            # Cache the result
            self.bulb_info[mac] = status
            return status

        except Exception as e:
            logger.error(f"Error getting bulb status: {e}")
            raise

    def toggle_bulb(self, mac: str) -> Dict:
        """Toggle a specific bulb's state."""
        try:
            # Get fresh bulb info
            bulb = self.client.bulbs.info(device_mac=mac)
            current_state = bulb.is_on  # Using the property instead of calling it
            
            if current_state:
                self.client.bulbs.turn_off(device_mac=mac, device_model=bulb.product.model)
                new_state = False
            else:
                self.client.bulbs.turn_on(device_mac=mac, device_model=bulb.product.model)
                new_state = True
            
            return {
                'success': True,
                'is_on': new_state,
                'name': bulb.nickname
            }
        except Exception as e:
            logger.error(f"Error toggling bulb {mac}: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_bulbs(self) -> List[Dict]:
        """Get all Wyze bulbs with their current status."""
        try:
            if not self.devices:
                self._refresh_devices()
            
            bulbs = []
            
            for device in self.devices:
                if device.product.model.startswith(('WLPA', 'WLPB')):
                    bulb_status = self.get_bulb_status(device.mac)
                    bulbs.append({
                        'name': device.nickname,
                        'mac': device.mac,
                        'is_online': device.is_online,
                        'is_on': bulb_status['is_on']
                    })
                    logger.info(f"Bulb: {device.nickname} is {'ON' if bulb_status['is_on'] else 'OFF'}")
            
            return bulbs
        except Exception as e:
            logger.error(f"Error getting bulbs: {e}")
            raise

    def set_brightness(self, mac: str, brightness: int) -> Dict:
        """Set brightness for a specific bulb (0-100)."""
        try:
            # Ensure brightness is within valid range
            brightness = max(0, min(100, brightness))
            
            bulb = self.client.bulbs.info(device_mac=mac)
            self.client.bulbs.set_brightness(
                device_mac=mac,
                device_model=bulb.product.model,
                brightness=brightness
            )
            
            return {
                'success': True,
                'brightness': brightness,
                'name': bulb.nickname
            }
        except Exception as e:
            logger.error(f"Error setting brightness for bulb {mac}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
