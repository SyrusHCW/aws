#!/usr/bin/python
import boto3
from botocore.exceptions import ClientError
import sys
import csv
import re

### User definedvars
region = 'us-east-2'

aws_access_key = sys.argv[1]
aws_secret_key = sys.argv[2]

description = 'VPC tag genertaed security group'


ec2 = boto3.resource('ec2',
            aws_access_key_id = aws_access_key ,
            aws_secret_access_key = aws_secret_key ,
            region_name = region
)

client = boto3.client('ec2',
            aws_access_key_id = aws_access_key ,
            aws_secret_access_key = aws_secret_key ,
            region_name = region
)



response = client.describe_vpcs()

count1 = len(response['Vpcs'])

for e in range(0,count1):
    #print(response['Vpcs'][e]['Tags'])
    try:
        count2 = len(response['Vpcs'][e]['Tags'])
        env_name = []
        for f in range(0, count2):
            #print(response['Vpcs'][e]['Tags'][f])      
            if response['Vpcs'][e]['Tags'][f]['Key'] == 'Name':
                #print('name') 
                vpc_name = response['Vpcs'][e]['Tags'][f]['Value']
                g,h = vpc_name.split('-VPC')
                print(g)              
                env_name.append(g) 
                #print(count2)
                for j in range(0, count2):
                    print(response['Vpcs'][e]['Tags'][j]['Key']) 
                    sg_list = []
                    if response['Vpcs'][e]['Tags'][j]['Value'] == 'security:group':
                        sg_list.append(response['Vpcs'][e]['Tags'][j]['Key'])
                        #print(response['Vpcs'][e]['Tags'][j]['Key'])

                    vpc_id = response['Vpcs'][e]['VpcId']
                    #print(vpc_id)                 
                    vpc = ec2.Vpc(vpc_id)
                    group_name = response['Vpcs'][e]['Tags'][j]['Key']
                    csv_name = '{0}{1}'.format(group_name, '.csv')
                    IpPermissions = []
                    path = '{0}{1}'.format('security-groups/', csv_name)
                    f = open(path)
                    csv_f = csv.reader(f)
                    headers = next(csv_f)      
                    for row in csv_f:
                        IpPermissions_loop={'IpProtocol': row[0],
                            'FromPort': int(row[1]),
                            'ToPort': int(row[2]),
                            'IpRanges': [{
                            'CidrIp': row[3], 
                            'Description': row[4]}]}
                        IpPermissions.append(IpPermissions_loop)
                        #print(IpPermissions)
                    try:
                        security_group = vpc.create_security_group(
                            Description=description,
                            GroupName=group_name,
                            DryRun=False,
                            )
                        sg = str(security_group)
                        #print(sg)
                        m,n,o = sg.split("'") 
                        security_group = ec2.SecurityGroup(n)
                        sg_rule={'IpProtocol': '-1',
                            'FromPort': -1,
                            'ToPort': -1,
                            'UserIdGroupPairs': [{
                            'GroupId': n,
                            'Description': 'Allows traffic from with in the same sg'}]}
                        IpPermissions.append(sg_rule)
                        data = security_group.authorize_ingress(
                            IpPermissions=IpPermissions)
                        name = '{0}{1}{2}'.format(env_name[0], '-', group_name)    
                        tag = security_group.create_tags(
                            DryRun=False,
                            Tags=[
                            {
                            'Key': 'Name',
                            'Value': name
                            },
                            ]
                        )                        
                    except:
                        print('security group already exists')
            else:
                continue
    except:
        print('No tags on VPC')          

