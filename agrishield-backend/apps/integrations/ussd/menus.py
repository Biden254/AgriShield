"""
Define USSD menu logic here.
Each function handles a menu level and returns the text to display.
"""

def main_menu():
    return "Welcome to the Farmer App:\n1. Register\n2. My Profile\n3. Alerts"

def register_menu():
    return "Enter your name:"

def profile_menu(user):
    return f"My Profile:\nName: {user.name}\nVillage: {user.village.name if user.village else 'N/A'}"

def alerts_menu(alerts):
    text = "Latest Alerts:\n"
    for i, alert in enumerate(alerts[:3], 1):
        text += f"{i}. {alert.message[:25]}...\n"
    return text
