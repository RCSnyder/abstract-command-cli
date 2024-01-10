import argparse
import json
from typing import List, Dict, Any, Union

def sub_function1(**kwargs: Dict[str, Any]) -> None:
    """Common sub-function 1 using global keyword arguments."""
    global_kwargs = kwargs.get('global_kwargs', {})
    print(f"Executing common sub-function 1 with global kwargs: {global_kwargs}")

def sub_function2(**kwargs: Dict[str, Any]) -> None:
    """Common sub-function 2 using global keyword arguments."""
    global_kwargs = kwargs.get('global_kwargs', {})
    print(f"Executing common sub-function 2 with global kwargs: {global_kwargs}")

def function1(**kwargs: Dict[str, Any]) -> None:
    """Example function 1."""
    sub_function1(**kwargs)
    print(f"Executing Function1 with arguments: {kwargs}")

def function2(**kwargs: Dict[str, Any]) -> None:
    """Example function 2."""
    sub_function2(**kwargs)
    print(f"Executing Function2 with arguments: {kwargs}")

def function3(**kwargs: Dict[str, Any]) -> None:
    """Example function 3."""
    sub_function1(**kwargs)  # Reusing common sub-function 1
    print(f"Executing Function3 with arguments: {kwargs}")

def execute_command(name: str, **kwargs: Dict[str, Any]) -> None:
    """Execute a command by name."""
    valid_functions = {
        'function1': function1,
        'function2': function2,
        'function3': function3,
    }

    if name in valid_functions:
        valid_functions[name](**kwargs)
    else:
        print(f"Command '{name}' not found.")

def execute_commands_in_order(command_list: List[str], kwargs: Dict[str, Any]) -> None:
    """Execute a list of commands in order."""
    for command in command_list:
        command_name, *command_args = command.split(' ')
        execute_command(command_name, **kwargs)
        if command_args:
            kwargs.update({k: _parse_argument(v) for k, v in (arg.split('=') for arg in command_args)})

def _parse_argument(arg: str) -> Union[int, float, bool, str]:
    """Parse an argument to its appropriate type."""
    try:
        return int(arg)
    except ValueError:
        try:
            return float(arg)
        except ValueError:
            if arg.lower() == 'true':
                return True
            elif arg.lower() == 'false':
                return False
            else:
                return arg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute inner functions with customizable keyword arguments and command list")
    parser.add_argument("--commands", nargs='+', help="List of commands to execute in order (e.g., 'function1 --arg1=42 function2 --arg2=hello')")
    parser.add_argument("--json-payload", type=str, help="JSON payload containing all CLI arguments")

    args = parser.parse_args()

    # Prepare the keyword arguments to pass to the inner functions
    kwargs: Dict[str, Any] = {}

    # Parse JSON payload if provided
    if args.json_payload:
        try:
            json_args = json.loads(args.json_payload)
            if 'global_kwargs' in json_args:
                global_kwargs = json_args['global_kwargs']
                kwargs.update(global_kwargs)
            if 'commands' in json_args:
                execute_commands_in_order(json_args['commands'], kwargs)
        except json.JSONDecodeError:
            print("Invalid JSON payload. Please provide a valid JSON payload.")
