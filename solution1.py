import hashlib

def very_secure_hashing_function(password: str) -> str:
    # Step 1: Start by hashing the password using SHA-1
    current_hash = hashlib.sha1(password.encode()).hexdigest()
    
    # Step 2: Repeat 100 times
    for _ in range(100):
        # Take the first and last character of the current hash
        first_char = current_hash[0]
        last_char = current_hash[-1]
        
        # Concatenate and convert to a number
        hex_value = int(first_char + last_char, 16)
        
        # Step 3: Decide whether to use SHA-1 or MD5
        if hex_value < 128:
            current_hash = hashlib.sha1(current_hash.encode()).hexdigest()
        else:
            current_hash = hashlib.md5(current_hash.encode()).hexdigest()
    
    # The result after 100 iterations is our "very secure hash"
    return current_hash

# Example usage
password = "Password123!"
final_hash = very_secure_hashing_function(password)
print("Final hashed password:", final_hash)
