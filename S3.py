from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
import sys

class S3:
    def __init__(self):
		''' Volumes Constructor '''

    #def create_bucket(self, conn):
    #  bucket = conn.create_bucket('mynew2016bucket')

    #DONE
    def checkBucket(self, conn, bucketName):
        buckets = conn.get_all_buckets()
        bucketsFound = False
        for b in buckets:
            if bucketName in b.name:
                bucketsFound = True

        return bucketsFound

    def checkFileExistAlready(self,conn,bucketName, fileName):
        fileFound = False
        bucket = conn.get_bucket(bucketName)
        for key in bucket.list():
            if fileName in key.name:
                fileFound = True
        return fileFound



    #DONE
    def list_buckets(self,conn):
        print("")
        buckets = conn.get_all_buckets()
        bucketsFound = False
        for b in buckets:
            bucketsFound = True
            print b.name
            #print b.__dict__
        print("")
        if bucketsFound == False:
            print("No buckets found")




    def list_object_in_pucket(self,conn, bucketName):
        print("")
        #buckets = conn.get_all_buckets()
        #bucketsFound = False
        #for b in buckets:
        #    if bucketName in b.name:
        #        bucketsFound = True
        bucketFound = self.checkBucket(conn, bucketName)
        if bucketFound == False:
            print("No buckets found")
        else:
            print("Objects in " + bucketName + ": " )
            bucket = conn.get_bucket(bucketName)

            bucketsFound = False
            for key in bucket.list():
               print key.name
               #print key.__dict__
               #print key.name.encode('utf-8')

               bucketsFound = True

            if bucketsFound == False:
                print("Bucket name " + "'" + bucketName + "'" + ' not found.' )
        print ("")


    def upload_file(self,conn):
        pathExists = False
        bucketName= raw_input("Please enter bucket name: ")
        bucketFound = self.checkBucket(conn,bucketName)
        if bucketFound == True:
            keyName= raw_input("Enter name of file: ")
            fileFound = self.checkFileExistAlready(conn,bucketName,keyName)
            if fileFound == False:
                filePath= raw_input("Please path of file you want to upload: ")
                pathExists = (os.path.exists(filePath))
                pathDirectory =(os.path.isdir(filePath))
            else:
                print("File " + keyName + " already exists.")
        else:
            print ("Bucket not found.")



        if pathExists == True and pathDirectory == False:
            buckets = conn.get_all_buckets()
            for b in buckets:
                if b.name == bucketName:
                    k = Key(b)
                    k.key = keyName
                    k.set_contents_from_filename(filePath)
        else:
            print("File path doesnt exist or is a directory.")

    def downloadFile(self,conn):
        pathExists = False
        bucketName= raw_input("Please enter bucket name: ")
        bucketFound = self.checkBucket(conn,bucketName)
        if bucketFound == True:
            keyName= raw_input("Enter you file want to download: ")
            fileFound = self.checkFileExistAlready(conn,bucketName,keyName)
            if fileFound == True:
                filePath= raw_input("Please path where the file will be save to: ")
                pathExists = (os.path.exists(filePath))
                pathDirectory =(os.path.isdir(filePath))
            else:
                print("File " + keyName + " doesnt exists.")
        else:
            print ("Bucket not found.")


        if pathExists == True and pathDirectory == True:
            #Tried tp use get_bucket using the bucket entered but returned null
            #bucket = conn.get_bucket(bucketName)
            buckets = conn.get_all_buckets()
            for b in buckets:
                if b.name == bucketName:
                    for l in b:
                        if keyName == l.key:
                            print("Getting file...")
                            if not os.path.exists(filePath+l.key):
                                l.get_contents_to_filename(filePath+l.key)
                            else:
                                print("File the file " + l.key + "  already exists in " + filePath +" .")



    def delete_object_(self,conn):
        confirmation = "n"
        bucketName= raw_input("Please enter bucket name: ")
        bucketFound = self.checkBucket(conn,bucketName)
        if bucketFound == True:
            keyName= raw_input("Enter name of file you want to delete: ")
            fileFound = self.checkFileExistAlready(conn,bucketName,keyName)
            if fileFound:
              #  confirmation = None
               # while confirmation is not "y" and confirmation is not "Y" and confirmation is not "n" and confirmation is not "n":
                confirmation= raw_input("Are you sure you want to remove " + keyName  + " :(y/n) ")

            else:
                print("File " + keyName + " doesnt exists.")

        else:
            print ("Bucket not found.")

        if confirmation == "y" or confirmation == "Y":
            buckets = conn.get_all_buckets()
            for b in buckets:
                if b.name == bucketName:
                    for l in b:
                        if keyName == l.key:
                             k = Key(b)
                             k.key = keyName
                             b.delete_key(k)
                             print (keyName + " deleted.")