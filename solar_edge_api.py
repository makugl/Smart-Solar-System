import requests
from datetime import datetime
import pprint
import paho.mqtt.client as mqtt

def get_and_publish():
    # datetime object containing current date and time
    now = datetime.now()
    print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print("date and time =", dt_string)

    start_end_day = now.strftime("%Y-%m-%d")
    start_end_time = now.strftime("%H:%M:%S")

    # api-endpoint
    URL = "https://monitoringapi.solaredge.com/site/2835613/power?startTime=" + start_end_day + "%20" + start_end_time +"&endTime=" + start_end_day + "%20" + start_end_time +"&api_key=X6E19DPG8P7IW99N64OPE2HC3O1BLRQH"

    # sending get request and saving the response as response object
    r = requests.get(url = URL)
    
    # extracting data in json format
    data = r.json()

    # pretty print the output
    #pprint.pprint(data)

    #get only power value from response
    current_power = data['power']['values'][0]['value']
    if current_power == None:
        print("power not readable atm. try again in a few seconds...")
        return

    # no float data needed
    power_production_mqtt = int(current_power)
    print(power_production_mqtt)

    #The IR-read-head unfortunately became defective. 
    # Therefore, the energy requirement was now published manually via mqtt. 
    # This value should come in future again from the smart meter
    defined_consumption = 1400

    # publish data
    mqtt_publisher(power_production_mqtt, defined_consumption)

# publish data to defined mqtt topic
# data should retain on broker and will be sent with qos=1
def mqtt_publisher(production, consumption):
    mqtt_client.connect(mqtt_host)
    mqtt_client.publish("haus4711/solaredge/production", production, retain=True, qos=1)
    mqtt_client.publish("haus4711/smartmeter/consumption", consumption, retain=True, qos=1)


if __name__ == '__main__':
    mqtt_host = "test.mosquitto.org"
    mqtt_client = mqtt.Client("SolarEdge4711")

    get_and_publish()
