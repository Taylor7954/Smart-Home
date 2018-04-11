import random

class algorithms:

    count = 0                                # Running total to keep up with the amount of Ccfs used in a month.
    Interior_Temp                            # Establishing an initial interior temp.
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
        global total_gallons
        global Ccf
        global count
        total_gallons += gallons                    # Increase total_gallons amount in database.
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

    # This method is used to create the temperature variation that occurs simply because
    # the HVAC is on. It doesn't matter if the door is open or not.
    def HVAC_Run(HVAC, Interior_Temp):              # HVAC is a boolean value. True = on, False = off.
        rand = random.randint(0,100000)             # Random number to create variance in temp while HVAC runs.
        if HVAC == True and rand < 5:               # Maybe random range can be decreased due to less frequent calls?
            Interior_Temp += 1
        elif HVAC == True and rand > 99995:
            Interior_Temp -= 1
        return Interior_Temp

    # Not sure how door events are going to be handled, but this method just adjusts
    # the internal temp based on external temp. In the simulation that I built to 
    # test it, a number was being randomized each minute and this method called inside of a loop, and if the random
    # number was the same for five consecutive minutes, the temp changed by calling
    # this method. This method can be used for if the door is open, closed, or if a 
    # window is open or closed.
    def InTempChange_Door(Interior_Temp, Current_ExTemp):                 # Current_ExTemp needs to come from database.
        if ((Interior_Temp - Current_ExTemp) >= 10):
            Interior_Temp -= 2                                            # External temp is less than internal temp by 10. Subtract.
        elif ((Interior_Temp - Current_ExTemp) <= -10):
            Interior_Temp += 2                                            # External temp is greater than internal temp by 10. Add.