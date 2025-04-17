import time
import random
import os
import re
from datetime import datetime, timedelta

log_file = "lottery_log.txt"
user_file = "registered_users.txt"
registered_users = set()

def is_valid_username(username):
    return username.isalnum()

def save_users():
    with open(user_file, 'w') as f:
        for user in registered_users:
            f.write(f"{user}\n")

def load_users():
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            for line in f:
                registered_users.add(line.strip())

def log_event(text):
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()} - {text}\n")

def register_users(end_time):
    last_log_time = time.time()
    while time.time() < end_time:
        remaining = int(end_time - time.time())
        print(f"Time left: {remaining // 60} minutes")
        username = input("Enter username to register: ").strip()
        if not is_valid_username(username):
            print("Invalid username")
            continue
        if username in registered_users:
            print("Username already registered")
            continue
        registered_users.add(username)
        log_event(f"User registered: {username}")
        print(f"Registered: {len(registered_users)} users")
        save_users()
        if time.time() - last_log_time >= 300:
            save_users()
            last_log_time = time.time()
    return len(registered_users)

def pick_winner():
    winner = random.choice(list(registered_users))
    log_event(f"Winner: {winner}")
    print("\nLottery Winner")
    print("==============")
    print(f"Winner: {winner}")
    print(f"Total Participants: {len(registered_users)}")

load_users()
start = time.time()
end = start + 3600
log_event("Lottery started")
users_count = register_users(end)
if users_count < 5:
    print("Less than 5 users, extending 30 minutes")
    end += 1800
    users_count = register_users(end)
if users_count == 0:
    print("No users registered. Exiting.")
    log_event("No users registered")
else:
    pick_winner()
