# vulnerable_app.py
# 此程式碼為教學用途，故意包含大量 Bug / Vulnerability / Code Smell
# 適合用 SonarQube 掃描示範

import os
import secrets
import subprocess
import hashlib
import json
import sqlite3
import logging
import ast
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PASSWORD = os.environ.get("APP_PASSWORD")  # Hardcoded password -> Fixed: Load from environment
API_KEY = os.environ.get("APP_API_KEY")  # Hardcoded secret -> Fixed: Load from environment
INSECURE_API_URL = os.environ.get("API_URL", "https://secure-api.com/data")

users = []

# =========================
# SQL Injection
# =========================
def login(username, password):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # SQL Injection -> Fixed: Parameterized query
    query = "SELECT * FROM users WHERE username=? AND password=?"

    cursor.execute(query, (username, password))

    result = cursor.fetchone()

    conn.close()

    if result:
        return True
    else:
        return False


# =========================
# Command Injection
# =========================
def ping_host(ip):
    # Command Injection -> Fixed: Use subprocess.run without shell=True
    try:
        subprocess.run(["ping", "-c", "1", ip], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Ping failed: {e}")


# =========================
# Unsafe subprocess
# =========================
def run_command(cmd):
    if isinstance(cmd, str):
        cmd = cmd.split()
    subprocess.run(cmd, check=True)


# =========================
# Weak Hash Algorithm
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# =========================
# Predictable Random
# =========================
def generate_token():
    return secrets.randbelow(9000) + 1000


# =========================
# Dangerous Pickle Load
# =========================
def load_user_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# =========================
# Division by Zero
# =========================
def divide(a, b):
    if b == 0:
        logger.warning("Zero division attempted.")
        return None
    return a / b


# =========================
# Unused Variable
# =========================
def calculate():
    x = 100
    y = 200
    # unused variable -> Fixed: Removed z

    return x + y


# =========================
# Duplicate Code
# =========================
def add_numbers(a, b):
    result = a + b
    print("Result:", result)
    return result


# Duplicate Code -> Fixed: Removed redundant add_numbers2


# =========================
# Infinite Recursion
# =========================
def recursive(depth=0, max_depth=5):
    if depth >= max_depth:
        return "Max depth reached"
    return recursive(depth + 1, max_depth)


# =========================
# Bare Except
# =========================
def unsafe_exception():
  
    except ZeroDivisionError as e:
        logger.error(f"Error occurred: {e}")


# =========================
# Debug Code
# =========================
def debug_mode():
    logger.debug("DEBUG MODE ENABLED")


# =========================
# Hardcoded URL
# =========================
def call_api():
    import requests
    url = INSECURE_API_URL

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"API call failed: {e}")
        return ""


# =========================
# File Resource Leak
# =========================
def read_file():
    if os.path.exists("test.txt"):
        with open("test.txt", "r", encoding="utf-8") as f:
            data = f.read()
        return data
    return ""


# =========================
# Unsafe Eval
# =========================
def calculate_input(user_input):
    try:
        return ast.literal_eval(user_input)
    except (ValueError, SyntaxError) as e:
        logger.error(f"Invalid input: {e}")
        return None


# =========================
# Global Variable Abuse
# =========================
class Counter:
    def __init__(self):
        self.count = 0

    def increase(self):
        self.count += 1


# =========================
# Long Function
# =========================
def huge_function():
    lines = [f"line{i}" for i in range(1, 21)]
    print("\n".join(lines))


# =========================
# Unreachable Code
# =========================
def test_return():
    print("Executing return statement")
    return True
    # Never execute -> Fixed: Removed unreachable code


# =========================
# None Comparison
# =========================
def check_none(value):
    if value is None:
        return True
    return False


# =========================
# Mutable Default Argument
# =========================
def append_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items


# =========================
# Sensitive Information Leak
# =========================
def print_credentials():
    pass


# =========================
# Main
# =========================
if __name__ == "__main__":

    print(login("admin", "admin123"))

    ping_host("127.0.0.1")

    print(hash_password("mypassword"))

    print(generate_token())

    unsafe_exception()

    debug_mode()

    print(calculate_input("100"))

    huge_function()
