import sys
from datetime import datetime, timedelta
from jira import JIRA
from colorama import Fore, Style, init
import os
import calendar  

# Replace with your Jira server URL, email, and token
jira_server = "YOUR_JIRA_URL"
jira_email = "YOUR_EMAIL"
jira_token = "YOUR_JIRA_API_TOKEN" #How to: https://docs.searchunify.com/Content/Content-Sources/Atlassian-Jira-Confluence-Authentication-Create-API-Token.htm
# Replace with your project key
project_key = "PROJECT_KEY"


# Connect to Jira
jira_options = {"server": jira_server}
jira = JIRA(options=jira_options, basic_auth=(jira_email, jira_token))

# Function to create an issue
def create_issue(summary, start_date, due_date, priority, epic_link, description=None):
    issue_dict = {
        "project": {"key": project_key},
        "summary": summary,
        "issuetype": {"name": "Task"},
        "duedate": due_date,
        "priority": {"name": priority},
    }
    if epic_link:
        issue_dict["customfield_XXXXX"] = epic_link  # Replace XXXXX with the actual custom field ID for Epic Link, feel free to modify to whatever custom field you like

    if description:
        issue_dict["description"] = description

    jira.create_issue(fields=issue_dict)

# Function to get available Epics in the project
def get_available_epics():
    jql_query = f'project = "{project_key}" AND issuetype = Epic'
    return jira.search_issues(jql_query)

from colorama import Fore, Style, init
import os

# Initialize colorama
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("""
   $$$$$\ $$\                           $$$$$$\  $$\       $$$$$$\ 
   \__$$ |\__|                         $$  __$$\ $$ |      \_$$  _|
      $$ |$$\  $$$$$$\  $$$$$$\        $$ /  \__|$$ |        $$ |  
      $$ |$$ |$$  __$$\ \____$$\       $$ |      $$ |        $$ |  
$$\   $$ |$$ |$$ |  \__|$$$$$$$ |      $$ |      $$ |        $$ |  
$$ |  $$ |$$ |$$ |     $$  __$$ |      $$ |  $$\ $$ |        $$ |  
\$$$$$$  |$$ |$$ |     \$$$$$$$ |      \$$$$$$  |$$$$$$$$\ $$$$$$\ 
 \______/ \__|\__|      \_______|       \______/ \________|\______|
    \n""")

    weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    current_date = datetime.now()

    # Get available Epics in the project
    epics = get_available_epics()
    print(Fore.GREEN + "Available Epics:" + Style.RESET_ALL)
    for i, epic in enumerate(epics, start=1):
        print(f"{i}. {epic.key} - {epic.fields.summary}")
    print()

    try:
        num_days = int(input("Enter the number of business days you want to plan ahead: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    business_days = 0
    days_passed = 0

    while business_days < num_days:
        current_weekday = (current_date + timedelta(days=days_passed)).weekday()
        day = calendar.day_name[current_weekday]  # Use calendar module to get the name of the current day
        start_date = (current_date + timedelta(days=days_passed)).strftime("%Y-%m-%d")

        if current_weekday != 4 and current_weekday != 5:
            # Check if the user wants to skip the day
            print()

            skip_day = input(f"Do you want to skip tasks for {day}? (y/n) ").lower()
            if skip_day != "y":
                tasks = input(f"What are you planning to start on {day}? (Separate tasks with a ';') ")

                for task in tasks.split(';'):
                    task_info = task.strip().split('|')
                    task_desc = task_info[0].strip()
                    if not task_desc:
                        continue

                    duration = int(task_info[1].strip()) if len(task_info) > 1 else 0
                    due_date = (current_date + timedelta(days=days_passed + duration)).strftime("%Y-%m-%d")

                    priority = input(f"Enter the priority for '{task_desc}' (e.g. Blocker(b), High (h), Medium(m), Low(l)): ")

                    if priority.lower() == "l":
                        priority = "Low"

                    elif priority.lower() == "m":
                        priority = "Medium"

                    elif priority.lower() == "h":
                        priority = "High"

                    elif priority.lower() == "b":
                        priority = "Blocker"

                    # Prompt the user to choose an Epic or skip
                    epic_choice = int(input(f"Enter the number of the Epic for '{task_desc}' or 0 to skip: "))
                    epic_link = epics[epic_choice - 1].key if epic_choice > 0 else None

                    # Ask the user if they want to add a description
                    add_description = input(f"Do you want to add a description for '{task_desc}'? (y/n) ").lower()
                    description = None
                    if add_description == "y":
                        description = input("Enter the description: ")

                    create_issue(task_desc, start_date, due_date, priority, epic_link, description)

            business_days += 1

        if current_weekday == 3:  # If it's Friday, skip Saturday and jump to Sunday
            days_passed += 3

        else:
            days_passed += 1

if __name__ == "__main__":
    main()
