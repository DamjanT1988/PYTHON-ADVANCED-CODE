import hashlib

def very_secure_hashing_function(password: str) -> str:
    # Steg 1: starta hasing av SHA-1
    current_hash = hashlib.sha1(password.encode()).hexdigest()
    
    # Steg 2: upprepa 100 gånger
    for _ in range(100):
        # Ta föersta och sista tecknet av nuvarande hash
        first_char = current_hash[0]
        last_char = current_hash[-1]
        
        # konkatenera och konvertera till ett num
        hex_value = int(first_char + last_char, 16)
        
        # Steg 3: bestäm vilken hashing-algoritm som ska användas
        if hex_value < 128:
            current_hash = hashlib.sha1(current_hash.encode()).hexdigest()
        else:
            current_hash = hashlib.md5(current_hash.encode()).hexdigest()
    
    # returnera den slutgiltiga hashen
    return current_hash

# Exampel
password = "Password123!"
final_hash = very_secure_hashing_function(password)
print("Final hashed password:", final_hash)
