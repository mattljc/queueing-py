import json
import numpy as np
import pandas as pd

"""
Load equipment and their initial conditions from a json.
"""
fi_name = "silo_set.json"
fi_do = open(fi_name,"r")
equipment = json.load(fi_do)["equipment"];

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
Iterate through the equipment chain, do the transfers
"""
while (time <= time_max):

    #Build the data table and append
    #Do all this at the start of the time frame
    data_dict["time"] = time
    data_dict["source_contents"] = source["contents"]
    data_dict["wet_silo_contents"] = wet_silo["contents"]
    data_dict["drier_contents"] = drier["contents"]
    data_dict["shed_contents"] = shed["contents"]
    temp = pd.DataFrame(data_dict, index=[0])
    data = data.append(temp)

    active = equipment["source"]

    while not active["is_sink"]:
        #Figure out how much to transfer
        #Work out where to transfer to
        #Do the transfer
        #Calculate the new destination moisture
        #Go to destination


    # while active is not None: #go back to the head of the chain
    #     if active["next"] is not None: #tail of the chain is a sink
    #         #Figure out how much to transfer
    #         transfer = active["transfer_rate"]
    #         #If current store is nearly empty, only transfer the last bit
    #         if (transfer > active["contents"]):
    #             transfer = active["contents"]
    #         #If the receiver is nearly full, don't overfill
    #         if (transfer > (active["next"]["max_contents"] - active["next"]["contents"])):
    #             transfer = active["next"]["max_contents"] - active["next"]["contents"]
    #
    #         #Do the transfers
    #         active["contents"] = active["contents"] - transfer
    #         active["next"]["contents"] = active["next"]["contents"] +transfer
    #     active = active["next"] #Move to next
    #
    # #Work out if to add more to the source
    # if time > 0:
    #     if time % delivery_time == 0:
    #         source["contents"] = source["contents"] + 30.0

    time = time + 1 #Iterate time

"""
Do something with the data, like export to Excel
"""
data.to_excel('data_out.xlsx')

## TODO:
# def action_node switch destination based on incoming property
# def action_drier build into moisture model
# def delivery with moisture variation
