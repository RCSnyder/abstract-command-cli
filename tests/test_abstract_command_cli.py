import json
import pytest
from unittest.mock import patch, MagicMock
from src.abstract_command_cli import (
    Command,
    BaseFunction,
    Function1,
    Function2,
    Function3,
    Invoker,
    execute_commands_in_order,
    _parse_argument,
)

@pytest.fixture
def mock_command():
    return MagicMock(Command)

@pytest.fixture
def mock_base_function():
    return MagicMock(BaseFunction)

@pytest.fixture
def mock_function1():
    return MagicMock(Function1)

@pytest.fixture
def mock_function2():
    return MagicMock(Function2)

@pytest.fixture
def mock_function3():
    return MagicMock(Function3)

@pytest.fixture
def invoker_with_commands(mock_command, mock_base_function, mock_function1, mock_function2, mock_function3):
    invoker = Invoker()
    invoker.add_command("command", mock_command)
    invoker.add_command("base_function", mock_base_function)
    invoker.add_command("function1", mock_function1)
    invoker.add_command("function2", mock_function2)
    invoker.add_command("function3", mock_function3)
    return invoker

def test_command_execute():
    command = Command()
    with pytest.raises(NotImplementedError):
        command.execute({})

def test_base_function_init():
    global_kwargs = {"arg1": 42, "arg2": "hello"}
    base_function = BaseFunction(global_kwargs)
    assert base_function.global_kwargs == global_kwargs

def test_function1_execute(mock_function1):
    kwargs = {"arg1": 42, "arg2": "hello"}
    function1 = Function1({})
    function1.execute(kwargs)
    mock_function1.sub_function1.assert_called_once_with(**kwargs)
    assert mock_function1.mock_calls[-1] == pytest.call(**kwargs)

# Add similar tests for Function2, Function3, and other classes/functions

def test_invoker_add_command(invoker_with_commands):
    assert "command" in invoker_with_commands.commands
    assert "base_function" in invoker_with_commands.commands
    assert "function1" in invoker_with_commands.commands
    assert "function2" in invoker_with_commands.commands
    assert "function3" in invoker_with_commands.commands

def test_invoker_execute_command(invoker_with_commands, mock_command):
    invoker_with_commands.execute_command("command", arg1=42)
    mock_command.execute.assert_called_once_with(arg1=42)

# Add similar tests for other functions/classes

def test_execute_commands_in_order(invoker_with_commands, mock_command):
    command_list = ["command", "base_function"]
    kwargs = {"arg1": 42, "arg2": "hello"}
    
    with patch("builtins.print") as mock_print:
        execute_commands_in_order(command_list, invoker_with_commands, kwargs)
    
    mock_command.execute.assert_called_once_with(**kwargs)
    mock_print.assert_called_once_with("Command 'base_function' not found.")

def test_parse_argument():
    assert _parse_argument("42") == 42
    assert _parse_argument("3.14") == 3.14
    assert _parse_argument("true") is True
    assert _parse_argument("false") is False
    assert _parse_argument("hello") == "hello"

# Additional tests for edge cases, JSON parsing, and more

if __name__ == "__main__":
    pytest.main()
