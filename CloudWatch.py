#from datetime import datetime
import datetime


from EC2 import EC2Instance
import boto


class CloudWatch:
    def __init__(self):
        ''' Volumes Constructor '''

    def enable_cw(self, conn):
        '''Enable CloudWatch monitoring on all running instances. This could be changed so you enable monitoring on
        a specific Instance ID'''

        list_inst_ids = []  # Create list of instance IDs
        reservations = conn.get_all_instances()  # Get information on currently running instances
        instances = [i for r in reservations for i in r.instances]  # Create list of instances
        for instance in instances:  # For loop checks for instance in list of instances
            if instance.state == u'running':  # If instance state is equals to runnin
                list_inst_ids.append(instance.id)  # Append instance ID to the list of instance IDs

        if list_inst_ids:
            inst_mon = conn.monitor_instances(list_inst_ids)
        else:
            print "No instances to monitor"

    def query_cw(self, ec2Conn, cw_conn):
        ''' Query CloudWatch for data about your instance'''
        instance_id = raw_input("Enter instace ID: ")
        # checkInstance = EC2Instance()
        # foundInstance = checkInstance.checkInstance(ec2Conn, instance_id)

        #nstance_id = "i-d3018a59"
        end_time = datetime.datetime.utcnow()
        start_time = datetime.datetime(2016, 4, 13, 9, 00)
        reservations = ec2Conn.get_all_reservations()

        instanceFound = False
        for r in reservations:
            #get all instances from the reservation
            instances = r.instances
            # loop through instances and print instance information
            for i in instances:
                tags = i.tags

                # check for Name property in tags object
                if instance_id in i.id:
                    instanceFound = True
                    instance = i
                    instance.monitor()
                    metrics = cw_conn.list_metrics()
                    for metric in metrics:
                        if 'InstanceId' in metric.dimensions:
                            if instance.id in metric.dimensions['InstanceId']:
                                result = cw_conn.get_metric_statistics(60, start_time, end_time, metric.name, 'AWS/EC2', "Average" , dimensions={'InstanceId':[instance_id]}, unit="Bytes")
                                for each in result:
                                    print metric, ": " , each
                                    #print type(each)
                                #print metric
                               # print result.member
        if instanceFound == False:
            print (instance_id, " not found....")
            #print my_metrics





    def cw_alarm(self, ec2Conn, sns,cw,ses):
            ''' Setup a CW alarm to send a notification - Assume you have CW enabled, you want to be notified when certain conditions
            arise. This make use of the Simple Notification Service (SNS) to send an email of CW events using alarms'''
            instance_id = "i-d3018a59"
            alarm_name = "test"
            email_addresses_list = []
            metric_name = "CPUUtilization"
            comparison = "<"
            threshold = "40"
            period = 60
            eval_periods = 5
            statistics = "Average"
            #emails = ['michael-o-sullivan@hotmail.com','michael.osullivan8@mycit.ie']
            # test  = ses.verify_email_address(emails[0])
            # test2  = ses.verify_email_address(emails[1])
            # print test
            # print test2
            i = 0
            email_addresses = ses.list_identities()
            for id in email_addresses.Identities:
                #print id
                print i, ": " , id
                email_addresses_list.append(id)
                i += 1
            emailSelected = input("Plase enter the number beside the email adreess: " )
            # if emailSelected.isdigit() and emailSelected in range(0,email_addresses_list.count(self)):
            #     intSelection = int(emailSelected)
            #     if emailSelected in range(0,email_addresses_list.count(self)):
            print ("Email selected: " + email_addresses_list[emailSelected])
            #     else:
            #      print ("'" + emailSelected +"' is not valid...")

            # for emails in email_addresses:
            #  #print emails.VerifiedEmailAddresses
            #  print emails.__dict__

            reservations = ec2Conn.get_all_reservations()

            #foundInstance = False
            # loop through reservations and extract instance information
            for r in reservations:
                # get all instances from the reservation
                instances = r.instances
                # loop through instances and print instance information
                for i in instances:
                 tags = i.tags

                 # check for Name property in tags object
                 if instance_id in i.id:
                  instance = i
                  instance.monitor()
                  # Create the SNS Topic



                topic_name = 'CWAlarm-%s' % alarm_name
                print 'Creating SNS topic: %s' % topic_name
                response = sns.create_topic(topic_name)
                topic_arn = response['CreateTopicResponse']['CreateTopicResult']['TopicArn']
                print 'Topic ARN: %s' % topic_arn
                #Subscribe the email addresses to SNS Topic
                print 'Subscribing %s to Topic %s' % (email_addresses_list[emailSelected], topic_arn)
                sns.subscribe(topic_arn, 'email', email_addresses_list[emailSelected])
                #Now find the Metric we want to be notified about
                metric = cw.list_metrics(dimensions={'InstanceId': instance_id},
                                      metric_name=metric_name)[0]
                print 'Found: %s' % metric
                #Now create Alarm for the metric
                print 'Creating alarm'
                alarm = metric.create_alarm(name=alarm_name, comparison="LessThanOrEqualToThreshold",
                                         threshold=threshold, period=period,
                                         evaluation_periods=eval_periods,
                                         statistic=statistics,
                                         alarm_actions=[topic_arn],
                                         ok_actions=[topic_arn])
                print alarm

  # def create_alarm(self, name, comparison, threshold,
  #                    period, evaluation_periods,
  #                    statistic, enabled=True, description=None,
  #                    dimensions=None, alarm_actions=None, ok_actions=None,
  #                    insufficient_data_actions=None, unit=None):