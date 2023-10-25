from vosk import Model, KaldiRecognizer
import pyaudio
import paho.mqtt.client as mqtt
import time
from gtts import gTTS
import os

# set language for gtts module (speech output)
language = 'de'

# instanziate speech model and recognizer
model = Model(r'german')
recognizer = KaldiRecognizer(model, 16000)

# power consumtion of various components
washer = 2000
pc = 1000
dryer = 1500
power_consumption = " "
power_production = " "

# reconize from the microphone
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# define mqtt host and instanziate client instance
mqtt_host = "test.mosquitto.org"
mqtt_client = mqtt.Client("SolarEdge666")

#this is using mqtt to get the power consumption data
def get_consumption():
    mqtt_client.on_message = on_message_consumption
    mqtt_client.connect(mqtt_host)
    mqtt_client.subscribe("haus4711/smartmeter/consumption", qos=1)
    mqtt_client.loop_start()
    time.sleep(0.2)
    mqtt_client.loop_stop()
    mqtt_client.unsubscribe("haus4711/smartmeter/consumption")

# this function is using mqtt to get the power produces by solar edge
def get_production():
    mqtt_client.on_message = on_message_production
    mqtt_client.connect(mqtt_host)
    mqtt_client.subscribe("haus4711/solaredge/production", qos=1)
    mqtt_client.loop_start()
    time.sleep(0.2)
    mqtt_client.loop_stop()
    mqtt_client.unsubscribe("haus4711/solaredge/production")


# handle subscribe call for production topic
def on_message_production(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    response = str(msg.payload).split("'",2)[1]

    # write data to global variable
    global power_production
    power_production = response

# handle subscribe call for consumtion topic
def on_message_consumption(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    response = str(msg.payload).split("'",2)[1]

    # write data to global variable
    global power_consumtion
    power_consumtion = response


while True:
    # speech input stream
    data = stream.read(4096, exception_on_overflow=False)
    if len(data) == 0:
        break

    # if speech was recognized, evaluate results
    if recognizer.AcceptWaveform(data):
        result = recognizer.FinalResult()
        splitted_result = result.split('"',4)
        print(splitted_result[3])
        
        #check user input
        if(splitted_result[3] == "wieviel strom wird im moment produziert" or splitted_result[3] == "wie viel strom wird im moment produziert"):
            get_production()
            output = "Aktuell werden " + power_production + " Watt produziert"

            # create answer for given question and save it to mp3 file
            s = gTTS(output, lang=language, slow=False)
            s.save('response1.mp3')

            # play answer
            os.system("afplay " + "response1.mp3")


        if(splitted_result[3] == "wieviel strom wird im moment verbraucht" or splitted_result[3] == "wie viel strom wird im moment verbraucht"):
            get_consumption()
            output = "Aktuell werden " + power_consumtion + " Watt verbraucht"

            # create answer for given question and save it to mp3 file
            s = gTTS(output, lang=language, slow=False)
            s.save('response2.mp3')

            # play answer
            os.system("afplay " + "response2.mp3")


        if(splitted_result[3] == "kann ich meine waschmaschine nachhaltig betreiben"):
            get_consumption()
            get_production()
            result = int(power_production) - int(power_consumtion)

            if result >= washer:
                output = "JA! Die Waschmaschine kann nachhaltig betrieben werden"
            else:
                output = "NEIN! Die Waschmaschine kann nicht nachhaltig betriben werden"

            # create answer for given question and save it to mp3 file
            s = gTTS(output, lang=language, slow=False)
            s.save('response3.mp3')

            # play answer
            os.system("afplay " + "response3.mp3")


        if(splitted_result[3] == "kann ich meinen trockner nachhaltig betreiben"):
            get_consumption()
            get_production()
            result = int(power_production) - int(power_consumption)

            if result >= dryer:
                output = "JA! Der Trockner kann nachhaltig betrieben werden"
            else:
                output = "NEIN! Der Trockner kann nicht nachhaltig betriben werden"

            # create answer for given question and save it to mp3 file
            s = gTTS(output, lang=language, slow=False)
            s.save('response4.mp3')

            # play answer
            os.system("afplay " + "response4.mp3")


        if(splitted_result[3] == "kann ich meinen pc nachhaltig betreiben"):
            get_consumption()
            get_production()
            result = int(power_production) - int(power_consumption)

            if result >= pc:
                output = "JA! Der PC kann nachhaltig betrieben werden"
            else:
                output = "NEIN! Der PC kann nicht nachhaltig betriben werden"

            # create answer for given question and save it to mp3 file
            s = gTTS(output, lang=language, slow=False)
            s.save('response5.mp3')

            # play answer
            os.system("afplay " + "response5.mp3")