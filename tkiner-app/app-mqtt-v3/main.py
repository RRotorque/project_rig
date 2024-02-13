import subprocess
import os
import shutil
import time

# Define the paths to the scripts
script1_path = "install_first_mosquitto.bat"
script2_path = "automate_running_mosquitto.bat"
script4_path = "app.py"  # Replace with the actual name of your script4

# Function to check if Mosquitto is installed
def is_mosquitto_installed():
    try:
        subprocess.run(["mosquitto", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to run script1.bat
def run_script1():
    subprocess.run(["cmd", "/c", script1_path], shell=True)
# Function to run script2.py
def run_script2():
    subprocess.Popen(["cmd", "/c", script2_path], shell=True)

# Function to run script4.py
def run_script4():
    subprocess.Popen(["python", script4_path], shell=True)

# Main function
def main():
    # Run script1.bat to install Mosquitto if not installed
    print("Running script1.bat...")
    run_script1()

    # Run script2.py to activate Mosquitto
    print("Running script2.py to activate Mosquitto...")
    run_script2()

    # Wait for script2.py to finish activation (adjust the sleep duration as needed)
    time.sleep(5)

    # Run script4.py after script2.py is running
    print("Running script4.py...")
    run_script4()

if __name__ == "__main__":
    main()
