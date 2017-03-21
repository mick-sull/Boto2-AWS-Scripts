from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
import libcloud.security
class openstack:

    def __init__(self):
        ''' Overstack Instance '''

    def listRunningInt(self, driver):
        nodes = driver.list_nodes()
        #print images
        x = 0
        for node in nodes:
            if node.state ==0:#0 is for running
                print x, ": ", node.name, " - ID: ", node.uuid, " - IP Address: ",  node.private_ips



    def displayVolumes(self,driver):
        volumes = driver.list_volumes()
        for v in volumes:
            print "Name: ", v.name, " -  ID: ", v.id, " - Size:", v.size , "GB"
        #print volumes.__dict__

