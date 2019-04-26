import numpy as np
import pandas as pd

"""
Initial conditions
"""
shed = dict();
drier = dict();
wet_silo = dict();
source = dict();

shed.update({
    "name"         : "shed",
    "contents"     : 0, #tn
    "max_contents" : 14000, #tn
    "transfer_rate": 4.167, #tn/min 250tn/hr
    "prev"         : drier,
    "next"         : None
})

drier.update({
    "name"         : "drier",
    "contents"     : 0, #tn
    "max_contents" : 0.5, #tn
    "transfer_rate": 0.5, #tn/min 250tn/hr
    "prev"         : wet_silo,
    "next"         : shed
})

wet_silo.update({
    "name"         : "wet_silo",
    "contents"     : 0, #tn
    "max_contents" : 250, #tn
    "transfer_rate": 4.167, #tn/min 250tn/hr
    "prev"         : source,
    "next"         : drier
})

source.update({
    "name"         : "source",
    "contents"     : 30, #tn
    "max_contents" : np.inf, #tn, inf because this number represents the ammount that has to be stored elsewhere
    "transfer_rate": 4.167, #tn/min 250tn/hr
    "prev"         : None,
    "next"         : wet_silo
})

"""
Setup initial conditions for simulation
"""
time = 0
time_max = 600 #minutes
delivery_time = 20 #minutes
data_dict = {
    "time":[],
    "source_contents":[],
    "wet_silo_contents":[],
    "drier_contents":[],
    "shed_contents":[]
}
data = pd.DataFrame(data_dict)

"""
Iterate backwards through the equipment chain, do the transfers
"""
while (time <= time_max):

    #Work out if to add more to the source
    if time > 0:
        if time % delivery_time == 0:
            source["contents"] = source["contents"] + 30.0

    active = shed #start with the shed

    while active is not None: #go back to the head of the chain
        if active["next"] is not None: #tail of the chain is a sink
            #Figure out how much to transfer
            transfer = active["transfer_rate"]
            #If current store is nearly empty, only transfer the last bit
            if (transfer > active["contents"]):
                transfer = active["contents"]
            #If the receiver is nearly full, don't overfill
            if (transfer > (active["next"]["max_contents"] - active["next"]["contents"])):
                transfer = active["next"]["max_contents"] - active["next"]["contents"]

            #Do the transfers
            active["contents"] = active["contents"] - transfer
            active["next"]["contents"] = active["next"]["contents"] +transfer
        active = active["prev"] #Move to next

    #Build the data table and append
    data_dict["time"] = time
    data_dict["source_contents"] = source["contents"]
    data_dict["wet_silo_contents"] = wet_silo["contents"]
    data_dict["drier_contents"] = drier["contents"]
    data_dict["shed_contents"] = shed["contents"]
    temp = pd.DataFrame(data_dict, index=[0])
    data = data.append(temp)

    time = time + 1 #Iterate time

"""
Do something with the data, like export to Excel
"""
data.to_excel('data_out.xlsx')
