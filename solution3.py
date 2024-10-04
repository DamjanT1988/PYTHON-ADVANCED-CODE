import requests
import hmac
import hashlib

# Skapa ett 1000x1000 rutnät med alla lysdioder släckta (False)
grid_size = 1000
panel = [[False for _ in range(grid_size)] for _ in range(grid_size)]

# Läs in instruktionerna från filen "contr-instr.txt"
def read_instructions_from_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

# Bearbeta varje instruktion och uppdatera panelen
def process_instruction(instruction):
    instruction = instruction.strip()
    print(f"Bearbetar instruktion: {instruction}")  # Debug: Visa varje instruktion
    
    if instruction.startswith("turn on"):
        action = "on"
        instruction = instruction[len("turn on "):]
    elif instruction.startswith("turn off"):
        action = "off"
        instruction = instruction[len("turn off "):]
    elif instruction.startswith("toggle"):
        action = "toggle"
        instruction = instruction[len("toggle "):]
    
    # Extrahera start- och slutkoordinater
    start_coords, end_coords = instruction.split(" through ")
    x1, y1 = map(int, start_coords.split(","))
    x2, y2 = map(int, end_coords.split(","))
    
    print(f"Åtgärd: {action}, från ({x1},{y1}) till ({x2},{y2})")  # Debug: Visa vilka koordinater vi arbetar med
    
    # Uppdatera panelens tillstånd baserat på instruktionen
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if action == "on":
                panel[x][y] = True
            elif action == "off":
                panel[x][y] = False
            elif action == "toggle":
                panel[x][y] = not panel[x][y]

# Räkna hur många lysdioder som är tända
def count_lights_on():
    return sum(sum(row) for row in panel)

# Steg 1: Bearbeta alla instruktioner från filen
instructions = read_instructions_from_file('contr-instr.txt')

if not instructions:
    print("Inga instruktioner hittades.")  # Debug: Säkerställ att filen lästes korrekt
else:
    print(f"Antal instruktioner: {len(instructions)}")  # Debug: Visa hur många instruktioner som lästes

for instruction in instructions:
    process_instruction(instruction)

# Steg 2: Räkna antalet lysdioder som är tända
current_lights_on = count_lights_on()

# Debug: Visa hur många lysdioder som faktiskt är tända
print(f"Antal lysdioder som är tända: {current_lights_on}")

# Enligt uppgiften är endast 597 lysdioder tända, vilket verkar vara för få.
expected_lights_on = 597
broken_diods = abs(current_lights_on - expected_lights_on)

print(f"Antal trasiga lysdioder: {broken_diods}")

# Steg 3: Skicka beställningen med antalet trasiga lysdioder via API:t
def place_order(broken_diods, callback_url):
    url = "https://webbhuset.se/employment-challenge/order"
    headers = {"X-Reply-To": callback_url}  # Använd callback URL för att ta emot svar från API:t
    response = requests.post(url, headers=headers, data=str(broken_diods))

    # Skriv alltid ut statuskod och respons-text
    print(f"Statuskod: {response.status_code}")
    print(f"Responstext: {response.text}")

    if response.status_code == 200:
        print("Beställning skickad framgångsrikt!")
    else:
        print(f"Misslyckades med att skicka beställning.")

# Steg 4: Placera beställning på trasiga lysdioder och använd en giltig callback URL
callback_url = "http://example.com:8000"  # Ersätt med din giltiga callback URL
place_order(broken_diods, callback_url)
