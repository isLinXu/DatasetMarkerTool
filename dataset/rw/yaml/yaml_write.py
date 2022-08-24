import yaml


def yaml_dump(filepath, data):
    """Dumps data to a yaml file"""
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)


if __name__ == '__main__':

    filepath = ''
    data = ''
    yaml_dump(filepath, data)
