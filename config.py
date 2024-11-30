"""Configuration management for the Wyze Light Control application."""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class WyzeConfig:
    email: str = os.getenv('WYZE_EMAIL', 'quinn@coincidence.net')
    password: str = os.getenv('WYZE_PASSWORD', 'Fr33d0m2022!!')
    key_id: str = os.getenv('WYZE_KEY_ID', '4541b08e-139b-4185-8bfa-8d229b655fce')
    api_key: str = os.getenv('WYZE_API_KEY', 'xhcqmuRHM26j36ZzERPwxGru0i8kg3JtYREMU47Hjsrjs0S7xBm8OJcCcFrc')

@dataclass
class AppConfig:
    debug: bool = True
    host: str = '0.0.0.0'
    port: int = 5001
    template_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

# Global config instances
wyze_config = WyzeConfig()
app_config = AppConfig()
