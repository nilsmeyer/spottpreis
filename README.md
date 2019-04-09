# ec2spotter - Discover spot prices for AWS EC2 Instance
## Description
This is a small helper for discovering the cheapest instance type in a region
and within availability zones. It can be used to automate bidding on spot
instances, returning the last bid for your selection. 

## Installation
```bash
git clone ssh://git@github.com/nilsmeyer/ec2spotter
cd ec2spotter
pip3 install --user . 
```

## Usage
This application uses click, you can check the arguments using the `--help`
command line switch. Output can be formatted in json or as text, it will
return a list starting with the least expensive.

You must have an AWS client environment configured and a profile available.

```
Usage: ec2spotter [OPTIONS]

Options:
  -r, --region TEXT              AWS region to use (default eu-west-1)
  -z, --availability-zone TEXT  Availability Zones to use, use 'all' for all
                                 zones
  -t, --instance-type TEXT      Instance types to use
  --cheapest / --all
  -f, --format [json|text]       output format
  --help                         Show this message and exit.
```

### Examples
#### find cheapest instance in all AZs
```bash
ec2spotter --cheapest --instance-type c5.large --instance-type c5n.large \
--instance-type c5d.large
```

#### instances ordered by last bid in all AZs
```bash
ec2spotter --instance-type c5.large --instance-type c5n.large \ 
--instance-type c5d.large
```

#### cheapest in eu-west-1c
```bash
ec2spotter --instance-type c5.large --instance-type c5n.large \
--instance-type c5d.large --instance-type m5.large --instance-type r5.large \
--availability-zone eu-west-1c --cheapest
```

#### shortening the zone is supported
```bash
ec2spotter --availability-zone b --availability-zone c \
--instance-type c5.large --instance-type c5n.large --instance-type c5d.large
```

## Trademarks
AWS and EC2 are (probably?) Trademarks of Amazon.com Inc. or it's subsidiaries. This
project is **NOT** in any way affiliated with Amazon. 