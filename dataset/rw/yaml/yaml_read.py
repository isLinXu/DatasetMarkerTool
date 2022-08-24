import yaml
import pprint


def yaml_loader(filepath):
    """Loads a yaml file"""
    with open(filepath, "r") as file_descriptor:
        # data = yaml.load(file_descriptor, Loader=yaml.FullLoader)
        data = yaml.full_load(file_descriptor)
    return data





def yamltotext(filename):
    with open(filename, "r") as yaml_file:
        file_data = yaml.load_all(yaml_file, Loader=yaml.FullLoader)

        for item in file_data:
            intent_type = item["type"]
            intent_name = item["name"]
            newline = "\n"

            if intent_type == "intent":
                utterances = item["utterances"]

                with open(f"data/Text_Files/Utterances/{intent_name}.txt", mode="w+") as intent_file:
                    for i, name in enumerate(utterances):
                        # print("Index: ", i, "\tLength:", len(utterances) - 1)
                        if len(utterances) - 1 == i:
                            newline = ""  # To remove new line at the end of file.
                        intent_file.write(name + newline)  # Adding data to text file with new line.

            elif intent_type == "entity":
                entity_values = str(item["values"])
                with open(f"data/Text_Files/Entity/{intent_name}.txt", mode="w+") as entity_file:
                    entity_file.write(entity_values)

        return "Text files created successfully."


# file_to_convert = "data/dataset.yaml"
# print(yamltotext(file_to_convert))

if __name__ == "__main__":
    file_path = "/home/hxzh02/PycharmProjects/PaddleWorkShop/PaddleDetection/configs/test.yaml"
    data = yaml_loader(file_path)
    print('data:', data)
    # print(data["weapons"])
    # pp = pprint.PrettyPrinter(indent=6, depth=4)
    # pp.pprint(data)
    # pp = pprint.PrettyPrinter(indent=6, depth=2)
    # pp.pprint(data)
    pp = pprint.PrettyPrinter(indent=1, depth=4)
    pp.pprint(data)
