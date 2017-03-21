from Connections import Connection
from AutoScaling import autoScaling


class autoscaling:
    def __init__(self):
        ''' Autoscaling Instance Constructor '''
    def displayMenu(self):
        print("**** Cloud Computing ****")
        print("Choose Option:")
        print("")
        print("1. List existing autoScale groups")
        print("2. List existing launch configurations")
        print("3. Create launch configurations ")
        print("4. Create group ")
        print("5. Set up upscale")
        print("6. Set up downscale")
        print("")
        choice = input("Choose Option: ")

        if choice == 1:
            conn = Connection()
            asConn = conn.autoscalingConnection()
            autos = autoScaling()
            autos.viewAllGroups(asConn)
            autoscaling.displayMenu(self)
        if choice == 2:
            conn = Connection()
            asConn = conn.autoscalingConnection()
            autos = autoScaling()
            autos.viewLaunchConfigs(asConn)
            autoscaling.displayMenu(self)
        if choice == 3:
            conn = Connection()
            asConn = conn.autoscalingConnection()
            autos = autoScaling()
            autos.createLaunchConfig(asConn)
            autoscaling.displayMenu(self)
        if choice == 4:
            conn = Connection()
            asConn = conn.autoscalingConnection()
            autos = autoScaling()
            autos.createGroup(asConn)
            autoscaling.displayMenu(self)

        if choice == 5:
            conn = Connection()
            asConn = conn.autoscalingConnection()
            cw2Conn = conn.cwConnection()
            autos = autoScaling()
            autos.createScaleUpForGroup(asConn,cw2Conn)
            autoscaling.displayMenu(self)
        if choice == 6:
            conn = Connection()
            asConn = conn.autoscalingConnection()
            cw2Conn = conn.cwConnection()
            autos = autoScaling()
            autos.createScaleDownForGroup(asConn,cw2Conn)
            autoscaling.displayMenu(self)



