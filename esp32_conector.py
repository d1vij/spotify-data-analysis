import serial
from time import sleep, time

SERIAL = serial.Serial("COM5", baudrate=115200)
def rw():
    current_playing : str= "P:"+get_current_playing()
    SERIAL.write(current_playing.encode('utf-8')) # sending track info to esp

    st = time()

    while True: # if incoming buffer stream has data
        try :
            response = SERIAL.readline().decode('utf-8').strip()
        except UnicodeDecodeError:
            response = SERIAL.readline()
        if response == "OK" :
            print("$ acknowledgment receieved from esp...")
            break
        else: print(response)

        if time() - st > 5:
            print("no response recieved from esp32 breaking out and resendinginfo ")



while True:
    rw()
    sleep(5)