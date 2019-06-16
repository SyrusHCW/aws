#!/usr/bin/python
import boto3
from botocore.exceptions import ClientError
import sys

    


aws_access_key = sys.argv[1]
aws_secret_key = sys.argv[2]

region = sys.argv[3]
inst_id = sys.argv[4]

ec2 = boto3.resource('ec2',
    aws_access_key_id = aws_access_key ,
    aws_secret_access_key = aws_secret_key ,
    region_name = region,
)

client = boto3.client('ec2',
    aws_access_key_id = aws_access_key ,
    aws_secret_access_key = aws_secret_key ,
    region_name = region,
)

###########################################################################
################ Run through all instances in returned ####################
###########################################################################

instance = ec2.Instance(inst_id)
vpc = instance.vpc
vpc_str = str(vpc)          # converts aws source to string
m,n,o = vpc_str.split("'")  # return value looks like ec2.SecurityGroup(id='sg-0a3546680dcc10614'), this will grab id between single quotes, and assign it a 'n'
vpc_id = n
tags = instance.tags
i = []                      # contains the instance id of instances with tags
i_dict = {}                 # creates a dictonary, which contains instance id as keyword, and list of security group id's as value
sg_vpc = []                 # contains all security groups in vpc
sg_inst = []                # list of security groups, this will become the value in the dictonary

###########################################################################
############# Grab a list of all security groups in region ################
###########################################################################

print(vpc_id)
sg_response = client.describe_security_groups()
count1 = len(sg_response['SecurityGroups'])
   
for y in range(0,count1):
    # if a security group belongs to the same vpc as an instance, it will added them to the list sg_vpc
    if sg_response['SecurityGroups'][y]['VpcId'] == vpc_id:
        sg_vpc.append(sg_response['SecurityGroups'][y]['GroupId'])
        print(sg_response['SecurityGroups'][y]['GroupName'])
        i_dict[inst_id] = []
        print(sg_vpc)


###########################################################################
################# Start searching for matching tags #######################             #if adding a new tag seach, create a list variable in top for loop
###########################################################################
        try:
            gname_sg = sg_response['SecurityGroups'][y]['GroupName']
            e,f = gname_sg.split('-sg')
            gname = e
            for tag in tags:
                #print(tag)
                try:
                    inst_sg = tag['Key']
                    g,h = inst_sg.split(':')
                    print(h)
                    print(gname)
                    gid = sg_response['SecurityGroups'][y]['GroupId']
                    print(gid)
                    if gname == h:
                        i.append(inst_id)
                        sg_inst.append(gid)
                        print(inst_id, gid)
                    else:
                        continue    
                except:
                    print('tag is not for security groups')
        except:
            print('nope')            

###########################################################################
################### End search for matching tags #########################
###########################################################################

i_dict.get(inst_id, []).append(sg_inst)                
print(i_dict)

if i_dict[inst_id][0] != []:                                                        # For instances with empty security groups skip
    print(inst_id)
    sg_list = i_dict[inst_id][0]                                                    # security group list is made from list in dictonary
    print(sg_list)
    sg_instance = ec2.Instance(inst_id)                                            # Select instance 
    sg_instance.modify_attribute(Groups=sg_list)                                   # Update instances using list

