


dynamodb = boto3.resource('dynamodb',
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_key,
    region_name = regions
    )

table = dynamodb.Table('p2p-cidrs')

data = table.scan()

ip_count = len(data['Items'])

top = ip_count - 1

new_net = data['Items'][top]['host_bits'] + 1

vpn_cidr = '{0}{1}'.format(data['Items'][top]['network_bits'], new_net)

print(vpn_cidr)

new_aws = new_net + 1
new_pa = new_aws + 1
new_brd = new_pa + 1
env_name = 'USE2-SB-LAB1'
role = '{0}{1}'.format(env_name, ' VPN network address')
vpc_name = '{0}{1}'.format(env_name, '-VPC')
table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_net,
        'account': 'id',
        'vpc_name': vpc_name,
        'role' : role
    }
)
role = '{0}{1}'.format(env_name, ' VPN aws address')
table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_aws,
        'account': 'id',
        'vpc_name': vpc_name,
        'role' : role
    }
)
role = '{0}{1}'.format(env_name, ' VPN palo alto address')
table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_pa,
        'account': 'id',
        'vpc_name': vpc_name,
        'role' : role
    }
)
role = '{0}{1}'.format(env_name, ' VPN broadcast address')
table.put_item(
   Item={
        'network_bits': data['Items'][top]['network_bits'],
        'host_bits': new_brd,
        'account': 'id',
        'vpc_name': vpc_name,
        'role' : role
    }
)
