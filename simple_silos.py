import json
import numpy as np
import pandas as pd

def get_destination(unit,equipment_dict):
    """
    Determine the destination of the grain packet. Quantity to be transfered is
    determined during the transfer function. This function only determines where
    it should go.
    """
    print(unit["name"])
    dest_str = None
    if unit["is_node"]:
        decision = unit["decision"]
        choice_ct = len(unit["value"])-1
        if unit[decision]<unit["value"][0]: #Lower than lowest threshold
            print('node:lo')
            dest_str = unit["next"][0]
        elif unit[decision]>unit["value"][choice_ct]: #Higher than highest threshold
            print('node:hi')
            dest_str = unit["next"][choice_ct+1]
        else: #Somewhere inbetween the min and max thresholds, check the indexing
            print('node:var')
            for ct in range(choice_ct-1):
                if unit[decision]>=unit["value"][ct] and unit[decision]<=unit["value"][ct+1]:
                    print('node:'+str(ct+1))
                    dest_str = unit["next"][ct+1]
    elif unit["is_sink"]:
        dest_str = None
    else:
        dest_str = unit["next"]

    if dest_str is not None:
        destination = equipment_dict[dest_str]
    else:
        return None

    return destination['name']

def do_transfers(ledger, equipment_dict, cycle_max=3):
    """
    Enact transfers and a calculate new moisture contents.
    In the case of a destination that is full, do nothing
    Returns True if all the transfers worked, false if not.
    """
    for count in range(cycle_max):
        for idx,entry in enumerate(ledger):
            origin = equipment_dict[entry[0]]
            destination = equipment_dict[entry[1]]
            good_transfer = False

            if origin["contents"] <= 0:
                """
                Origin is empty
                """
                print('dt:orig empty')
                quantity = 0
                good_transfer = False
                ledger.pop(idx)
            elif (destination["max_contents"]-destination["contents"]) <= 0:
                """
                Destination is full.
                """
                print('dt:dest full')
                good_transfer = False
            elif (destination["max_contents"]-destination["contents"]) < source["transfer_rate"]:
                """
                Destination is nearly full, fill up the destination
                """
                print("dt:dest near full")
                quantity = destination["max_contents"]-destination["contents"]
                good_transfer = True
            elif origin["contents"] < source["transfer_rate"]:
                """
                Origin is nearly empty, take the last bit of grain
                """
                print('dt:orig near empty')
                quantity = origin["contents"]
                good_transfer = True
            else:
                """
                Normal transfer, quantity is fine
                """
                print('dt:norm')
                quantity = source["transfer_rate"]
                good_transfer = True

            if good_transfer:
                """
                This is a valid transfer so do all the math. Otherwise do
                nothing and wait for the next pass through.
                """
                print("dt:transfer")
                print("dt:"+str(quantity))
                total_mass = destination["contents"]+quantity
                transfer_water = origin["moisture"] * quantity
                destination_water = destination["moisture"] * destination["contents"]
                new_moisture = (destination_water + transfer_water)/total_mass
                destination["contents"] = total_mass
                origin["contents"] = origin["contents"] - quantity
                if destination["is_drier"]:
                    """
                    Driers dry to their default dryness
                    """
                    destination["moisture"] = destination["moisture"]
                else:
                    """
                    Everything else is mass averaged
                    """
                    destination["moisture"] = new_moisture
                ledger.pop(idx)
        print("***")

    """
    A handy little snippet to indicate whether all the transfers suceeded or not.
    """
    if len(ledger) is 0:
        return True
    else:
        return False

def do_delivery(source, time, delivery_schedule):
    """
    Work out if a delivery should be done, and the moisture properties of the
    delivery. Assumes that times in the schedules are repeated (i.e. use modulo
    of time against time_max in schedule.)

    Delivery times are discrete minute of cycles that deliveries will occur,
    with the ammount to be delivered.

    Moisture schedule is a piece-wise continuous set of polynomials defining the
    moisture content at any time of the day.
    """

    len_delivery = len(delivery_schedule[0])
    cyclic_delivery_time = time % delivery_schedule[0][len_delivery-1]

    poly = []
    delivery_moisture = 0

    if cyclic_delivery_time in delivery_schedule[0]:
        """
        Work out delivery quantity and moisture
        """
        idx = delivery_schedule[0].index(cyclic_delivery_time)
        delivery_quantity = delivery_schedule[1][idx]
        delivery_moisture = delivery_schedule[2][idx]

        """
        Put delivery quantity in source, work out the new moisture
        """
        old_water = source["moisture"] * source["contents"]
        source["contents"] = source["contents"] + delivery_quantity
        if source["contents"]>0:
            source["moisture"] = (old_water + delivery_moisture * delivery_quantity)/source["contents"]
        else:
            source["moisture"] = 0;


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
Load equipment and their initial conditions from a json.
"""
fi_name = "silo_set.json"
with open(fi_name,"r") as fido:
    model = json.load(fido)
equipment = model["equipment"];
equipment_names = [x['name'] for x in equipment]

#Useful to know which one is the source explicitly, also build a dict of equipment
source_idx = [x['is_source'] for x in equipment].index(True)
source = equipment[source_idx]
equipment_dict = dict(zip(equipment_names,equipment))

"""
Setup initial conditions for simulation
"""
time = 0
time_max = 48*60 #minutes
delivery_schedule = model["delivery_schedule"]

"""
Build data collectors
"""
data_dict = {"time":[],"ledger_start":[],"ledger_end":[]}
for unit in equipment:
    entry_name = unit["name"]+"_contents"
    data_dict.update({entry_name:[]})
    entry_name = unit["name"]+"_moisture"
    data_dict.update({entry_name:[]})
data = pd.DataFrame(data_dict)

"""
Iterate through the equipment chain, do the transfers
"""
while (time <= time_max):

    ledger = []

    """
    Work out the transfer ledger, execute all the transfers.
    """
    for unit in equipment:
        origin = unit['name']
        destination = get_destination(unit, equipment_dict)
        entry = (origin,destination)
        if destination is None:
            pass
        else:
            ledger.append(entry)
    print("<"+str(time)+">"+str(ledger))
    data_dict["ledger_start"] = str(ledger)
    #Execute transfers and deliveries
    truth = do_transfers(ledger, equipment_dict)
    do_delivery(source, time, delivery_schedule)
    print(truth)
    time = time + 1 #Iterate time
    print("<<##>>")

    """
    Build the data table and append
    Do all this at the start or end of the time frame?
    """
    data_dict["time"] = time
    data_dict["ledger_end"] = str(ledger)
    for unit in equipment:
        data_dict[unit["name"]+"_contents"] = unit["contents"]
        data_dict[unit["name"]+"_moisture"] = unit["moisture"]
    temp = pd.DataFrame(data_dict, index=[0])
    data = data.append(temp)

"""
Do something with the data, like export to Excel
"""
data.to_excel('data_out.xlsx')
