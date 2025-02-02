from flask import Flask, request, jsonify
from flask import render_template
import utils
import os
import json
app = Flask(__name__)


# This is the route for the home page
@app.route('/')
def home():
    return render_template('index.html')
# This is the route for update machine


@app.route('/machines')
def machines():
    machine_data = utils.load_machine()
    return machine_data


@app.route('/data/<machine_id>')
def get_machine_data(machine_id):
    data = utils.load_data(machine_id)
    return data


@app.route('/delete', methods=['POST'])
def delete_data():
    data = request.get_json()

    for row in data:
        machine_id = row['machineID']
        options_id = row['OptionsID']
        component = row['component']
        print(f"machine ID: {machine_id}")
        file_path = f"data/{machine_id}.json"
        print(f"file path: {file_path}")
        if not os.path.exists(file_path):
            return jsonify({'message': f'MachineID {machine_id} not found'}), 404

        with open(file_path, 'r') as file:
            machine_data = json.load(file)

        if options_id in machine_data:
            original_length = len(machine_data[options_id])
            machine_data[options_id] = [
                item for item in machine_data[options_id] if item['component'] != component]
            if len(machine_data[options_id]) == original_length:
                return jsonify({'message': f'Component {component} not found in {options_id}'}), 404
        else:
            return jsonify({'message': f'OptionsID {options_id} not found'}), 404

        with open(file_path, 'w') as file:
            json.dump(machine_data, file, indent=4)

    return jsonify({'message': 'Components deleted successfully'})


@app.route('/delete-all', methods=['POST'])
def delete_all_data():
    data = request.get_json()
    if data.get('action') == 'delete all':
        return jsonify({'message': 'All data deleted successfully'})
    else:
        return jsonify({'message': 'Invalid action'}), 400


if __name__ == '__main__':
    app.run(debug=True)
