# login py file


# Register feature
import csv
import re

def main():
    register()


def register():
    """
    Register function - requires a username and password from the user and stores it in the logindetails.csv file.
    """
    while True:
        try:
            username = input("Your username should be between 8 and 16 characters long and only consist of letters a-z and numbers 0-9.\n\nPlease enter a username: ")
            validate_username(username) # Call function for username validation.
            print("Username confirmed.")
            break
        except ValueError as e:
            print(f"\nINVALID USERNAME: {e} \nPlease try again.\n")
            continue   
    while True:
        try:
            password = input("\nYour password should contain at least one capital letter, at least one of '?' or '!', letters a-z and numbers 0-9 and be between 8 and 16 characters long.\n\nPlease enter a password: ")
            validate_password(password) # Call function for password validation.
            print("Password confirmed.")
            break    
        except ValueError as e:
            print(f"\nINVALID USERNAME: {e} \nPlease try again.\n")
            continue
    with open("./files/logindetails.csv", "a") as file:
        file.write(f"{username},{password},{True}\n")
        file.close()
        
        
def validate_username(username):
    """
    Validates the inputted username.
    
    Args:
        username (str): username inputted by user.

    Raises:
        ValueError: if no spaces
        ValueError: length (8 < password < 16).
        ValueError: alphanumeric characters.
    """
    # Check whether username already exists using a csv object - iterated through.
    with open("./files/logindetails.csv", "r") as file:
        file_reader = csv.reader(file)
        next(file_reader)
        for row in file_reader:
            if username == row[0]:
                raise ValueError("This username already exists. Please try an alternative username.")
            else:
                continue
            
    if " " in username:
        raise ValueError("Do not enter spaces in your username.")
    elif len(username) < 8 or len(username) > 16:
        raise ValueError("Please ensure that your username is between 8 and 16 characters long.")
    elif username.isalnum() == False:
        raise ValueError("Please ensure that your username contains only numbers and letters.")

def validate_password(password):
    """
    Validates the inputted password.

    Args:
        password (str): password inputted by user
   Raises:
        ValueError: absence of spaces.
        ValueError: length (8 < password < 16).
        ValueError: at least one capital letter in the passsword.
        ValueError: alphanumeric character / ! / ?.
    """
    pw_chars = r'^[A-Za-z0-9!?]+$'
    punc_chars = r'[!?]'
    if " " in password:
        raise ValueError("Do not enter spaces in your password.")
    elif len(password) < 8 or len(password) > 16:
        raise ValueError("Please ensure that your password is between 8 and 16 characters long.")
    elif not any(c.isupper() for c in password):
        raise ValueError("Please ensure that your password contains at least one capital letter.")
    elif not re.match(pw_chars, password) or not re.search(punc_chars, password):
        raise ValueError("Please ensure that your password contains only letters a-z, numbers 0-9, and at least one of '!' or '?'.")
    

if __name__ == "__main__":
    main()