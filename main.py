#RATP
from datetime import datetime
import requests
import time

import locale
import signal
locale.setlocale(locale.LC_TIME,'') # temps en français

    #todo : see array with 1 element => pb ? 
    #todo, => departure time with delay (put base time + delay)
    #todo gui ?
    #todo : remove wieh displaying arrivals the first train stop in the  list of stops 
#way = "departures" 
way = "arrivals"
username = "db91d487-b783-4bd4-a78e-3df3cd675966" #SECRET ID
time = time.strftime("%Y%m%dT%H%M%S")
req = requests.get("https://api.sncf.com/v1/coverage/sncf/stop_areas/stop_area:SNCF:87713040/" + way + "?datetime=" + time, auth=(username, ""))
json = req.json()
train = json[way]
are_here = False
if(way == "departures"):
    are_here = False
else:
    are_here = True

for i in range(0, len(json[way])):
    link_journey = "https://api.sncf.com/v1/coverage/sncf/vehicle_journeys/" + train[i]['links'][1]['id']
    train_journey = requests.get(link_journey, auth=(username, "")).json()
    if(way == "departures"):
        print(train[i]['display_informations']['network'] + ' ' +  train[i]['display_informations']['direction'] + ' ' + train[i]['display_informations']['headsign'], end=" ")
    else:
        print(train[i]['display_informations']['network'] + ' ' +  train_journey['vehicle_journeys'][0]['stop_times'][0]['stop_point']['label'] + ' ' + train[i]['display_informations']['headsign'], end=" ")
    if(len(train_journey['disruptions']) > 0):
        retard = train_journey['disruptions']
        print("retard ", end="")
        for y in range(0, len(retard)):
            for x in range(0, len(retard[y]['messages'])):
                print(retard[y]['messages'][x]['text'], end=" ")
        print('|', end=" ")
    else:
        print('', end=": ")
    for j in range(0, len(train_journey['vehicle_journeys'][0]['stop_times']) - 1): # fix this for departures
        #print("debug", train_journey['vehicle_journeys'][0]['stop_times'][i]['stop_point']['name'])
        if( train_journey['vehicle_journeys'][0]['stop_times'][j]['stop_point']['name']  == 'Dijon' and way == "arrivals"):
            are_here = False
        if(are_here == True):
            if(train_journey['vehicle_journeys'][0]['stop_times'][j]['skipped_stop'] == True):
                print("SKIPPED", end="|")
            print(train_journey['vehicle_journeys'][0]['stop_times'][j]['stop_point']['label'], end=" - ")
        if( train_journey['vehicle_journeys'][0]['stop_times'][j]['stop_point']['name']  == 'Dijon' and way == "departures"):
            are_here = True
        
    if(way == "departures"):
       are_here = False
    else:
        are_here = True
    if(way == "departures"):
        time = datetime.strptime(train[i]['stop_date_time']['departure_date_time'], "%Y%m%dT%H%M%S")
        print("départ :", time.strftime("%H:%M"), end="")
    else:
        time = datetime.strptime(train[i]['stop_date_time']['arrival_date_time'], "%Y%m%dT%H%M%S")
        print("arrivée :", time.strftime("%H:%M"), end="")
    print('')
    
    
