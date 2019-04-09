import boto3
import click
import json
from operator import itemgetter
from sys import exit


@click.command()
@click.option('-r', '--region', help='AWS region to use', default="eu-west-1")
@click.option('-z', '--availability-zone', multiple=True,
              help="Availability Zones to use, use 'all' for all zones, multiple invocations supported, default all",
              default=["all"])
@click.option('-t', '--instance-type', multiple=True,
              help="Instance types to use, multiple invocations supported, default t3.micro", default=["t3.micro"])
@click.option('--cheapest/--all', default=False)
@click.option('-f', '--format', type=click.Choice(['json', 'text']), help="output format", default='text')
def cli(region, availability_zone, instance_type, format, cheapest):
    ec2 = boto3.client("ec2", region_name=region)

    az_query = ec2.describe_availability_zones()
    az_available = []
    for zone in az_query['AvailabilityZones']:
        az_available.append(zone['ZoneName'])

    if "all" in availability_zone:
        azs = az_available
    else:
        azs = []
        for zone in availability_zone:
            zone_name = zone
            if len(zone) == 1:
                zone_name = "{}{}".format(region, zone)

            if zone_name not in az_available:
                print("Zone not available: {}, available zones: ".format(zone_name, az_available))
                exit(1)
            else:
                azs.append(zone_name)

    results = []
    instance_types = instance_type  # less ambiguous
    for zone in azs:
        for instance_type in instance_types:
            # get last price
            last = ec2.describe_spot_price_history(InstanceTypes=[instance_type], MaxResults=1,
                                                   ProductDescriptions=['Linux/UNIX (Amazon VPC)'],
                                                   AvailabilityZone=zone)
            if len(last['SpotPriceHistory']) == 0:
                print("warning, no spot price history for instance type: {}, AZ: {}. Instance type may not"
                      "be availablein this region.".format(instance_type, zone))
            else:
                results.append({'az': zone,
                                'type': instance_type,
                                'price': float(last['SpotPriceHistory'][-1]['SpotPrice'])})

    if len(results) == 0:
        print("No results, invalid instance types?")
        exit(1)

    if cheapest:
        output = [sorted(results, key=itemgetter('price'))[0]]
    else:
        output = sorted(results, key=itemgetter('price'))

    if format == "json":
        print(json.dumps(output))
    elif format == "text":
        print("AZ\t\tInstance Type\tSpot Price")
        for line in output:
            print("{}\t{}\t{}".format(line['az'], line['type'], line['price']))