## this bat script has to run on powershell 

# install first installation bat script
`./install_first_mosquitto.bat`

# secound bat script to run mosquitto in port 1883
`./install_mosquitto.bat`

# it has to be run in run as admistration 
# to run mosquitto along with the config file # check testconfig.txt
`mosquitto -v -c .\testconfig.txt`   

# cmd
`sc query mosquitto`
`net start mosquitto` #start command
`net stop mosquitto`  #stop command


# need to do
test config file automation creation
using bat 