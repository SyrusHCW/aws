import boto3
from botocore.exceptions import ClientError
import sys
import csv


region = ['us-east-1', 
        'us-east-2', 
        'us-west-1', 
        'us-west-2',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3']

group_name = 'DOPS-WFE-SG'

csv_name = '{0}{1}'.format(group_name, '.csv')


#aws_access_key = sys.argv[1]
#aws_secret_key = sys.argv[2]

description = 'DevOps web fron end security group'

count1 = len(region)

print(group_name)

for z in range(0,count1):


    ec2 = boto3.resource('ec2',
                #aws_access_key_id = aws_access_key ,
                #aws_secret_access_key = aws_secret_key ,
                region_name = region[z],
    )

    client = boto3.client('ec2',
                #aws_access_key_id = aws_access_key ,
                #aws_secret_access_key = aws_secret_key ,
                region_name = region[z],
    )


    sg_id = []

    response = client.describe_security_groups()

    count3 = len(response['SecurityGroups'])

    for x in range(0,count3):
        if response['SecurityGroups'][x]['GroupName'] == group_name:
            sg_id.append(response['SecurityGroups'][x]['GroupId'])
        else:
            continue

    print(region[z])
    print("This regions that matches DOPS-WFE-SG")
    print(sg_id)

    count4 = len(sg_id)
    for e in range(0,count4):
        sg_vpc = []
        elb_sg = []
        response = client.describe_security_groups(GroupIds = [sg_id[e]])
        vpc_id = response['SecurityGroups'][0]['VpcId']
        response1 = client.describe_security_groups()
        count3 = len(response1['SecurityGroups'])
        sg_vpc = []


        for x in range(0,count3):
            if response1['SecurityGroups'][x]['VpcId'] ==  vpc_id:
                sg_vpc.append(response1['SecurityGroups'][x]['GroupId'])
            else:
                continue
        print("Security Groups in Single VPC")
        print(sg_vpc)        


        count7 = len(sg_vpc)

        for c in range(0,count7): 
            tag_list = []   
            security_group = client.describe_security_groups(GroupIds = [sg_vpc[c]])
            count8 = len(security_group['SecurityGroups'][0])
            #print(count8)
            try:
                #print(security_group['SecurityGroups'][0]['Tags'])
                count9 = len(security_group['SecurityGroups'][0]['Tags'])
                for d in range(0,count9):
                    if security_group['SecurityGroups'][0]['Tags'][d]['Key'] == 'public:fe':
                        #print("Matches FE")
                        elb_sg.append(security_group['SecurityGroups'][0]['GroupId'])   #####
                        #print(True)
                    else:
                        print(False)    
                else:
                    continue    
            except:
                print('No tags present')  


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
        elb_count = len(elb_sg)
        if elb_count > 0:
            elb_rule={'IpProtocol': 'tcp',
                'FromPort': 443,
                'ToPort': 443,
                'UserIdGroupPairs': [{
                'GroupId': elb_sg[0],
                'Description': "Allows ELB to talk to Web front ends"}]}
            IpPermissions.append(elb_rule)  
        sg_rule={'IpProtocol': '-1',
            'FromPort': -1,
            'ToPort': -1,
            'UserIdGroupPairs': [{
            'GroupId': sg_id[e],
            'Description': 'DevOps Web front end Security Group'}]}

        IpPermissions.append(sg_rule)
        security_group = ec2.SecurityGroup(sg_id[e])    #############
        print(IpPermissions)
        try:
            security_group.revoke_ingress(IpPermissions=security_group.ip_permissions)
            data = security_group.authorize_ingress(
                IpPermissions=IpPermissions)
        except:
            print('no inbound rules in this region')
            data = security_group.authorize_ingress(
                IpPermissions=IpPermissions)


