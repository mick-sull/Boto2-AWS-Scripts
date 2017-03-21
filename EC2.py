import boto.ec2


class EC2Instance:
    def __init__(self):
        ''' EC2Instance Constructor '''

    def list_instances(self, conn):
        ''' List EC2 Instances '''
        # get all instance reservations associated with this AWS account
        reservations = conn.get_all_reservations()

        x = 0
        # loop through reservations and extract instance information
        for r in reservations:
            # get all instances from the reservation
            instances = r.instances
            # loop through instances and print instance information

            for i in instances:

                # get instance name from the tags object
                #print i.__dict__

                tags = i.tags
                instancename = 'Default EC2 Instance Name'

                if 'running'  in i.state:
                    # print instance information
                #    print i, ':' , 'Instance Name:', instancename, ' Instance Id:', i.id, ' State:', i.state, 'Launch Time: ', i.launch_time, 'IP ADDRESS', i.ip_address
                    print x,':',i.id,'-',i.instance_type,'<',i.region,'>',' <Running since:',i.launch_time,'>'
                    print ("")
                    x += 1


    def viewInstance(self, conn, instanceID):
        ''' View details of instance from instance ID entered by user'''
        # get all instance reservations associated with this AWS account
        reservations = conn.get_all_reservations()

        foundInstance = False
        # loop through reservations and extract instance information
        for r in reservations:
            # get all instances from the reservation
            instances = r.instances
            # loop through instances and print instance information
            for i in instances:
                tags = i.tags

                # check for Name property in tags object
                if instanceID in i.id:
                     print i.id,'-',i.instance_type,'<',i.region,'>',' <Running since:',i.launch_time,'>'
                     foundInstance = True
        if foundInstance == False:
            print("Instance ID " + "'" + instanceID + "'" + ' not found.' )


#--------------NEEDS TO LOOKED AT--------------------------------
    def start_instance(self, conn):



        ''' Starts a stopped instance '''
                # get all instance reservations associated with this AWS account
        reservations = conn.get_all_reservations()

        foundInstance = False
        # loop through reservations and extract instance information
        for r in reservations:
            # get all instances from the reservation
            instances = r.instances
            # loop through instances and print instance information
            x = 0
            amiList =[]
            keyNameList = []
            instanceTypeList =[]
            for i in instances:
                tags = i.tags

                # check for Name property in tags object
                if 'running' not in i.state:
                     foundInstance = True
                     print ("ID:",x,  " - ", i.image_id)

                     amiList.insert(x, i.image_id)
                     keyNameList.insert(x,i.key_name)
                     instanceTypeList.insert(x, i.instance_type)
                     x += 1
                     print ("X: ", x)

        print ("LIST SIZE: ", len(amiList))
        for r in keyNameList:
            print r
        if foundInstance == False:
            print("No ami availible")
        else:
            print("")
            for r in keyNameList:
                print r
          #  amiChosen = input("Please enter the ID of the ami you would like to start: ")
          #  reservation = conn.run_instances(amiList[amiChosen], keyNameList[amiChosen],instanceTypeList[amiChosen])


    def stop_all_instance(self, conn):
        ''' Stops all running instances'''
        conn.stop_all()

    def stop_instance_by_id(self, conn, instanceID):
        ''' Stops a running instance by ID'''
        validInstance  =EC2Instance()
        foundInstance = validInstance.checkInstance(conn,instanceID)
        # reservations = conn.get_all_reservations()
        # foundInstance = False
        # # loop through reservations and extract instance information
        # for r in reservations:
        #     # get all instances from the reservation
        #     instances = r.instances
        #     # loop through instances and print instance information
        #     for i in instances:
        #         tags = i.tags
        #
        #         # check for Name property in tags object
        #         if instanceID in i.id:
        #              foundInstance = True
        if foundInstance == False:
            print("Instance ID " + "'" + instanceID + "'" + ' not found.' )
            print("Try Again")
        else:
            print ("Stopping instance " + "'" + instanceID +"'")
            conn.stop_instances(instanceID)
            #EC2Instance.list_instances(conn)

    def checkInstance(self,conn,instanceID):
        reservations = conn.get_all_reservations()
        foundInstance = False
        # loop through reservations and extract instance information
        for r in reservations:
            # get all instances from the reservation
            instances = r.instances
            # loop through instances and print instance information
            for i in instances:
                tags = i.tags

                # check for Name property in tags object
                if instanceID in i.id:
                     foundInstance = True
        if foundInstance == False:
            print("Instance ID " + "'" + instanceID + "'" + ' not found.' )
            print("Try Again")
        return foundInstance

    def checkVolumeAvailible(self,conn, volID):
            vols = conn.get_all_volumes()
            found = False
            if vols:
                for v in vols:
                    if volID in v.id and 'available' in v.status:
                        found = True
                    if volID in v.id and 'in-use' in v.status:
                        choice = raw_input(v.id  + " volume in-use. Would you like to detach volume(y/n): ")

            if found == False:
             print("Volume ID " + "'" + volID + "'" + ' not found or in-use.' )
             print("Try Again")
            return found

    def attachVolume(self,conn,volID, instanceID, device):
        # volAvail  =EC2Instance()
        # volResult = volAvail.checkVolumeAvailible(conn,volID)
        # validInstance  =EC2Instance()
        # foundInstance = validInstance.checkInstance(conn,instanceID)

        #Check Volume Availability
        vols = conn.get_all_volumes()
        foundVolume = False
        if vols:
            for v in vols:
                if volID in v.id and 'available' in v.status:
                    foundVolume = True
                    volAvailabilityZone = v.zone
                if volID in v.id and 'in-use' in v.status:
                    choice = raw_input(v.id  + " is in-use. Would you like to detach volume: (y/n): ")
                    if choice == "y" or choice == "Y":
                        detach =EC2Instance()
                        detach.detachVolume(conn,volID)
                        foundVolume = True
                        print(v.id  + " is now availible to be used.")
                        volAvailabilityZone = v.zone

        if foundVolume == False:
            print("Volume ID " + "'" + volID + "'" + ' not found or in-use.' )
            print("Try Again")

        #Check Instance
        reservations = conn.get_all_reservations()
        foundInstance = False
        # loop through reservations and extract instance information
        for r in reservations:
        # get all instances from the reservation
            instances = r.instances
            # loop through instances and print instance information
            for i in instances:
                tags = i.tags

                # check for Name property in tags object
                if instanceID in i.id and device not in i.block_device_mapping:
                    foundInstance = True
                    instanceAvailabilityZone = i._placement

        if foundInstance == False:
            print("Instance ID " + "'" + instanceID + "'" + ' not found or already has a volume attached to ' + device + ".")
            print("Try Again")

        regionsMatch = True
        if instanceAvailabilityZone != volAvailabilityZone:
            print("Error....Instance and Volume are in different regions.")
            regionsMatch = False

        if foundVolume == True and foundInstance == True and regionsMatch == True :
          print conn.attach_volume(volID, instanceID,device,False)



    def detachVolume(self,conn, volumeID):
        vols = conn.get_all_volumes()
        found = False
        if vols:
            for v in vols:
                if volumeID in v.id and 'in-use' in v.status:
                    found = True
                    attachmentData = v.attach_data
                    confirmDetach = raw_input("Detaching " + volumeID + " from " + attachmentData.instance_id + ". Confirm(y/n): " )
                    if confirmDetach == "y" or confirmDetach == "Y":
                        detached = v.detach()
                        if detached:
                            print ("Volume " + volumeID + " detached successfully!")
                        else:
                            print ("Error detaching volume " +  volumeID)
                    else:
                        print(v.id + " not detached")
                elif volumeID in v.id and 'availible' in v.status:
                    found = True
                    print ("Volume has already been detached")

        else:
            print("No volume found")
        if not found:
            print("Volume not found.")
            print ("Try Again...")

    def createInstance(self, conn, instanceType):
        if instanceType =="linux":
            imageId = 'ami-31328842'#Amazon Linux AMI
        else:
            imageId = 'ami-c6972fb5' #Windows Server
        print conn.run_instances(imageId)