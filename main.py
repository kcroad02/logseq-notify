import os
import re
import json
import subprocess
from datetime import datetime
from socket import gethostname

# Determine the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_PATH = os.path.join(SCRIPT_DIR, 'config.json')

home_dir_alt = os.getenv('HOME')
if home_dir_alt:
    # Adjusted to a more generic assets location for the script's config
    ALTERNATIVE_CONFIG_PATH = os.path.join(home_dir_alt, 'storage', 'emulated', '0', 'Logseq', 'assets', 'logseq-task-notifier', 'config.json')
else:
    # Fallback if HOME is not set
    ALTERNATIVE_CONFIG_PATH = os.path.join(SCRIPT_DIR, 'alternative_config.json')

def create_default_config(config_path):
    """Create a default configuration file if it doesn't exist."""
    if not os.path.exists(config_path):
        print(f"Creating default configuration file at {config_path}.")
        default_config = {
            "paths": {
                "default": {
                    "markdown": "",
                    "output_dir": "",
                    "notification_tracker": ""
                }
            }
        }
        
        # Simplified Termux environment check for initial setup guidance
        if gethostname() == 'localhost' or "com.termux" in os.getenv("PREFIX", ""):
            print("Detected Termux environment. Please configure paths for your Logseq files.")
        
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        print(f'Default configuration file created at {config_path}. Please update it with your markdown file path and output directory.')
    else:
        print(f"Configuration file already exists at {config_path}.")

def load_config():
    """Load configuration from the JSON file from both potential paths."""
    config_path_to_try = None
    # Prefer alternative config path if it exists
    if os.path.exists(ALTERNATIVE_CONFIG_PATH):
        print(f"Loading configuration from alternative path: {ALTERNATIVE_CONFIG_PATH}.")
        config_path_to_try = ALTERNATIVE_CONFIG_PATH
    elif os.path.exists(DEFAULT_CONFIG_PATH):
        print(f"Loading configuration from default path (next to script): {DEFAULT_CONFIG_PATH}.")
        config_path_to_try = DEFAULT_CONFIG_PATH
    else:
        print(f"No configuration file found at expected locations.")
        print(f"Attempting to create a default config at: {DEFAULT_CONFIG_PATH}")
        default_dir = os.path.dirname(DEFAULT_CONFIG_PATH)
        # Ensure default_dir is not empty if SCRIPT_DIR is root
        if not os.path.exists(default_dir) and default_dir != "": 
            try:
                os.makedirs(default_dir, exist_ok=True)
                print(f"Created directory for default config: {default_dir}")
            except OSError as e:
                print(f"Error creating directory {default_dir}: {e}")
                return None, None
        
        create_default_config(DEFAULT_CONFIG_PATH)
        if os.path.exists(DEFAULT_CONFIG_PATH):
             print(f"Loading newly created configuration from default path: {DEFAULT_CONFIG_PATH}.")
             config_path_to_try = DEFAULT_CONFIG_PATH
        else:
            print("Failed to create or find a configuration file after attempting creation.")
            return None, None
    
    if config_path_to_try:
        try:
            with open(config_path_to_try, encoding='utf-8') as f: # Added encoding
                return json.load(f), config_path_to_try
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {config_path_to_try}: {e}")
            return None, None
        except IOError as e:
            print(f"Error reading file {config_path_to_try}: {e}")
            return None, None
    return None, None


def save_config(config, config_path):
    """Save configuration to the JSON file."""
    print(f"Saving configuration to {config_path}.")
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f: # Added encoding
            json.dump(config, f, indent=4)
    except IOError as e:
        print(f"Error saving configuration to {config_path}: {e}")


def prompt_for_paths(paths_config_section):
    """Prompt the user to input file paths if they are not already present."""
    home_dir = os.getenv('HOME')
    if not home_dir:
        print("HOME environment variable not set. Cannot determine default paths. Please enter paths manually.")
        paths_config_section['markdown'] = input("Enter the custom markdown file path: ").strip()
        paths_config_section['output_dir'] = input("Enter the custom output directory path (for notification tracker): ").strip()
    else:
        # Adjusted default paths to be more generic within user's Logseq structure
        default_markdown_path = os.path.join(home_dir, 'storage', 'emulated', '0', 'Logseq', 'pages', 'Tasks.md') # Example page name
        default_output_dir = os.path.join(home_dir, 'storage', 'emulated', '0', 'Logseq', 'assets', 'logseq-task-notifier-data')

        def get_user_choice_paths():
            print("Please specify the path to your Logseq Markdown file containing tasks.")
            md_path_choice = input(f"Use default markdown file path ({default_markdown_path})? (Y/n): ").strip().lower()
            final_markdown_path = default_markdown_path if md_path_choice in ['y', ''] else input("Enter the custom markdown file path: ").strip()

            print("\nPlease specify an output directory for this script's data (e.g., notification tracker).")
            output_dir_choice = input(f"Use default output directory ({default_output_dir})? (Y/n): ").strip().lower()
            final_output_dir = default_output_dir if output_dir_choice in ['y', ''] else input("Enter the custom output directory path: ").strip()
            
            return final_markdown_path, final_output_dir

        if not paths_config_section.get('markdown') or not paths_config_section.get('output_dir'):
            paths_config_section['markdown'], paths_config_section['output_dir'] = get_user_choice_paths()
            print(f"Markdown file set to: {paths_config_section['markdown']}")
            print(f"Output directory set to: {paths_config_section['output_dir']}")

    # Derive notification_tracker path if output_dir is set
    output_dir = paths_config_section.get('output_dir')
    if output_dir and not paths_config_section.get('notification_tracker'):
        paths_config_section['notification_tracker'] = os.path.join(output_dir, 'notification_tracker.txt')
        print(f"Notification tracker path set to: {paths_config_section['notification_tracker']}")
    elif not output_dir:
        print("Output directory is not set. Cannot configure notification_tracker.")


def get_task_file_paths(config):
    """Return file paths based on configuration and prompt user for required inputs."""
    if 'paths' not in config or 'default' not in config['paths']:
        print("Configuration 'paths' or 'paths.default' section is missing. Initializing.")
        config['paths'] = config.get('paths', {})
        config['paths']['default'] = {
            "markdown": "",
            "output_dir": "",
            "notification_tracker": ""
        }
    
    paths_section = config['paths']['default']
    
    if not paths_section.get('markdown') or not paths_section.get('output_dir'):
        prompt_for_paths(paths_section) # This will also derive notification_tracker if output_dir is set

    return paths_section


def parse_task_line(line):
    """Extract task description from a line."""
    match = re.match(r"- TODO (.+)", line) # Assumes tasks start with "- TODO "
    return match.group(1).strip() if match else None

def parse_scheduled_line(line):
    """Extract date and time from a scheduling line."""
    # Example: SCHEDULED: <2023-10-26 Thu 10:00>
    date_match = re.search(r"SCHEDULED:.*?<(\d{4}-\d{2}-\d{2})", line)
    time_match = re.search(r"(\d{2}:\d{2})", line) # Extracts time if present alongside date
    
    scheduled_date = date_match.group(1) if date_match else None
    scheduled_time = time_match.group(1) if time_match else "00:00" # Default time if only date is present
    return scheduled_date, scheduled_time

def send_termux_notification(title, body):
    """Send a notification using Termux."""
    print(f"Sending Termux notification with title: '{title}' and body: '{body}'.")
    try:
        result = subprocess.run(['termux-notification', '--title', title, '--content', body, '--priority', 'high'], 
                                check=False, capture_output=True, text=True) # Added priority
        if result.returncode == 0:
            print("Notification sent successfully via Termux.")
        else:
            print(f"Failed to send notification via Termux. Return code: {result.returncode}")
            print(f"Stderr: {result.stderr}")
            if "No such file or directory" in result.stderr or "not found" in result.stderr:
                 print("Hint: Is the Termux:API app installed and 'termux-notification' command accessible from PATH?")
    except FileNotFoundError:
        print("Error: termux-notification command not found. Is Termux:API app installed and configured correctly?")
        print("Ensure 'termux-api' package is installed in Termux and Termux:API app is installed on Android.")
    except Exception as e: 
        print(f"An unexpected error occurred while sending Termux notification: {e}")


def should_send_notification(tracker_file, task_unique_id):
    """Determine if the notification should be sent based on the tracker file."""
    if not tracker_file: # Safety check
        print("Error: Notification tracker file path is not configured. Cannot track/send notifications.")
        return False

    tracker_dir = os.path.dirname(tracker_file)
    # Ensure tracker_dir is not empty
    if not os.path.exists(tracker_dir) and tracker_dir != "":
        try:
            os.makedirs(tracker_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory for tracker file {tracker_dir}: {e}")
            return False

    sent_notifications = set()
    if os.path.exists(tracker_file):
        try:
            with open(tracker_file, 'r', encoding='utf-8') as f: # Added encoding
                sent_notifications = set(line.strip() for line in f)
        except IOError as e:
            print(f"Error reading tracker file {tracker_file}: {e}")
            # Continue, assuming it's okay to try sending if read fails,
            # as a new tracker file might be created or an existing one might be temporarily inaccessible.
            
    if task_unique_id in sent_notifications:
        print(f"Notification already sent for this task ID: {task_unique_id}.")
        return False
    
    try:
        with open(tracker_file, 'a', encoding='utf-8') as f: # Added encoding
            f.write(task_unique_id + '\n')
        print(f"Notification for task ID {task_unique_id} marked as sent.")
        return True
    except IOError as e:
        print(f"Error writing to tracker file {tracker_file}: {e}")
        return False


def truncate_task_description(task_description, trunc_length):
    """Truncate the task description, preferring word boundaries."""
    if len(task_description) <= trunc_length:
        return task_description
    
    # Ensure trunc_length is at least 3 for "..."
    if trunc_length < 3:
        return "..."[:trunc_length]

    # Reserve space for "..."
    effective_trunc_length = trunc_length - 3
    
    # Truncate then find last space
    truncated = task_description[:effective_trunc_length]
    last_space = truncated.rfind(' ')
    
    if last_space != -1: # If a space is found
        return truncated[:last_space] + "..."
    else: # No space found, hard truncate
        return truncated + "..."

def main():
    print("Starting Logseq Task Notifier script.")
    
    config, config_path = load_config()
    if config is None or config_path is None: 
        print("Failed to load or create configuration. Aborting.")
        return 1

    # Ensure paths section exists, prompt if necessary
    if 'paths' not in config or 'default' not in config['paths'] or \
       not config['paths']['default'].get('markdown') or \
       not config['paths']['default'].get('output_dir'):
        print("Configuration for 'markdown' or 'output_dir' is missing. Prompting for setup.")
        # get_task_file_paths will prompt and update config in-memory
        paths_config = get_task_file_paths(config) 
        save_config(config, config_path) # Save after prompting
    else:
        paths_config = config['paths']['default']
        # Ensure notification_tracker is derived if output_dir exists but tracker doesn't
        if paths_config.get('output_dir') and not paths_config.get('notification_tracker'):
            paths_config['notification_tracker'] = os.path.join(paths_config['output_dir'], 'notification_tracker.txt')
            print(f"Derived Notification tracker path: {paths_config['notification_tracker']}")
            save_config(config, config_path)


    markdown_file = paths_config.get('markdown')
    output_dir = paths_config.get('output_dir')
    notification_tracker_file = paths_config.get('notification_tracker')

    print(f"Using Markdown file: {markdown_file}")
    print(f"Using Output directory (for tracker): {output_dir}")
    print(f"Using Notification tracker file: {notification_tracker_file}")
    
    if not all([markdown_file, output_dir, notification_tracker_file]):
        print("Critical path configuration is missing (markdown, output_dir, or notification_tracker). Please check configuration. Aborting.")
        return 1
        
    try:
        # Only ensure output_dir exists (for notification_tracker.txt)
        if not os.path.exists(output_dir) and output_dir != "":
            os.makedirs(output_dir, exist_ok=True)
            print(f"Created output directory: {output_dir}")
    except OSError as e:
        print(f"Error creating output directory {output_dir}: {e}. Aborting.")
        return 1
        
    now = datetime.now()
    
    if not os.path.exists(markdown_file):
        print(f"Markdown file not found at {markdown_file}. Aborting.")
        return 1
    
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except IOError as e:
        print(f"Error reading markdown file {markdown_file}: {e}. Aborting.")
        return 1
    
    tasks_found = []
    
    i = 0
    while i < len(lines):
        line_content = lines[i].strip()
        # Support both common Logseq TODO formats
        if line_content.startswith(('- TODO', 'TODO')):
            task_desc = parse_task_line(line_content)
            if not task_desc: 
                i += 1
                continue

            scheduled_dt_obj = None
            # Check current line and next line for SCHEDULED pattern
            for j in range(i, min(i + 2, len(lines))): 
                current_check_line = lines[j].strip()
                if 'SCHEDULED:' in current_check_line:
                    s_date_str, s_time_str = parse_scheduled_line(current_check_line)
                    if s_date_str:
                        try:
                            full_datetime_str = f'{s_date_str} {s_time_str}'
                            scheduled_dt_obj = datetime.strptime(full_datetime_str, '%Y-%m-%d %H:%M')
                            # If SCHEDULED was on the next line, advance main loop counter
                            if j == i + 1: 
                                i +=1 
                            break # Found scheduled info for this TODO
                        except ValueError as e:
                            print(f"Warning: Could not parse date/time for task '{task_desc}': {e}. Line: '{current_check_line}'")
            
            task_id_str_part = scheduled_dt_obj.isoformat() if scheduled_dt_obj else "NoDate"
            # Sanitize task_desc for use in ID
            sanitized_task_desc = re.sub(r'[^\w\s-]', '', task_desc).strip().replace(' ', '_')
            # Truncate sanitized desc for ID
            task_unique_id = f"{sanitized_task_desc[:50]}_{task_id_str_part}" 

            tasks_found.append({'description': task_desc, 'datetime': scheduled_dt_obj, 'id': task_unique_id})
        i += 1
    
    # Sort tasks: those with datetime first, then by datetime, then by original order (implicit via stable sort)
    tasks_found.sort(key=lambda x: (x['datetime'] is None, x['datetime'] if x['datetime'] else datetime.max))
    
    print(f"Found {len(tasks_found)} TODO tasks.")

    # Process tasks for notifications
    for task in tasks_found:
        task_description_orig = task['description']
        scheduled_date_time_obj = task['datetime']
        task_id = task['id']
    
        if scheduled_date_time_obj and scheduled_date_time_obj > now:
            time_difference_seconds = (scheduled_date_time_obj - now).total_seconds()
            # Notify if due within 3 minutes (180 seconds)
            if 0 <= time_difference_seconds <= 180:
                if should_send_notification(notification_tracker_file, task_id):
                    notif_title = 'Task Reminder'
                    # Truncate description for notification body
                    notif_body_desc = truncate_task_description(task_description_orig, 60) 
                    notif_body = f"{notif_body_desc} is due at {scheduled_date_time_obj.strftime('%H:%M')}!"
                    send_termux_notification(notif_title, notif_body)
    
    print("Script finished processing tasks for notifications.")
    return 0

if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)