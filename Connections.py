import boto.ec2
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.ec2.cloudwatch import CloudWatchConnection
from boto.ses import SESConnection
import boto.ec2.autoscale
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


import libcloud.security

from boto import config
aws_access_key_id = config.get('CREDENTIALS', 'aws_access_key_id')
aws_secret_access_key = config.get('CREDENTIALS','aws_secret_access_key')



class Connection:
    def __init__(self):
        ''' Connection Instance '''
        self.region = 'eu-west-1'

    #def ec2Connection(self, aws_access_key_id, aws_secret_access_key):
    def ec2Connection(self):
        ''' Create and return an EC2 Connection '''
        conn = boto.ec2.connect_to_region(self.region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        return conn

    def s3Connection(self):
        conn = S3Connection(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        return conn

    def cwConnection(self):
        #cw_conn = CloudWatchConnection( aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        cw_conn = boto.ec2.cloudwatch.connect_to_region(self.region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        return cw_conn

    def snsConnection(self):
         snsConn = boto.connect_sns(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
         return snsConn

    def sesConnection(self):
        sesConn = boto.connect_ses(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        return sesConn

    def autoscalingConnection(self):
        #asConn = boto.connect_autoscale(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        asConn = boto.ec2.autoscale.connect_to_region(self.region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        #asConn =  boto.connect_autoscale(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        return asConn

    def openstackConnection(self):# This assumes you don't have SSL set up.

        libcloud.security.CA_CERTS_PATH= ['']
        OpenStack = get_driver(Provider.OPENSTACK)
        driver = OpenStack('',
                        '',
                        ex_force_auth_url='',
                        ex_force_service_type='',
                        ex_force_auth_version='',
                        ex_tenant_name='')
        return driver
