import json


def read_txt_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 2:
                component, counter = parts
                data.append({
                    "component": component,
                    "counter": int(counter)
                })
    return data


def convert_to_json():
    analog_data = read_txt_file('./data/analog.txt')
    nodes_data = read_txt_file('./data/nodes.txt')
    # Assuming you have a vtep.txt file
    vtep_data = read_txt_file('./data/vtep.txt')

    json_data = {
        "analog": analog_data,
        "nodes": nodes_data,
        "vtep": vtep_data
    }

    json_string = json.dumps(json_data, indent=4)
    # Lưu chuỗi JSON vào file FVNM10.json
    with open('./data/FVNM10.json', 'w') as json_file:
        json_file.write(json_string)
    return json_string


if __name__ == '__main__':
    json_output = convert_to_json()
    print(json_output)
