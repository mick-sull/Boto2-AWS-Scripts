from Monitoring import monitoring
from computeMenu import compute
from storageMenu import storage
from AutoscalingMenu import autoScaling
import os
class mainmenu:
        def __init__(self):
            ''' EC2Instance Constructor '''
            self.displayMainMenu()

        def displayMainMenu(self):
            print("**** Cloud Computing ****")
            print("Choose Option:")
            print("")
            print("1. Compute")
            print("2. Storage")
            print("3. Monitoring")
            print("4. Autoscaling")
            print("5. ")
            print("")
            choice = input("Choose Option: ")

            if choice == 1:
                #print("Opening AWS....")
                os.system('cls')
                awsMenu = compute()
                awsMenu.displayMenu()

            if choice == 2:
                os.system('cls')
                s3Menu = storage()
                s3Menu.displayMenu()
            if choice == 3:
                os.system('cls')
                cloudwatch = monitoring()
                cloudwatch.displayMenu()
            if choice == 4:
                os.system('cls')
                autoscaling = autoScaling()
                autoscaling.displayMenu()





