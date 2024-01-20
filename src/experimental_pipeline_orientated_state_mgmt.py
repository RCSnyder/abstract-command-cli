import sys
import json
import hashlib
import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd
import pyarrow.parquet as pq
from io import BytesIO

# Initialize AWS S3 client
s3 = boto3.client('s3')

# Function to save intermediate state to S3 as Parquet
def save_df_to_s3(execution_id, df):
    try:
        with BytesIO() as buffer:
            df.to_parquet(buffer, index=False)
            buffer.seek(0)
            s3.upload_fileobj(buffer, 'your-s3-bucket', f'pipeline_states/{execution_id}.parquet')
    except NoCredentialsError:
        print("AWS credentials not found. Unable to save to S3.")

# Function to load intermediate state from S3 as Parquet
def load_df_from_s3(execution_id):
    try:
        with BytesIO() as buffer:
            s3.download_fileobj('your-s3-bucket', f'pipeline_states/{execution_id}.parquet', buffer)
            buffer.seek(0)
            return pd.read_parquet(buffer)
    except NoCredentialsError:
        print("AWS credentials not found. Unable to load from S3.")
    except s3.exceptions.NoSuchKey:
        print(f"No cached state found for execution ID {execution_id}.")
    return None

# Function to initialize DataFrames from S3 paths
def initialize_dataframes(data_list):
    data_dict = {}
    for item in data_list:
        df_name = item['name']
        s3_path = item['s3_path']
        try:
            with BytesIO() as buffer:
                s3.download_fileobj('your-s3-bucket', s3_path, buffer)
                buffer.seek(0)
                data_dict[df_name] = pd.read_parquet(buffer)
        except NoCredentialsError:
            print("AWS credentials not found. Unable to load DataFrame from S3.")
        except s3.exceptions.NoSuchKey:
            print(f"No data found at S3 path: {s3_path}")
    return data_dict

# Example functions for the pipeline steps
def step1(data, arg1=0, **kwargs):
    # Perform some operation on DataFrame
    data['result1'] = data['value'] + arg1
    return data

def step2(data, arg2=0, **kwargs):
    # Perform another operation on DataFrame
    data['result2'] = data['result1'] * arg2
    return data

def step3(data, arg3=0, **kwargs):
    # Add another step (generic) on DataFrame
    data['result3'] = data['result2'] - arg3
    return data

# List of step functions with their respective arguments
steps = [
    (step1, {'arg1': 5}),
    (step2, {'arg2': 3}),
    (step3, {'arg3': 2})
]

class Pipe:
    """A class for creating function pipelines."""

    def __init__(self):
        self.data = None
        self.completed_steps = []

    def apply(self, step_func, step_args):
        if self.data is None:
            raise ValueError("Pipeline data not initialized. Use 'initialize_data' method first.")
        step_name = step_func.__name__
        if step_name not in self.completed_steps:
            self.data = step_func(self.data, **step_args)
            self.completed_steps.append(step_name)
        return self

    def result(self):
        return self.data

    def initialize_data(self, data):
        self.data = data

def calculate_execution_id(**kwargs):
    """Generate a deterministic execution ID based on input arguments (kwargs)."""
    args_json = json.dumps(kwargs, sort_keys=True)
    return hashlib.sha256(args_json.encode()).hexdigest()

def main(steps, input_args, data_list):
    execution_id = calculate_execution_id(**input_args)
    cached_state = load_df_from_s3(execution_id)
    
    if cached_state is not None:
        print(f"Resuming pipeline with execution ID {execution_id} from cached state.")
        initial_data = cached_state['data']
        completed_steps = cached_state['completed_steps']
    else:
        print(f"Starting new pipeline with execution ID {execution_id}.")
        completed_steps = []

    # Initialize DataFrames from S3 paths
    initial_data = initialize_dataframes(data_list)

    # Create a Pipe instance, initialize data, and apply the desired steps with arguments
    pipe = Pipe()
    pipe.initialize_data(initial_data)
    for step_func, step_args in steps:
        step_name = step_func.__name__
        if step_name not in completed_steps:
            pipe.apply(step_func, step_args)

    final_result = pipe.result()
    save_df_to_s3(execution_id, {'data': final_result, 'completed_steps': completed_steps})  # Save intermediate state to S3

    return final_result

# Example input arguments (kwargs)
input_args = {
    'param1': 10,
    'param2': 20,
    'param3': 'abc'
}

# Example initial data list (DataFrame names and S3 paths)
data_list = [
    {'name': 'df1', 's3_path': 'path/to/df1.parquet'},
    {'name': 'df2', 's3_path': 'path/to/df2.parquet'}
]

# Perform pipeline execution based on input arguments, data list, and selected steps with arguments
result = main(steps, input_args, data_list)
print(f"Final result for execution ID {calculate_execution_id(**input_args)}:\n{result}")
