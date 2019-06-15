#!/usr/bin/python
import boto3
from botocore.exceptions import ClientError
import sys
import csv
import re

### User definedvars
vpc_id = 'vpc-02cab3df56dd953b6'
region = 'us-east-2'


aws_access_key = sys.argv[1]
aws_secret_key = sys.argv[2]


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

env_name = []

response = client.describe_vpcs(VpcIds = [vpc_id])
tags = response['Vpcs'][0]['Tags']
tag_count = len(response['Vpcs'][0]['Tags'])

for tag in range(0,tag_count):
    if response['Vpcs'][0]['Tags'][tag]['Key'] == 'Name':
        vpc_name = response['Vpcs'][0]['Tags'][tag]['Value']
        m,n = vpc_name.split('-VPC')
        env_name.append(m)

for tag in range(0,tag_count):
    try:
        key = response['Vpcs'][0]['Tags'][tag]['Key']
        m,n = key.split(':')
        if m == 'sg' and response['Vpcs'][0]['Tags'][tag]['Value'] == 'true':
            group = n
            team, app = n.split('-')
            #print(team, app)
            team_def = []
            if team == 'dops':
                team_def.append('Development Operations ')
            if team == 'nops':
                team_def.append('Network Operations ')
            if team == 'sops':
                team_def.append('Security Operations ')
            if team == 'iops':
                team_def.append('Infrastructure Operations ')
            print(team_def)
            description = '{0}{1}{2}'.format(team_def[0], app, ' security group')
            print(description)    
            group_name = '{0}{1}'.format(n, '-sg')
            csv_name = '{0}{1}'.format(group_name, '.csv')
            IpPermissions = []
            path = '{0}{1}'.format('./security-groups/', csv_name)
            print(n)
            try:
                print(path)               
                f = open(path)
                print(path, 'Opening')
                csv_f = csv.reader(f)
                headers = next(csv_f)
                print('Open')      
                for row in csv_f:
                    IpPermissions_loop={'IpProtocol': row[0],
                        'FromPort': int(row[1]),
                        'ToPort': int(row[2]),
                        'IpRanges': [{
                        'CidrIp': row[3], 
                        'Description': row[4]}]}
                    IpPermissions.append(IpPermissions_loop)
                    print(IpPermissions)
            except:
                print('No matching csv file') 
            try:
                print('creating')
                vpc = ec2.Vpc(vpc_id)
                security_group = vpc.create_security_group(
                    Description=description,
                    GroupName=group_name,
                    DryRun=False,
                    )
                sg = str(security_group)
                #print(sg)
                x,y,z = sg.split("'") 
                print(y)
                security_group = ec2.SecurityGroup(y)
                sg_rule={'IpProtocol': '-1',
                    'FromPort': -1,
                    'ToPort': -1,
                    'UserIdGroupPairs': [{
                    'GroupId': y,
                    'Description': 'Allows traffic from with in the same sg'}]}
                IpPermissions.append(sg_rule)
                print(IpPermissions)
                data = security_group.authorize_ingress(
                    IpPermissions=IpPermissions)
                print(env_name)
                name = '{0}{1}{2}'.format(env_name[0], '-', group_name.upper()) 
                print(name)        
                sg_tag = security_group.create_tags(
                    DryRun=False,
                    Tags=[
                    {
                    'Key': 'Name',
                    'Value': name
                    },
                    ]
                    )
                vpc_tag = ec2.meta.client.create_tags(
                    DryRun=False,
                    Resources=[
                        vpc_id,
                    ],
                    Tags=[
                    {
                    'Key': key,
                    'Value': 'deployed'
                    },
                    ]
                    )                        
            except:
                print('security group already exists')    
    except:
        print('not an sg')  



 
