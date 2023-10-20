import hashlib

global username
# the dictionary which use to store data
user_info = {}


def authenticate(username, password):
    if username in user_info:
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if user_info[username]['password'] == hashed_password:
            return True
    return False


def user_config(file_name):
    try:
        with open(file_name, 'r') as file:
            for line in file:
                username, password, user_type, privilege = line.strip().split(',')
                user_info[username] = {'password': password, 'user_type': user_type, 'privilege': int(privilege)}
    except FileNotFoundError:
        print(f"Configuration file '{file_name}' not found.")


# Write patient data to the data file
def write_patient_data(file_name, data):
    with open(file_name, 'a') as file:
        file.write(data)


# register the staff+ patient to User_data file
def register_user(file_name, username, password, user_type, privilege):
    hashed_password = hashlib.md5(password.encode()).hexdigest()  # Hash the password
    with open(file_name, 'a') as file:
        data = f"{username},{hashed_password},{user_type},{privilege}\n"
        file.write(data)


def read_patient_data(file_name, username):
    try:
        with open(file_name, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                data_sensitivity = data[4]
                if has_privilege(username, data_sensitivity):
                    print("Patient Data:", data)
    except FileNotFoundError:
        print(f"Data file '{file_name}' not found.")


# Check if a user has the privilege to access data
def has_privilege(username, data_sensitivity):
    if username in user_info:
        user_privilege = user_info[username]['privilege']
        data_sensitivity_level = get_sensitivity_level(data_sensitivity)
        return user_privilege >= data_sensitivity_level
    return False


# Map sensitivity levels to numeric values
def get_sensitivity_level(data_sensitivity):
    sensitivity_levels = {
        "low": 1,
        "medium": 2,
        "high": 3
    }
    return sensitivity_levels.get(data_sensitivity.lower(), 0)


def edit_patient_data(file_name, patient_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        found = False
        with open(file_name, 'w') as file:
            for line in lines:
                data = line.strip().split(',')
                name = data[0]
                if name == patient_name:
                    found = True
                    print(f"Editing data for {name}:")
                    sickness = input("Sickness: ")
                    drugs = input("Drugs: ")
                    lab_tests = input("Lab Test Prescriptions: ")
                    sensitivity = input("Data Sensitivity (Low/Medium/High): ")
                    updated_data = f"{name},{sickness},{drugs},{lab_tests}{sensitivity}\n"
                    file.write(updated_data)
                else:
                    file.write(line)

        if not found:
            print(f"Patient with the name {patient_name} not found.")
    except FileNotFoundError:
        print(f"Data file '{file_name}' not found.")


if __name__ == "__main__":
    config_file = "User_data.txt"
    data_file = "medical_data.txt"

    user_config(config_file)
    logged_in = False  # Add this variable to track user login status
    while True:
        print("1. Login")
        print("2. Write Patient Data")
        print("3. Read Patient Data")
        print("4. Register New User")
        print("5. Edit Patient Data")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            if logged_in:
                print("You are already logged in.")
            else:
                username = input("Enter your username: ")
                password = input("Enter your password: ")

                if authenticate(username, password):
                    print(f"Logged in as {username}")
                    logged_in = True  # Set the login status to True
                else:
                    print("Authentication failed.")

        elif choice == "2":
            if not logged_in:
                print("Please login first.")
            else:
                if user_info[username]['user_type'] == "staff":
                    print("Write patient data:")
                    name = input("Name: ")
                    sickness = input("Sickness: ")
                    drugs = input("Drug Prescriptions: ")
                    lab_tests = input("Lab Test Prescriptions: ")
                    sensitivity = input("Data Sensitivity (Low/Medium/High): ")
                    data = f"{name},{sickness},{drugs},{lab_tests},{sensitivity}\n"
                    write_patient_data(data_file, data)
                else:
                    print("Patients are not allowed to write data.")

        elif choice == "3":
            if "username" not in locals():
                print("Please login first.")
            else:
                print(f"Read patient data as {username}:")
                read_patient_data(data_file, username)

        elif choice == "4":
            if not logged_in:
                print("Please login first.")
            else:
                if user_info[username]['user_type'] == "staff":
                    print("Register a new user:")
                    username = input("username: ")
                    password = input("password: ")
                    user_type = input("register as staff or patient: ")
                    privilege = input("privilege level: ")
                    data = f"{username},{password},{user_type},{privilege}\n"
                    register_user(config_file, username, password, user_type, privilege)
                    print("New user has been successfully registered.")
                else:
                    print("Not allowed to register new patients.")
        elif choice == "5":
            if not logged_in:
                print("Please login first.")
            else:
                if user_info[username]['user_type'] == "staff" and user_info[username]['privilege'] == 2:
                    patient_name = input("Enter the name of the patient to edit: ")
                    edit_patient_data(data_file, patient_name)
                else:
                    print("Not allowed to edit patient data.")
        elif choice == "6":
            print("Successfully logged out!")
            break
        else:
            print("Invalid choice. Please try again.")
