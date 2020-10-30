import yaml

config = {}
with open('config.yaml') as parameters:
    config = yaml.safe_load(parameters)
