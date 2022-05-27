import serial,time
import requests
import re

# The URL of the Snapcast server
snap_url = 'http://tea.local:1780/jsonrpc'

# The JSON object we will use to communicate with the Snapcast API
cmd_obj = [
    {
        "id": "1",
        "jsonrpc": "2.0",
        "method": "Client.SetVolume",
        "params": {
            "id": "bedroom",
            "volume": {
                "percent": 10
            }
        }
    },
    {
        "id": "2",
        "jsonrpc": "2.0",
        "method": "Client.SetVolume",
        "params": {
            "id": "bathroom",
            "volume": {
                "percent": 10
            }
        }
    },
    {
        "id": "3",
        "jsonrpc": "2.0",
        "method": "Client.SetVolume",
        "params": {
            "id": "192.168.1.126",
            "volume": {
                "percent": 10
            }
        }
    },
    {
        "id": "4",
        "jsonrpc": "2.0",
        "method": "Client.SetVolume",
        "params": {
            "id": "kitchen",
            "volume": {
                "percent": 10
            }
        }
    }
]

rooms = {"bedroom","bathroom","192.168.1.126","kitchen"}
launching = True 
last = {"timestamp":0,"target":{"bathroom":10,"bedroom":10,"kitchen":10,"192.168.1.126":10}}


def parseCommands(receivedCommand):
    #print(receivedCommand)
    now = time.time()
    for i in range(4):
      target = int(answer.split(",")[i].strip())
      #print("target ",target)
      cmd_obj[i]["params"]["volume"]["percent"] = target

# This part ensures that we're not sending updates more than every 2 seconds
    if(now-last["timestamp"] > 2.0) :
        print("sending")
        #print(cmd_obj)
        x = requests.post(snap_url, json = cmd_obj)
#        print(x.text)
        print(x.status_code)
        last["target"] = cmd_obj
        last["timestamp"] = time.time()

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')
    if(launching):
        last["timestamp"] = time.time()
# Connecting to the Arduino
    with serial.Serial("/dev/ttyACM0", 9600, timeout=2) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            print("- - - -")
            try:
                while True:
                    answer=arduino.readline().decode('utf-8')
                    #print((answer))
                    verification = re.split(",",answer)
                    #print(verification)
		    #Check if we've received a command with the proper syntax 
                    if(len(verification)<4):
                        print("Received something weird, ignoring it")
                    else:
                        #print("parsing")
                        parseCommands(answer)
		    
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")
