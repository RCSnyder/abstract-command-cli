# Contributing Developer Guide: Extending the Functionality

## Introduction

This guide explains how to extend the functionality of our Python CLI package by adding your own custom function classes or by extending the BaseFunction class. Custom function classes allow you to define specific operations or tasks that can be executed through the CLI, making your CLI tool more versatile and tailored to your needs.

## When to Add Your Own Function Class

You may consider adding your own function class in the following situations:

1. Unique Operations: When you need to perform unique operations that are not covered by the existing function classes.

2. Custom Workflow: When you want to define a custom workflow involving multiple commands executed in a specific order.

3. Specialized Tasks: If your application requires specialized tasks with unique keyword arguments and behavior.
