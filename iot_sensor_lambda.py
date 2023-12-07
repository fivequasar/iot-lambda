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

    host = "52.74.129.244"; # broker's ip
    
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
        
        if latestDweetTimeStampAir != currentAirTimeStamp: 
            
            currentAirTimeStamp = latestDweetTimeStampAir
            
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
