import base64
import os
import yaml

def decode_base64_in_yaml(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = yaml.safe_load(infile)

    def decode(data):
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = decode(value)
        elif isinstance(data, list):
            for index, value in enumerate(data):
                data[index] = decode(value)
        elif isinstance(data, str):
            try:
                # Attempt to decode as base64
                decoded_value = base64.b64decode(data).decode('utf-8')
                return decoded_value
            except Exception:
                # Not base64-encoded, return as-is
                pass
        return data

    decoded_data = decode(data)

    with open(output_file, 'w') as outfile:
        yaml.dump(decoded_data, outfile, default_flow_style=False)

def decode_secrets_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, "decoded_" + filename)
            decode_base64_in_yaml(input_file, output_file)
            print(f"Decoded {input_file} to {output_file}")

if __name__ == "__main__":
    directory_path = "./"  # Replace with your directory path
    decode_secrets_in_directory(directory_path)
