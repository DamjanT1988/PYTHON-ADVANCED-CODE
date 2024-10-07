import hmac
import hashlib
import requests

# Steg 1:läs lösenorden från en fil
def read_passwords_from_file(filename):
    with open(filename, 'r') as file:
        passwords = [line.strip() for line in file.readlines()]
    return passwords

# Steg 2:Regler för lösenordspolicy
def contains_three_vowels(password):
    vowels = set("aeiou")
    count = sum(1 for char in password if char in vowels)
    return count >= 3

def contains_double_letter(password):
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            return True
    return False

def contains_no_forbidden_strings(password):
    forbidden_strings = ["ab", "cd", "pq", "xy"]
    return all(forbidden not in password for forbidden in forbidden_strings)

def is_password_secure(password):
    return (contains_three_vowels(password) and
            contains_double_letter(password) and
            contains_no_forbidden_strings(password))

# Steg 3:kolla igenom lösenorden från filen
passwords = read_passwords_from_file('passlist.txt')

secure_passwords = [pw for pw in passwords if is_password_secure(pw)]
answer = str(len(secure_passwords))

#Steg 4: Skapa signaturen
def create_signature(message, key):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

key = "xG9HlwoVJeA2"
signature = create_signature(answer, key)

# Steg 5: skicka POST-begäran
url = "https://webbhuset.se/employment-challenge/answer"
headers = {"X-Signature": signature}
response = requests.post(url, headers=headers, data=answer)

# Steg 6:Skriv ut resultatet
print(f"Antal säkra lösenord: {answer}")
print(f"Response status: {response.status_code}")
print(f"Response text: {response.text}")
