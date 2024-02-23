python3 -m venv venv
`source venv/bin/activate`


Install virtualenv Globally:
Open a command prompt as an administrator and run the following command:

bash
Copy code
`pip install virtualenv`
Create the Virtual Environment Using virtualenv:
After installing virtualenv, create the virtual environment:

bash
Copy code
`virtualenv venv`
Activate the virtual environment:

On Windows:
bash
Copy code
`.\venv\Scripts\activate`
`deactivate`

# requirements
# after enteing into venv you can freeze package using these commands
`pip freeze > requirements.txt`

# build
`pyinstaller app.py` #this comment will create a build and dist file 
# import sys and import os 

# onefile command
`pyinstaller --name RigQue --onefile --windowed --icon=image.ico app.py`

# asset management
set the asset folder and check the exe is working or not 

# inno setup
step1: create a new script file using the script wizard .
--------------------click ok ---------------------------
--------------------click next--------------------------
step2: aplication name:
       version no:
       comapny name:
       company site:
       -----------------click next-------------------
       -----------------click next-------------------
step3:browse the exe file 
      Add the asset folders
      -------------------click next-------------------
step4: uncheck it and go for next------
step5: schortcut for desktop and window icon needed 
---------------------click next-----------------------
step6: upload license txt
----------------------next----------------------------
----------------------next----------------------------
step7: compiler setting
      -mention the output folder
      -output file name 
      -output icon for setup
      ---------------------------next-----------------
      ---------------------------next-----------------

----------------finish--------------------------------

step8: select no
    go to files section DestDir: "{app}/asset"   #add /asset
    -save the file
