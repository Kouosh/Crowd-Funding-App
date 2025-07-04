import json
import os
import re

USERS_FILE = os.path.join('data', 'users.json')

# Egyptian phone number regex: starts with 01, then 0/1/2/5, then 8 digits
def is_valid_egyptian_phone(phone):
    return re.fullmatch(r"01[0125][0-9]{8}", phone) is not None

def is_valid_email(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email) is not None

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def register():
    print("\n--- User Registration ---")
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    confirm_password = input("Confirm password: ").strip()
    phone = input("Mobile phone (Egyptian): ").strip()

    if not first_name or not last_name:
        print("First and last name are required.")
        return
    if not is_valid_email(email):
        print("Invalid email format.")
        return
    if password != confirm_password:
        print("Passwords do not match.")
        return
    if len(password) < 6:
        print("Password must be at least 6 characters.")
        return
    if not is_valid_egyptian_phone(phone):
        print("Invalid Egyptian phone number.")
        return

    users = load_users()
    if any(u['email'] == email for u in users):
        print("Email already registered.")
        return

    user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,  # In production, hash this!
        'phone': phone
    }
    users.append(user)
    save_users(users)
    print("Registration successful! You can now log in.")

def login():
    print("\n--- User Login ---")
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    users = load_users()
    for user in users:
        if user['email'] == email and user['password'] == password:
            print(f"Welcome, {user['first_name']}!")
            return user
    print("Invalid email or password.")
    return None 