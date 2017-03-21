import os
from Connections import Connection
from S3 import S3
from CloudWatch import CloudWatch


class monitoring:
    def __init__(self):
        ''' S3 Instance Constructor '''
    def displayMenu(self):
        print("**** Cloud Computing ****")
        print("Choose Option:")
        print("")
        print("1. Display all default performance metrics for EC2 Instance")
        print("2. Create alarm")
        print("")
        choice = input("Choose Option: ")

        if choice == 1:
            conn = Connection()
            ec2Con = conn.ec2Connection()
            cwConn = conn.cwConnection()
            cloudwatch = CloudWatch()
            cloudwatch.query_cw(ec2Con, cwConn)
            monitoring.displayMenu(self)
        if choice == 2:
            conn = Connection()
            sns = conn.snsConnection()
            ec2Con = conn.ec2Connection()
            cw = conn.cwConnection()
            ses = conn.sesConnection()
            cloudwatchAlert = CloudWatch()
            cloudwatchAlert.cw_alarm(ec2Con,sns,cw, ses)
            monitoring.displayMenu(self)
            #List all objects in a bucket