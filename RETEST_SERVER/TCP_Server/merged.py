import json
import os

# Đường dẫn tới các file JSON
file1_path = 'file1.json'
file2_path = 'file2.json'
file3_path = 'file3.json'
merged_file_path = 'merged.json'


def read_json(file_path):
    try:
        if not os.path.getsize(file_path) > 0:

            with open(file_path, 'r') as f:
                return json.load(f)
        else:
            return {}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


# Đọc nội dung của các file JSON
data1 = read_json(file1_path)
data2 = read_json(file2_path)
data3 = read_json(file3_path)

# Ghép nội dung của các file JSON và bao gồm tên file
merged_data = {
    os.path.basename(file1_path): data1,
    os.path.basename(file2_path): data2,
    os.path.basename(file3_path): data3
}

# Ghi nội dung đã ghép vào file JSON mới
with open(merged_file_path, 'w') as f:
    json.dump(merged_data, f, indent=4)

print(f"Merged data has been written to {merged_file_path}")
