import json
import dweepy
import time
import os
import random
from paho.mqtt import client as mqtt_client
#import apprpriate modules

def lambda_handler(event, context):
    
    link_air = "4640D_air_con_sensor"; # ensure that when you use IFTT, https://dweet.io/dweet/for/4640D_air_con_sensor?status=onoff is the url for your web hook application

    link_light = "4640D_light_sensor"; # ensure that when you use IFTT, https://dweet.io/dweet/for/4640D_light_sensor?status=onoff is the url for your web hook application

    host = "44.221.118.197"; # broker's ip
    
    port = 1883 # broker's port

    topic = "brokerchannel" # broker's channel
    
    client_id = f'publish-{random.randint(0, 1000)}'

    mqtt_username = "4640D_user"; # mqtt user that was created on mqtt_server.

    mqtt_password = "4640D_password"; # mqtt password that was created on mqtt_server.

    query_air_state  = event['air_state']; #air_state's value, stored in variable "query_air_state"

    query_air_read  = event['air_read']; #air_read's value, stored in variable "query_air_read"
    
    query_light_state = event['light_state']; #light_state's value, stored in variable "query_light_state"

    query_light_bright = event['light_bright']; #query_light_bright's value, stored in variable "query_light_bright"
    
    query_air_state_low_cap = query_air_state.lower(); #Ensure low capitals for the inputs

    query_air_read_num_to_string = str(query_air_read);
    
    query_light_state_low_cap = query_light_state.lower();

    query_light_bright_num_to_string = str(query_light_bright);

    
    if query_air_state_low_cap == "on":
        
        print("Air-conditioner is on!");
        result = dweepy.dweet_for(link_air, {'status': 'on', 'temp': query_air_read_num_to_string});
        currentAirTimeStamp = result['created'];
        
        client = mqtt_client.Client(client_id);
        client.username_pw_set(mqtt_username, mqtt_password);
        client.connect(host, port);
        msg = currentAirTimeStamp + "_aircon_on" + query_air_read_num_to_string;
        result = client.publish(topic, msg);
        
    elif query_air_state_low_cap == "off":
        
        print("Air-conditioner is off!");
        result = dweepy.dweet_for(link_air, {'status': 'off', 'temp': '0'});
        currentAirTimeStamp = result['created'];
        
        client = mqtt_client.Client(client_id);
        client.username_pw_set(mqtt_username, mqtt_password);
        client.connect(host, port);
        msg = currentAirTimeStamp + "_aircon_of0";
        result = client.publish(topic, msg);
        
        

    if query_light_state_low_cap == "on":
    
        print("Light is on!");
        result = dweepy.dweet_for(link_light, {'status': 'on', 'brightness': query_light_bright_num_to_string});
        currentLightTimeStamp = result['created'];
        
        client = mqtt_client.Client(client_id);
        client.username_pw_set(mqtt_username, mqtt_password);
        client.connect(host, port);
        msg = currentLightTimeStamp + "_lights_on" + query_light_bright_num_to_string;
        result = client.publish(topic, msg);


    elif query_light_state_low_cap == "off":
        
        print("Light is off!");
        result = dweepy.dweet_for(link_light, {'status': 'off', 'brightness': '0'});
        currentLightTimeStamp = result['created'];
        
        client = mqtt_client.Client(client_id);
        client.username_pw_set(mqtt_username, mqtt_password);
        client.connect(host, port);
        msg = currentLightTimeStamp + "_lights_of0";
        result = client.publish(topic, msg);
        
        
        
    while True:
    
        latestDweetAir = dweepy.get_latest_dweet_for(link_air);
        latestDweetLight = dweepy.get_latest_dweet_for(link_light);
        
        latestDweetTimeStampAir = latestDweetAir[0]['created'];
        latestDweetTimeStampLight = latestDweetLight[0]['created'];
        
        for thing in latestDweetAir[0]['content']: #Check if there are changes to temperature | dweet link is https://dweet.io/dweet/for/4640D_air_con_sensor?temp={{NoteText}}
            if thing == "temp":
                query_air_read_num_to_string = str(latestDweetAir[0]['content']['temp']); 
                if query_air_read_num_to_string.isdigit():
                    currentAirTemp = "changed";
                else:
                    currentAirTemp = "not int";
            else:
                currentAirTemp = "unchanged";
        
        for thing in latestDweetLight[0]['content']: #Check if there are changes to brightness | dweet link is https://dweet.io/dweet/for/4640D_light_sensor?brightness={{NoteText}}
            if thing == "brightness":
                    query_light_bright_num_to_string = str(latestDweetLight[0]['content']['brightness']);
                    if query_light_bright_num_to_string.isdigit():
                        currentLightBrightness = "changed";
                    else:
                        currentLightBrightness = "not int";
            else:
                currentLightBrightness = "unchanged";
        
        if latestDweetTimeStampAir != currentAirTimeStamp: 
            
            currentAirTimeStamp = latestDweetTimeStampAir
            
            if currentAirTemp == "changed":
            
                if query_air_state == "off": #Change temperature but reading remains off
                    
                    client = mqtt_client.Client(client_id)
                    client.username_pw_set(mqtt_username, mqtt_password)
                    client.connect(host, port)
                    msg = latestDweetTimeStampAir + "_aircon_of0"
                    result = client.publish(topic, msg)
                    print(msg)
                    query_air_state = "off"
                
                elif query_air_state == "on": #Change temperature
                    
                    client = mqtt_client.Client(client_id)
                    client.username_pw_set(mqtt_username, mqtt_password)
                    client.connect(host, port)
                    msg = latestDweetTimeStampAir + "_aircon_on" + query_air_read_num_to_string
                    result = client.publish(topic, msg)
                    print(msg)
            
            elif currentAirTemp == "unchanged": 
                
                if query_air_state == "off":
                    
                    client = mqtt_client.Client(client_id)
                    client.username_pw_set(mqtt_username, mqtt_password)
                    client.connect(host, port)
                    msg = latestDweetTimeStampAir + "_aircon_on" + query_air_read_num_to_string
                    result = client.publish(topic, msg)
                    print(msg)
                    query_air_state = "on"
                    
                elif query_air_state == "on":
                    
                    client = mqtt_client.Client(client_id)
                    client.username_pw_set(mqtt_username, mqtt_password)
                    client.connect(host, port)
                    msg = latestDweetTimeStampAir + "_aircon_of0"
                    result = client.publish(topic, msg)
                    print(msg)
                    query_air_state = "off"
                
        time.sleep(1) 
        
        if latestDweetTimeStampLight != currentLightTimeStamp: 
            
            currentLightTimeStamp = latestDweetTimeStampLight
            
            if currentLightBrightness == "changed":
            
                if query_light_state == "off": #Change brightness but reading remains off
        
                    client = mqtt_client.Client(client_id)
                    client.username_pw_set(mqtt_username, mqtt_password)
                    client.connect(host, port)
                    msg = latestDweetTimeStampLight + "_lights_of0"
                    result = client.publish(topic, msg)
                    print(msg)
                    query_light_state = "off"
                    
                elif query_light_state == "on":
        
                    client = mqtt_client.Client(client_id)
                    client.username_pw_set(mqtt_username, mqtt_password)
                    client.connect(host, port)
                    msg = latestDweetTimeStampLight + "_lights_on" + query_light_bright_num_to_string
                    result = client.publish(topic, msg)
                    print(msg)
            
            elif currentLightBrightness == "unchanged":
                
                if query_light_state == "off": 
        
                    client = mqtt_client.Client(client_id)
                    client.username_pw_set(mqtt_username, mqtt_password)
                    client.connect(host, port)
                    msg = latestDweetTimeStampLight + "_lights_on" + query_light_bright_num_to_string
                    result = client.publish(topic, msg)
                    print(msg)
                    query_light_state = "on"
                    
                elif query_light_state == "on":
        
                    client = mqtt_client.Client(client_id)
                    client.username_pw_set(mqtt_username, mqtt_password)
                    client.connect(host, port)
                    msg = latestDweetTimeStampLight + "_lights_of0" 
                    result = client.publish(topic, msg)
                    print(msg)
                    query_light_state = "off"
        
    time.sleep(1)
