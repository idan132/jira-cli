# Jira-CLI
This tool is a Python-based command-line interface (CLI) designed to help users manage tasks in Jira. The purpose of this tool is to allow users to plan their tasks for a specified number of business days in advance, automatically creating Jira issues based on the user's input, instead of creating one ticket after another using the tedious UI Jira offers.

## Installation 
1- Make sure you have Python3 installed on your machine

2- Run the following command: pip3 install jira (library for querying Jira's api easily using Python)

3- Run the following command: pip3 install colorama

4- Sync the code with your details: server, user name, api key, project key 

Thats it! You are ready to run and use the script

## Usage
#### To use the tool:

Run the script in a terminal or command prompt.
The script will display a title "Jira CLI" and list available Epics in the given Jira project.
The user will be prompted to enter the number of business days they want to plan ahead.
For each business day, the user will be asked if they want to skip tasks for that day. If not, they can enter their tasks for that day.
Tasks should be separated by a semicolon (;)
Users can add an optional duration (in business days) for each task by appending "| X" to the task description, where X is the number of days required to complete the task. If not specified, the due date will be set to the same day.
For each task, the user will be prompted to enter its priority (e.g., High, Medium, Low).
The user will be asked to choose an Epic for each task by entering the corresponding number or entering 0 to skip linking the task to an Epic.
The script will create a Jira issue for each task with the provided information, including task description, start date, due date, priority, and Epic link (if chosen).
By following these steps, the user can efficiently plan and manage their tasks in Jira using this CLI tool.

### Enjoy :)
