import boto.ec2.autoscale
from boto.ec2.autoscale.group import AutoScalingGroup
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import ScalingPolicy
from boto.ec2.cloudwatch import MetricAlarm

class autoScaling:
    def __init__(self):
        ''' autoScaling Instance Constructor '''

    def viewAllGroups(self,asConn):
        groups = asConn.get_all_groups()
        print("***GROUPS***")
        for each in groups:
            print ("")
            print "Name: ", each.name
            print "Created on: ", each.created_time
            print "Launch Configurations: ", each.launch_config_name
            print "Minimum number of instances: ", each.min_size
            print "Max number of instances: ", each.max_size
            print ("")
        print ("")
        print ("get_all_autoscaling_instances")
        test = asConn.get_all_autoscaling_instances()
        print test
    def viewLaunchConfigs(self,asConn):
        launchConfig = asConn.get_all_launch_configurations()
        print("***Launch Configurations***")
        for each in launchConfig:
            print ("")
            print "Name: ", each.name
            print "Connection: ", each.connection
            print "Image ID : ", each.image_id
            print ("")


    def createLaunchConfig(self, asConn):
        launchName= raw_input("Please enter name of launch configurations: " )
        instanceType= raw_input("Please enter free tier OS(windows/linux): " )
        if instanceType =="linux":
            imageId = 'ami-31328842'#Amazon Linux AMI
        else:
            imageId = 'ami-c6972fb5' #Windows Server

        lc = LaunchConfiguration(name=launchName, image_id=imageId,
                             key_name='michael',
                             security_groups=['groupSecuirtyMOS'])
        res = asConn.create_launch_configuration(lc)

        print ("")
        print ("All launch Configurations: ")
        #self.viewAllGroups(asConn)
        #print asConn.get_all_activities()
    def createGroup(self,asConn):
        allLaunchConfigs = asConn.get_all_launch_configurations()
        listOfConfigs = []
        i = 0
        for each in allLaunchConfigs:
            print i, ": ", each.name
            listOfConfigs.append(each.name)
            i += 1

        zones= ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
        configSelected = input("Plase enter the number beside the launch configurations you want to use: ")
        minSize = input("Plase enter minimum size of the group: ")
        maxSize = input("Plase enter maximum size of the group: ")
        #groupName = input("Plase enter group name: ")
        ag = AutoScalingGroup(group_name='my_group', availability_zones= zones
                                             ,min_size=minSize, max_size=maxSize,load_balancers=['myLB'],
                                             launch_config=listOfConfigs[configSelected])

        asConn.create_auto_scaling_group(ag)

    def createScaleUpForGroup(self,asConn, cw2Conn):
        groups = asConn.get_all_groups()
        listOfGroups = []
        i = 0
        groupSelected = -1
        for each in groups:
            print i, ": ", each.name
            listOfGroups.append(each.name)
            i += 1
        groupSelected = input("Plase enter the number beside the group you want to create scale up policy: ")
        nameOfPolicy = raw_input("Plase enter name of policy: ")

        scale_up_policy = ScalingPolicy(
        name=nameOfPolicy, adjustment_type='ChangeInCapacity',
        as_name=listOfGroups[groupSelected], scaling_adjustment=1, cooldown=180)

        asConn.create_scaling_policy(scale_up_policy)

        scale_up_policy = asConn.get_all_policies(
                    as_group=listOfGroups[groupSelected], policy_names=[nameOfPolicy])[0]
        alarm_dimensions = {"AutoScalingGroupName": listOfGroups[groupSelected]}

        # One alarm for when to scale up...
        scale_up_alarm = MetricAlarm(
                name='scale_up_on_cpu', namespace='AWS/EC2',
                metric='CPUUtilization', statistic='Average',
                comparison='>', threshold='70',
                period='60', evaluation_periods=2,
                alarm_actions=[scale_up_policy.policy_arn],
                dimensions=alarm_dimensions)
        res =  cw2Conn.create_alarm(scale_up_alarm)
        if(res):
            print ("Scaled up " + nameOfPolicy + " created.")
        else:
            print ("ERROR, Scaled up " + nameOfPolicy + " not created.")



    def createScaleDownForGroup(self,asConn, cw2Conn):
        groups = asConn.get_all_groups()
        listOfGroups = []
        i = 0
        for each in groups:
            print i, ": ", each.name
            listOfGroups.append(each.name)
            i += 1
        groupSelected = input("Plase enter the number beside the group you want to create scale up policy: ")
        nameOfPolicy = raw_input("Plase enter name of policy: ")

        scale_down_policy = ScalingPolicy(
            name=nameOfPolicy, adjustment_type='ChangeInCapacity',
            as_name=listOfGroups[groupSelected], scaling_adjustment=-1, cooldown=180)

        # The policy objects are now defined locally.
        # Let's submit them to AWS.
        asConn.create_scaling_policy(scale_down_policy)
        scale_down_policy = asConn.get_all_policies(
                as_group=listOfGroups[groupSelected], policy_names=[nameOfPolicy])[0]
        asConn.create_scaling_policy(scale_down_policy)
        alarm_dimensions = {"AutoScalingGroupName": listOfGroups[groupSelected]}


        scale_down_alarm = MetricAlarm(
        name='scale_down_on_cpu', namespace='AWS/EC2',
        metric='CPUUtilization', statistic='Average',
        comparison='<', threshold='40',
        period='60', evaluation_periods=2,
        alarm_actions=[scale_down_policy.policy_arn],
        dimensions=alarm_dimensions)
        res = cw2Conn.create_alarm(scale_down_alarm)
        if(res):
            print ("Scaled down " + nameOfPolicy + " created.")
        else:
            print ("ERROR, Scaled down " + nameOfPolicy + " not created.")
