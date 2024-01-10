import argparse
import json
from typing import List, Dict, Any, Union

class Command:
    """Base class for executable commands."""
    
    def execute(self, **kwargs: Dict[str, Any]) -> None:
        """Execute the command.

        Args:
            **kwargs (Dict[str, Any]): Keyword arguments for the command.
        """
        pass

class BaseFunction(Command):
    """Base class for functions with global keyword arguments."""
    
    def __init__(self, global_kwargs: Dict[str, Any]) -> None:
        """
        Initialize the function with global keyword arguments.

        Args:
            global_kwargs (Dict[str, Any]): Global keyword arguments.
        """
        self.global_kwargs = global_kwargs

    def sub_function1(self, **kwargs: Dict[str, Any]) -> None:
        """Common sub-function 1 using global keyword arguments.

        Args:
            **kwargs (Dict[str, Any]): Keyword arguments.
        """
        print(f"Executing common sub-function 1 with global kwargs: {self.global_kwargs}")

    def sub_function2(self, **kwargs: Dict[str, Any]) -> None:
        """Common sub-function 2 using global keyword arguments.

        Args:
            **kwargs (Dict[str, Any]): Keyword arguments.
        """
        print(f"Executing common sub-function 2 with global kwargs: {self.global_kwargs}")

class Function1(BaseFunction):
    """Example function 1."""
    
    def execute(self, **kwargs: Dict[str, Any]) -> None:
        """Execute function 1.

        Args:
            **kwargs (Dict[str, Any]): Keyword arguments.
        """
        self.sub_function1(**kwargs)
        print(f"Executing Function1 with arguments: {kwargs}")

class Function2(BaseFunction):
    """Example function 2."""
    
    def execute(self, **kwargs: Dict[str, Any]) -> None:
        """Execute function 2.

        Args:
            **kwargs (Dict[str, Any]): Keyword arguments.
        """
        self.sub_function2(**kwargs)
        print(f"Executing Function2 with arguments: {kwargs}")

class Function3(BaseFunction):
    """Example function 3."""
    
    def execute(self, **kwargs: Dict[str, Any]) -> None:
        """Execute function 3.

        Args:
            **kwargs (Dict[str, Any]): Keyword arguments.
        """
        self.sub_function1(**kwargs)  # Reusing common sub-function 1
        print(f"Executing Function3 with arguments: {kwargs}")

class Invoker:
    """Class to manage and execute commands."""
    
    def __init__(self) -> None:
        self.commands: Dict[str, Command] = {}

    def add_command(self, name: str, command: Command) -> None:
        """Add a command to the invoker.

        Args:
            name (str): Name of the command.
            command (Command): Command instance to add.
        """
        self.commands[name] = command

    def execute_command(self, name: str, **kwargs: Dict[str, Any]) -> None:
        """Execute a command.

        Args:
            name (str): Name of the command.
            **kwargs (Dict[str, Any]): Keyword arguments for the command.
        """
        if name in self.commands:
            self.commands[name].execute(**kwargs)
        else:
            print(f"Command '{name}' not found.")

def execute_commands_in_order(command_list: List[str], invoker: Invoker, kwargs: Dict[str, Any]) -> None:
    """Execute a list of commands in order.

    Args:
        command_list (List[str]): List of commands to execute.
        invoker (Invoker): Invoker instance to manage command execution.
        kwargs (Dict[str, Any]): Keyword arguments for the commands.
    """
    for command in command_list:
        command_name, *command_args = command.split(' ')
        invoker.execute_command(command_name, **kwargs)
        if command_args:
            kwargs.update({k: _parse_argument(v) for k, v in (arg.split('=') for arg in command_args)})

def _parse_argument(arg: str) -> Union[int, float, bool, str]:
    """Parse an argument to its appropriate type.

    Args:
        arg (str): Argument to parse.

    Returns:
        Union[int, float, bool, str]: Parsed argument.
    """
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

    invoker = Invoker()

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
                execute_commands_in_order(json_args['commands'], invoker, kwargs)
        except json.JSONDecodeError:
            print("Invalid JSON payload. Please provide a valid JSON payload.")
