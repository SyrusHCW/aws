import boto3

aws_access_key = ''
aws_secret_key = ''

env_name = 'USE2-SB-LAB1'
bgp_asn = '65702'
regions = 'us-east-2'
acct_id = '111111111'

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_key,
    region_name = regions
    )

###### Update AZ1 Table #####################
table = dynamodb.Table('USE1-LE-TRANSIT-AZ1')
data = table.scan()
ip_count = len(data['Items'])
top = ip_count - 1
new_net = data['Items'][top]['host_bits'] + 1
vpn_cidr = '{0}{1}'.format(data['Items'][top]['network_bits'], new_net)
print(vpn_cidr)

new_aws = new_net + 1
new_pa = new_aws + 1
new_brd = new_pa + 1
role = '{0}{1}'.format(env_name, ' VPN network address')

vpc_name = '{0}{1}'.format(env_name, '-VPC')

table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_net,
        'account': acct_id,
        'vpc_name': vpc_name,
        'role' : role,
        'bgpASN' : bgp_asn
    }
)

role = '{0}{1}'.format(env_name, ' VPN aws address')

table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_aws,
        'account': acct_id,
        'vpc_name': vpc_name,
        'role' : role,
        'bgpASN' : bgp_asn
    }
)

role = '{0}{1}'.format(env_name, ' VPN palo alto address')

table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_pa,
        'account': acct_id,
        'vpc_name': vpc_name,
        'role' : role,
        'bgpASN' : bgp_asn
    }
)

role = '{0}{1}'.format(env_name, ' VPN broadcast address')

table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_brd,
        'account': acct_id,
        'vpc_name': vpc_name,
        'role' : role,
        'bgpASN' : bgp_asn
    }
)

###### Update AZ2 Table #####################
table = dynamodb.Table('USE1-LE-TRANSIT-AZ2')
data = table.scan()
ip_count = len(data['Items'])
top = ip_count - 1
new_net = data['Items'][top]['host_bits'] + 1
vpn_cidr = '{0}{1}'.format(data['Items'][top]['network_bits'], new_net)
print(vpn_cidr)

new_aws = new_net + 1
new_pa = new_aws + 1
new_brd = new_pa + 1
role = '{0}{1}'.format(env_name, ' VPN network address')

vpc_name = '{0}{1}'.format(env_name, '-VPC')

table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_net,
        'account': acct_id,
        'vpc_name': vpc_name,
        'role' : role,
        'bgpASN' : bgp_asn
    }
)

role = '{0}{1}'.format(env_name, ' VPN aws address')

table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_aws,
        'account': acct_id,
        'vpc_name': vpc_name,
        'role' : role,
        'bgpASN' : bgp_asn
    }
)

role = '{0}{1}'.format(env_name, ' VPN palo alto address')

table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_pa,
        'account': acct_id,
        'vpc_name': vpc_name,
        'role' : role,
        'bgpASN' : bgp_asn
    }
)

role = '{0}{1}'.format(env_name, ' VPN broadcast address')

table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_brd,
        'account': acct_id,
        'vpc_name': vpc_name,
        'role' : role,
        'bgpASN' : bgp_asn
    }
)
