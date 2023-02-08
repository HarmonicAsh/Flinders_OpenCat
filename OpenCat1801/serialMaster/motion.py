def motion():
        dist = distance() #Need to add some form of error checking here!
        send(goodPorts,['kwkF',0.1],)
        while dist >= 24:
            dist = distance()
            print("Forwards...")
            print("Distance = ", dist, "cm")
            time.sleep(0.2)
        else:
            print("\nI am too close to something...")
            direction()

def direction():
        dist = distance() 
        send(goodPorts,['ksit',0.5],)  #Sit, then look straight ahead and measure the distance to the obstruction
        send(goodPorts,['i', [0, 0, 1, -30], 0.5],)
        print("\nThe obstruction is... ")
        print(dist, " cm in front")
        send(goodPorts,['i', [0, 50, 1, -38], 0.5],) #Look left and measure the distance to the obstruction
        dist_left = distance()
        print(dist_left, " cm to the left")
        send(goodPorts,['i', [0, -50, 1, -38], 0.5],) #Look right and measure the distance to the obstruction
        dist_right = distance()
        print(dist_right, " cm to the right")
        print("Time to find a way around this obstruction...")
        
        if dist_left < dist_right:      #When Nybble should deviate right
            time_mod = dist_left/dist_right
            print("Time factor (face left) = ", time_mod)
            time = 9*time_mod
            send(goodPorts,['kbkL',time],)
            #send(goodPorts,['kwkR',time],)
            motion()
        elif dist_left > dist_right:        #When Nybble should deviate ;eft   
            time_mod = dist_right/dist_left
            print("Time factor (face right) = ", time_mod)
            time = 9*time_mod
            send(goodPorts,['kbkR',time],)
            #send(goodPorts,['kwkL',time],)
            motion()
        else: #If the same reading is recorded (in case of error, should not be possible)
            print("These measurements don't make sense... sleeping now")
            send(goodPorts,['kbalance',2],)
            send(goodPorts,['krest',10],) 

