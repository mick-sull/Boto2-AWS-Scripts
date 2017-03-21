import os
from Connections import Connection
from S3 import S3
from Openstack import openstack

class storage:
    def __init__(self):
        ''' S3 Instance Constructor '''
    def displayMenu(self):
        os.system('cls')
        print("**** Storage ****")
        print("")
        print("1. AWS")
        print("2. Openstack")
        print("")
        choice = input("Choose Option: ")
        if choice == 1:
            self.displayAWSMenu()
        elif choice == 2:
            self.displayOpenstackMenu()
        else:
            print "Invalid option..."
            storage.displayMenu(self)

    def displayOpenstackMenu(self):
        os.system('cls')
        print("**** Openstack ****")
        print("")
        print("1. List all volumes")
        print("")
        choice = input("Choose Option: ")
        if choice == 1:
            conn = Connection()
            driver = conn.openstackConnection()
            openS = openstack()
            openS.displayVolumes(driver)
            storage.displayMenu(self)


    def displayAWSMenu(self):
        os.system('cls')
        print("**** AWS ****")
        print("")
        print("1. List all buckets")
        print("2. List all objects in a bucket")
        print("3. Upload an object")
        print("4. Download an object")
        print("5. Delete an object")
        print("")
        choice = input("Choose Option: ")

        if choice == 1:
            conn = Connection()
            s3Con = conn.s3Connection()
            listBuckets = S3()
            listBuckets.list_buckets(s3Con)
            storage.displayMenu(self)
        #List all objects in a bucket
        if choice == 2:
            os.system('cls')
            conn = Connection()
            s3Con = conn.s3Connection()
            bucketName= raw_input("Please enter bucket name: ")
            s3 = S3()
            s3.list_object_in_pucket(s3Con, bucketName)
            storage.displayMenu(self)
        # Upload an object
        if choice == 3:
            os.system('cls')
            conn = Connection()
            s3Con = conn.s3Connection()
            s3 = S3()
            s3.upload_file(s3Con)
            storage.displayMenu(self)

        if choice == 4:
            os.system('cls')
            conn = Connection()
            s3Con = conn.s3Connection()
            s3 = S3()
            s3.downloadFile(s3Con)
            storage.displayMenu(self)

        if choice == 5:
            os.system('cls')
            conn = Connection()
            s3Con = conn.s3Connection()
            s3 = S3()
            s3.delete_object_(s3Con)
            storage.displayMenu(self)