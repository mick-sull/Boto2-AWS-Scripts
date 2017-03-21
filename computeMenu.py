import boto.ec2
from EC2 import EC2Instance
from Openstack import openstack
#from MainMenu import mainmenu

import boto
from Connections import Connection
import numbers

class compute:
    def __init__(self):
        ''' EC2Instance Constructor '''

    def displayComputeMenu(self):
        print ("*** Compute ***")
        print ("")
        print("1. AWS")
        print("2. Openstack")
        print("0. Return to previous menu")
        print("")
        choice = input("Choose Option: ")

        if choice == 1:
            self.displayAWSMenu()
        elif choice == 2:
            compute.displayMenu(self)
        elif choice == 0:
            print("Returning...")
            #main = mainmenu()
            #main.displayMainMenu()



    def displayAWSComputeMenu(self):
        print ("AWS")
        print ("")
        print("1. List all running instances")
        print("2. View instance by instance ID")
        print("3. Start new instance using existing AMI")
        print("4. Stop all instances")
        print("5. Stop instance by entering instance ID")
        print("6. Attach volume to instance")
        print("7. Detach volume from instance")
        print("8. Launch a new instance")
        print("0. Return to previous menu")
        print("")
        choice = input("Choose Option: ")
        # #if(isinstance(choice, numbers.Integral)):
        # if(choice.isdigit):
        if choice == 1:
            conn = Connection()
            ec2Con = conn.ec2Connection()
            #Get running instances
            listIn = EC2Instance()
            listIn.list_instances(ec2Con)
            compute.displayMenu(self)
        elif choice == 2:
            conn = Connection()
            ec2Con = conn.ec2Connection()
            print("")
            insID= raw_input("Please enter instance ID: ")
            findInstance = EC2Instance()
            findInstance.viewInstance(ec2Con,insID)
            compute.displayMenu(self)
        elif choice == 3:
            conn = Connection()
            ec2Con = conn.ec2Connection()
            print("")
            startInsance = EC2Instance()
            startInsance.start_instance(ec2Con)
            compute.displayMenu(self)
        elif choice == 4:
            conn = Connection()
            ec2Con = conn.ec2Connection()
            print("")
            stopAllInstances = EC2Instance()
            stopAllInstances.stop_all_instance(ec2Con)
            compute.displayMenu(self)
        elif choice == 5:
            conn = Connection()
            ec2Con = conn.ec2Connection()
            print("")
            insID= raw_input("Please enter instance ID you want to stop: ")
            stopInstanceByID = EC2Instance()
            stopInstanceByID.stop_instance_by_id(ec2Con,insID)
            compute.displayMenu(self)
        elif choice == 6:
            conn = Connection()
            ec2Con = conn.ec2Connection()
            attachVol = EC2Instance()
            inst = raw_input("Please enter the instance ID: ")
            volID= raw_input("Please enter the volume ID you want to attach to '" + inst +"': " )
            device = raw_input("Please enter device: ")
            attachVol.attachVolume(ec2Con, volID,inst, device)
            #print found
            compute.displayMenu(self)
        elif choice == 7:
            conn = Connection()
            ec2Con = conn.ec2Connection()
            detach = EC2Instance()
            volumeID= raw_input("Please enter volume ID you want to detach: " )
            detach.detachVolume(ec2Con,volumeID)
            compute.displayMenu(self)
        elif choice == 8:
            conn = Connection()
            ec2Con = conn.ec2Connection()
            createInstance = EC2Instance()
            instanceType= raw_input("Please enter free tier OS(windows/linux): " )
            while instanceType != "windows" and instanceType != "linux":
                print(instanceType + " is not a valid operating sytem.")
                instanceType= raw_input("Please enter free tier OS(windows/linux): " )
            createInstance.createInstance(ec2Con,instanceType)
        elif choice == 0:
            print("Returning...")
            self.displayMenu()
        else:
            print("Invalid option....")
            compute.displayMenu(self)


    def displayOpenstackComputeMenu(self):
        print ("*** Compute ***")
        print ("")
        print("OpenStack")
        print("")
        print("1. List All Running Instances")
        print("0. Return to previous menu")
        print("")
        choice = input("Choose Option: ")
        if choice == 1:
            conn = Connection()
            driver = conn.openstackConnection()
            openS = openstack()
            openS.listRunningInt(driver)
        elif choice == 0:
            print("Returning...")
            self.displayMenu()


