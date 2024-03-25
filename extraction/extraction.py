import os
import json
import pandas as pd
from sqlalchemy import create_engine

def get_data_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f'File not found: {file_path}')
        return None

def process_data(data_directory, engine):
    quarter_data = []

    for current_dir, subdirs, files in os.walk(data_directory):
        if 'aggregated' in current_dir or 'map' in current_dir or 'top' in current_dir:
            data_type = os.path.basename(os.path.dirname(os.path.dirname(current_dir)))
            subfolder_name = os.path.basename(current_dir)

            if 'state' in current_dir:
                for state in os.listdir(current_dir):
                    state_dir = os.path.join(current_dir, state)

                    for file in os.listdir(state_dir):
                        if file.endswith('.json'):
                            file_path = os.path.join(state_dir, file)
                            parsed_data = get_data_from_file(file_path)

                            if parsed_data is not None:
                                year = int(file_path.split('/')[-3])
                                quarter = int(file.split('.')[0])
                                extract_function = choose_appropriate_data_extraction_function(data_type, subfolder_name, state)
                                extracted_data = extract_function(parsed_data, year, quarter)
                                if extracted_data is not None:
                                    quarter_data.append(extracted_data)
            else:
                for file in files:
                    if file.endswith('.json'):
                        file_path = os.path.join(current_dir, file)
                        parsed_data = get_data_from_file(file_path)

                        if parsed_data is not None:
                            year = int(file_path.split('/')[-2])
                            quarter = int(file.split('.')[0])
                            extract_function = choose_appropriate_data_extraction_function(data_type, subfolder_name, None)
                            extracted_data = extract_function(parsed_data, year, quarter)
                            if extracted_data is not None:
                                quarter_data.append(extracted_data)

    if not quarter_data:
        print("No data to process.")
        return None

    df = pd.concat(quarter_data, ignore_index=True)
    if df.empty:
        print("No data to save to the database.")
        return None

    file_name = choose_appropriate_data_extraction_function.__name__
    try:
        df.to_sql(f'{file_name}', engine, index=False, if_exists='replace')
        engine.execute(f"CREATE INDEX idx_quarter ON {file_name} (quarter)")
    except Exception as e:
        print(f"Failed to save data to the database: {e}")
        return None

    return df

# Define the data extraction functions here

# Example of a data extraction function
def extract_aggregated_insurance_country_data(parsed_data, year, quarter):
    table = []
    transaction_data = parsed_data['data']['transactionData']

    for transaction in transaction_data:
        row = {
            'year': year,
            'quarter': quarter,
            'name': transaction['name'],
            'count': transaction['paymentInstruments'][0]['count'],
            'amount': transaction['paymentInstruments'][0]['amount']  # Assuming 'amount' is a key in the JSON
        }
        table.append(row)

    return pd.DataFrame(table)

# Define the other data extraction functions here
def extract_aggregated_insurance_country_data(parsed_data):
    table = []
    transaction_data = parsed_data['data']['transactionData']

    for transaction in transaction_data:
        row = {
            'year': int(os.path.basename(os.path.dirname(file_path))),
            'quarter': int(file.split('.')[0]),
            'name': transaction['name'],
            'count': transaction['paymentInstruments'][0]['count'],
            'amount': transaction['paymentInstruments'][0]['amount'],
        }
        table.append(row)

    return pd.DataFrame(table)


def extract_aggregated_insurance_state_data(parsed_data):
    table = []
    from_timestamp = parsed_data['data']['from']
    to_timestamp = parsed_data['data']['to']
    transaction_data = parsed_data['data']['transactionData']

    for transaction in transaction_data:
        row = {
            'state': state.replace('-', ' ').title(),
            'year': int(os.path.basename(os.path.dirname(file_path))),
            'quarter': int(file.split('.')[0]),
            'from_timestamp': from_timestamp,
            'to_timestamp': to_timestamp,
            'type_of_transaction': transaction['name'],
            'number_of_transactions': transaction['paymentInstruments'][0]['count'],
            'total_amount': transaction['paymentInstruments'][0]['amount'],
        }
        table.append(row)

    return pd.DataFrame(table)


def extract_aggregated_transaction_country_data(parsed_data):
    table = []
    transaction_data = parsed_data['data']['transactionData']

    for transaction in transaction_data:
        row = {
            'year': int(os.path.basename(os.path.dirname(file_path))),
            'quarter': int(file.split('.')[0]),
            'name': transaction['name'],
            'count': transaction['paymentInstruments'][0]['count'],
            'amount': transaction['paymentInstruments'][0]['amount'],
        }
        table.append(row)

    return pd.DataFrame(table)


def extract_aggregated_transaction_state_data(parsed_data):
    table = []
    from_timestamp = parsed_data['data']['from']
    to_timestamp = parsed_data['data']['to']
    transaction_data = parsed_data['data']['transactionData']

    for transaction in transaction_data:
        row = {
            'state': state.replace('-', ' ').title(),
            'year': int(os.path.basename(os.path.dirname(file_path))),
            'quarter': int(file.split('.')[0]),
            'type_of_transaction': transaction['name'],
            'number_of_transactions': transaction['paymentInstruments'][0]['count'],
            'total_amount': transaction['paymentInstruments'][0]['amount'],
        }
        table.append(row)

    return pd.DataFrame(table)


def extract_aggregated_user_country_data(parsed_data):
    table = []
    registered_users = parsed_data["data"]["aggregated"]["registeredUsers"]
    total_open_apps = parsed_data["data"]["aggregated"]["appOpens"]
    users_by_device = parsed_data["data"]["usersByDevice"]

    if users_by_device is not None:
        for user_device in users_by_device:
            row = {
                'year': int(os.path.basename(os.path.dirname(file_path))),
                'quarter': int(file.split('.')[0]),
                "registered_users": registered_users,
                "total_open_apps": total_open_apps,
                "phone_brand": user_device["brand"],
                "phone_count": user_device["count"],
                "Percentage": f"{user_device['percentage'] * 100:.2f}",
            }
            table.append(row)

    return pd.DataFrame(table)


def extract_aggregated_user_state_data(parsed_data):
    table = []
    registered_users = parsed_data["data"]["aggregated"]["registeredUsers"]
    total_open_apps = parsed_data["data"]["aggregated"]["appOpens"]
    users_by_device = parsed_data["data"]["usersByDevice"]

    if users_by_device is not None:
        for user_device in users_by_device:
            row = {
                'state': state.replace('-', ' ').title(),
                'year': int(os.path.basename(os.path.dirname(file_path))),
                'quarter': int(file.split('.')[0]),
                "registered_users": registered_users,
                "total_open_apps": total_open_apps,
                "phone_brand": user_device["brand"],
                "phone_count": user_device["count"],
                "Percentage": f"{user_device['percentage'] * 100:.2f}",
            }
            table.append(row)

    return pd.DataFrame(table)


def extract_map_insurance_hover_country_data(parsed_data):
    table = []
    hover_data_list = parsed_data["data"]["hoverDataList"]

    for entry in hover_data_list:
        metric_data = entry["metric"][0]
        row = {
            'year': int(os.path.basename(os.path.dirname(file_path))),
            'quarter': int(file.split('.')[0]),
            'state': entry["name"].replace('-', ' ').title(),
            'total_transactions_count': metric_data["count"],
            'total_transactions_amount': metric_data["amount"],
        }
        table.append(row)

    return pd.DataFrame(table)


def extract_map_insurance_hover_state_data(parsed_data):
    table = []
    hover_data_list = parsed_data["data"]["hoverDataList"]

    for entry in hover_data_list:
        district_name = entry["name"].replace('-', ' ').title(),
        metric_data = entry["metric"][0]
        total_transactions_count = metric_data["count"]
        total_transactions_amount = metric_data["amount"]

        row = {
            'year': int(os.path.basename(os.path.dirname(file_path))),
            'quarter': int(file.split('.')[0]),
            'state': state.replace('-', ' ').title(),
            'districts_name': district_name,
            'total_transactions_count': total_transactions_count,
            'total_transactions_amount': total_transactions_amount,
        }
        table.append(row)

    return pd.DataFrame(table)


def extract_map_transaction_hover_country_data(parsed_data):
    table = []
    hover_data_list = parsed_data["data"]["hoverDataList"]

    for entry in hover_data_list:
        metric_data = entry["metric"][0]
        row = {
            'year': int(os.path.basename(os.path.dirname(file_path))),
            'quarter': int(file.split('.')[0]),
            'state': entry["name"].replace('-', ' ').title(),
            'total_transactions_count': metric_data["count"],
            'total_transactions_amount': metric_data["amount"],
        }
        table.append(row)

    return pd.DataFrame(table)


def extract_map_transaction_hover_state_data(parsed_data):
    table = []
    hover_data_list = parsed_data["data"]["hoverDataList"]

    for entry in hover_data_list:
        district_name = entry["name"]
        metric_data = entry["metric"][0]
        total_transactions_count = metric_data["count"]
        total_transactions_amount = metric_data["amount"]

        row = {
            'year': int(os.path.basename(os.path.dirname(file_path))),
            'quarter': int(file.split('.')[0]),
            'state': state.replace('-', ' ').title(),
            'districts_name': district_name,
            'total_transactions_count': total_transactions_count,
            'total_transactions_amount': total_transactions_amount,
        }
        table.append(row)

    return pd.DataFrame(table)


def extract_map_user_hover_country_data(parsed_data):
    table = []
    hover_data = parsed_data["data"]["hoverData"]

    for state, state_data in hover_data.items():
        row = {
            'year': int(os.path.basename(os.path.dirname(file_path))),
            'quarter': int(file.split('.')[0]),
            'state': state.replace('-', ' ').title(),
            'registered_users': state_data["registeredUsers"],
        }
        table.append(row)

    return pd.DataFrame(table)


def extract_map_user_hover_state_data(parsed_data):
    table = []
    hover_data = parsed_data["data"]["hoverData"]

    for district, district_data in hover_data.items():
        row = {
            'year': int(os.path.basename(os.path.dirname(file_path))),
            'quarter': int(file.split('.')[0]),
            'state': state.replace('-', ' ').title(),
            'districts_name': district,
            'registered_users': district_data["registeredUsers"],
        }
        table.append(row)

    return pd.DataFrame(table)


def extract_top_insurance_country_data(parsed_data):
    entity_data = []
    for entity_type in ['states', 'districts', 'pincodes']:
        entities = parsed_data['data'][entity_type]

        for entity in entities:
            entity_row = {
                'year': int(os.path.basename(os.path.dirname(file_path))),
                'quarter': int(file.split('.')[0]),
                'entity_type': entity_type,
                'entity_name': entity['entityName'],
                'transaction_type': entity['metric']['type'],
                'count': entity['metric']['count'],
                'amount': entity['metric']['amount'],
            }
            entity_data.append(entity_row)

    return pd.DataFrame(entity_data)


def extract_top_insurance_state_data(parsed_data):
    for entity_type in ['states', 'districts', 'pincodes']:
        entities = parsed_data['data'].get(entity_type)

        if entities is not None:
            entity_data = []

            for entity in entities:
                entity_name = entity["entityName"]
                entity_metric = entity["metric"]

                row = {
                    'year': int(os.path.basename(os.path.dirname(file_path))),
                    'quarter': int(file.split('.')[0]),
                    'entity_type': entity_type,
                    'entity_name': entity_name,
                    'transaction_type': entity_metric['type'],
                    'count': entity_metric['count'],
                    'amount': entity_metric['amount'],
                }
                entity_data.append(row)

            return pd.DataFrame(entity_data)

# Function to choose appropriate data extraction function
def choose_appropriate_data_extraction_function(data_type, subfolder_name, state):
    if data_type == 'aggregated':
        if subfolder_name == 'insurance':
            if state is not None:
                return extract_aggregated_insurance_state_data
            else:
                return extract_aggregated_insurance_country_data
        elif subfolder_name == 'user':
            if state is not None:
                return extract_aggregated_user_state_data
            else:
                return extract_aggregated_user_country_data
        elif subfolder_name == 'transaction':
            if state is not None:
                return extract_aggregated_transaction_state_data
            else:
                return extract_aggregated_transaction_country_data
    elif data_type == 'map':
        if subfolder_name == 'insurance':
            if state is not None:
                return extract_map_insurance_hover_state_data
            else:
                return extract_map_insurance_hover_country_data
        elif subfolder_name == 'transaction':
            if state is not None:
                return extract_map_transaction_hover_state_data
            else:
                return extract_map_transaction_hover_country_data
        elif subfolder_name == 'user':
            if state is not None:
                return extract_map_user_hover_state_data
            else:
                return extract_map_user_hover_country_data
    elif data_type == 'top':
        if subfolder_name == 'insurance':
            if state is not None:
                return extract_top_insurance_state_data
            else:
                return extract_top_insurance_country_data

# Database connection
engine = create_engine('sqlite:///mydatabase.db')

# Example usage
data_directory = '/home/user/pulse/data'
df = process_data(data_directory, engine)
