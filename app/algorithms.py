
import random


count = 0  # Running total to keep up with the number of Ccfs used in a month.
# Interior_Temp                            # Establishing an initial interior temp.
Ccf = 748                                # 748 gallons make a Ccf.
HVAC = False
Total_Electric_Bill = 0.0               # Running total of electricity bill

def electricity(watts, minutes):
    flat_rate = 0.12                            # flat rate provided in assignment
    kilowatts = (watts/1000)                    # convert watts to kilowatts
    hours_of_operation = (minutes/60)           # determine hours of operation
    kWh = (kilowatts * hours_of_operation)      # determine kilowatt hours
    cost = (flat_rate * kWh)                    # final cost for length of time that device is running. NOT FINAL MONTHLY BILL
    Total_Electric_Bill += cost
    return cost

def water_usage(gallons):                       # Receive gallons used by device.
    # global total_gallons
    # global Ccf
    # global count
    total_gallons += gallons                    # Increase total_gallons number in database.
    if total_gallons == Ccf:                    
        Ccf += 748                               # Increase Ccf each time to raise the cap for the next iteration.
        count += 1


# This method calculates the total water bill for the month based on the amount of Ccfs used
def water_calc(count):
    base_charge = 34.48                         # Base charge for a 3/4 inch connection in B'ham.
    Ccf_charge = 0                              # This number will vary depending on monthly usage.

    # This if/elif statement changes the amount charged for Ccf depending on how many are used in a month.
    if count <= 3:                              
        Ccf_charge = 2.43
    elif count >= 4 and count <= 15:
        Ccf_charge = 2.87
    elif count > 15:
        Ccf_charge = 4.29
    
    volume_charge = count * Ccf_charge
    total_payment = volume_charge + base_charge
    return total_payment

def HVAC_Run(HVAC, Interior_Temp):              # HVAC is a boolean value. True = on, False = off.
    rand = random.randint(0,100000)             # Random number to create variance in temp while HVAC runs.
    if HVAC == True and rand < 5:               # Maybe random range can be decreased due to less frequent calls?
        Interior_Temp += 1
    elif HVAC == True and rand > 99995:
        Interior_Temp -= 1
    return Interior_Temp