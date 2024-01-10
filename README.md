# Quick Start Guide: Open-Source CLI Tool

_Note: This repo is theoretical and only for learning purposes. It is not meant for production use or pretty much any use other than to review the design pattern._

## Introduction

Welcome to the open-source CLI tool, abstract-command-cli a versatile and extensible utility for executing a sequence of commands with customizable keyword arguments. This guide will help you get started with the tool and provide comprehensive usage examples.

## Installation

You can easily install the tool using pip:

```bash
pip install abstract-command-cli
```

## Usage

## Basic Usage

Execute a single command with custom keyword arguments:

```bash
abstract-command-cli function1 --arg1=42 --arg2=hello
```

### Multiple Commands

Execute multiple commands in sequence with different keyword arguments:

```bash
abstract-command-cli --commands "function1 --arg1=42" \
                      "function2 --arg2=hello" \
                      "function3 --arg1=100 --arg2=world" \
                      "function2 --arg2=custom_string" \
                      "function1 --arg3=False" \
                      "function3 --arg1=50.5 --arg2=example"

```

### Global Arguments

Use global arguments that apply to all commands:

```bash
abstract-command-cli --commands "function1 --arg1=42" \
                      "function2 --arg2=hello" \
                      "function3 --arg1=100 --arg2=world" \
                      "function2 --arg2=custom_string" \
                      "function1 --arg3=False" \
                      "function3 --arg1=50.5 --arg2=example" \
                      --arg1 10 --arg2 "global_arg" --arg3 True --arg4 3.14
```

### JSON Payload

Pass all CLI arguments, including global keyword arguments, multiple commands, and any number of custom keyword arguments, as a JSON payload:

```bash
abstract-command-cli --json-payload '{"commands": ["function1 --arg1=42", "function2 --arg2=hello"], "global_kwargs": {"arg1": 10, "arg2": "global_arg", "arg3": true, "arg4": 3.14}}'
```

## Comprehensive Examples

### Example 1: Execute Multiple Commands with JSON Payload

```bash
abstract-command-cli --json-payload '{"commands": ["function1 --arg1=42", "function2 --arg2=hello"], "global_kwargs": {"arg1": 10, "arg2": "global_arg", "arg3": true, "arg4": 3.14}}'
```

In this example, we execute multiple commands in sequence, including global keyword arguments and custom keyword arguments passed as a JSON payload.

### Example 2: Custom Keyword Arguments with JSON Payload

```bash
abstract-command-cli --json-payload '{"commands": ["function1 --arg1=42"], "global_kwargs": {"arg1": 10, "arg2": "global_arg", "arg3": true, "arg4": 3.14}, "custom_arg": "custom_value"}'
```

This example demonstrates how to execute a single command with custom keyword arguments and global keyword arguments using a JSON payload.

## Design Values

Aggregating custom scripts into a singular Python package can be beneficial in various organizational and technical use cases, especially when these scripts/functions are developed adhoc-ly in various team silos and need to be orchestrated through a workflow tool using data from sources like AWS S3 or Redshift. Here are some scenarios where such aggregation is advantageous:

### Organizational Design Use Cases

Standardization and Consistency: In a large organization with multiple engineering teams, standardizing scripts into a single package ensures consistency in coding style, libraries, and dependencies. It helps maintain a common set of coding practices and standards across teams.

**Version Control:** Managing multiple individual scripts can become challenging when it comes to version control. Packaging scripts into a single Python package allows for better version control, ensuring that all scripts are at the same version.

**Collaboration:** When multiple engineers or teams collaborate on a project, having a centralized package simplifies the sharing of code. Engineers can work on different parts of the package and contribute collaboratively.

**Documentation:** Bundling scripts into a package facilitates better documentation practices. Engineers can include comprehensive documentation within the package, making it easier for team members to understand and use the scripts.

**Deployment and Distribution:** When deploying code to various environments or distributing it to multiple users, a packaged solution is more convenient. It simplifies deployment workflows and reduces the likelihood of missing dependencies or configuration issues.

### Technical Use Cases

**Workflow Orchestration:** Many organizations use workflow orchestration tools like Argo, Apache Airflow, Flyte, Prefact, Mage.ai, Windmill or AWS Step Functions to manage and execute data processing pipelines. Packaging scripts as functions within a Python package makes it easier to integrate them into these orchestration workflows.

**Data Processing Pipelines:** When building data pipelines that involve processing data from sources like Amazon S3, packaging scripts can streamline data ingestion, transformation, and storage operations. Engineers can leverage the package's functions within the pipeline steps.

**Reusability:** By creating a package with reusable functions, engineers can avoid duplicating code. These functions can be used across different projects and workflows, saving development time and effort.

**Testing and Debugging:** Packaged scripts are easier to test and debug. Engineers can write unit tests for individual functions and ensure their functionality is maintained across different workflows.

**Scalability:** In situations where the number of scripts or data processing tasks grows, a packaged solution is more scalable. New functions can be added to the package to accommodate additional tasks or use cases.

**Security and Access Control:** Packaging scripts can also help implement access control and security measures more effectively. Engineers can define access permissions and security policies at the package level.

Overall, aggregating custom scripts into a single Python package enhances code organization, maintainability, and scalability. It also aligns well with modern software engineering practices and facilitates integration with workflow orchestration tools, making it an essential approach for managing complex data processing and automation tasks.

## Conclusion

The open-source CLI tool provides flexibility and ease of use for executing commands with customizable keyword arguments. You can execute single or multiple commands, use global arguments, and pass any number of global keyword arguments within a JSON payload.

We welcome contributions and feedback from the community to improve and extend the tool's capabilities.

Thank you for using the open-source CLI tool, and happy scripting!
