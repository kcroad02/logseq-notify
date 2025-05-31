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
    ALTERNATIVE_CONFIG_PATH = os.path.join(home_dir_alt, 'storage', 'emulated', '0', 'Logseq', 'assets', 'logseq-notify-android', 'config.json')
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
                    "pushWidget_target": "",
                    "notification_tracker": ""
                }
            }
        }
        
        # Check for Termux environment
        if gethostname() == 'localhost' or "com.termux" in os.getenv("PREFIX", ""):
            is_termux_user = input("Are you using Termux on an Android device? (Y/n): ").strip().lower()
            if is_termux_user in ['y', '']:
                pass
        
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        print(f'Default configuration file created at {config_path}. Please update it with your markdown file paths.')
    else:
        print(f"Configuration file already exists at {config_path}.")

def load_config():
    """Load configuration from the JSON file from both potential paths."""
    config_path_to_try = None
    if os.path.exists(ALTERNATIVE_CONFIG_PATH):
        print(f"Loading configuration from alternative path: {ALTERNATIVE_CONFIG_PATH}.")
        config_path_to_try = ALTERNATIVE_CONFIG_PATH
    elif os.path.exists(DEFAULT_CONFIG_PATH):
        print(f"Loading configuration from default path: {DEFAULT_CONFIG_PATH}.")
        config_path_to_try = DEFAULT_CONFIG_PATH
    else:
        print(f"No configuration file found. Attempting to create one at default path: {DEFAULT_CONFIG_PATH}")
        default_dir = os.path.dirname(DEFAULT_CONFIG_PATH)
        if not os.path.exists(default_dir):
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
            print("Failed to create or find a configuration file.")
            return None, None
    
    if config_path_to_try:
        try:
            with open(config_path_to_try) as f:
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
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
    except IOError as e:
        print(f"Error saving configuration to {config_path}: {e}")


def prompt_for_paths(paths_config_section):
    """Prompt the user to input file paths if they are not already present."""
    home_dir = os.getenv('HOME')
    if not home_dir:
        print("HOME environment variable not set. Cannot determine default paths.")
        paths_config_section['markdown'] = input("Enter the custom markdown file path: ").strip()
        paths_config_section['output_dir'] = input("Enter the custom output directory path: ").strip()
    else:
        default_markdown_path = os.path.join(home_dir, 'Sync', 'Logseq', 'pages', 'Logpush.md')
        default_output_dir = os.path.join(home_dir, 'Sync', 'Logseq', 'assets', 'logpush')

        def get_user_choice():
            choice = input(f"Use default markdown file ({default_markdown_path}) and output directory ({default_output_dir})? (Y/n): ").strip().lower()
            if choice in ['y', '']:
                return default_markdown_path, default_output_dir
            elif choice == 'n':
                custom_markdown = input("Enter the custom markdown file path: ").strip()
                custom_output_dir = input("Enter the custom output directory path: ").strip()
                return custom_markdown, custom_output_dir
            else:
                print("Invalid choice. Please try again.")
                return get_user_choice()

        if not paths_config_section.get('markdown'): 
            paths_config_section['markdown'], paths_config_section['output_dir'] = get_user_choice()
            print(f"Markdown file set to: {paths_config_section['markdown']}")
            print(f"Output directory set to: {paths_config_section['output_dir']}")

    output_dir = paths_config_section.get('output_dir') 
    if output_dir: 
        paths_config_section['pushWidget_target'] = os.path.join(output_dir, 'pushWidget')
        paths_config_section['notification_tracker'] = os.path.join(output_dir, 'notification_tracker.txt')
        print(f"PushWidget target set to: {paths_config_section['pushWidget_target']}")
        print(f"Notification tracker set to: {paths_config_section['notification_tracker']}")
    else:
        print("Output directory is not set. Cannot configure pushWidget_target and notification_tracker.")


def get_task_file_paths(config):
    """Return file paths based on configuration and prompt user for required inputs."""
    if 'paths' not in config or 'default' not in config['paths']:
        print("Configuration 'paths' or 'paths.default' section is missing. Initializing.")
        config['paths'] = config.get('paths', {}) 
        config['paths']['default'] = config['paths'].get('default', {
            "markdown": "",
            "output_dir": "",
            "pushWidget_target": "",
            "notification_tracker": ""
        })
    
    paths_section = config['paths']['default']
    print(f"Current paths configuration: {paths_section}")
    
    if not paths_section.get('markdown') or not paths_section.get('output_dir'):
        prompt_for_paths(paths_section)

    return paths_section


def parse_task_line(line):
    """Extract task description from a line."""
    match = re.match(r"- TODO (.+)", line)
    return match.group(1) if match else None

def parse_scheduled_line(line):
    """Extract date and time from a scheduling line."""
    date_match = re.search(r"SCHEDULED: <(\d{4}-\d{2}-\d{2})", line)
    time_match = re.search(r"(\d{2}:\d{2})", line) 
    scheduled_date = date_match.group(1) if date_match else None
    scheduled_time = time_match.group(1) if time_match else "00:00" # Default time if only date is present
    return scheduled_date, scheduled_time

def write_task_file(task_content, index, output_dir_for_widget):
    """Write task information to a file."""
    file_path = os.path.join(output_dir_for_widget, f"pushWidget{index}.txt")
    print(f"Writing task to {file_path}.")
    try:
        with open(file_path, 'w') as f:
            f.write(task_content)
    except IOError as e:
        print(f"Error writing task file {file_path}: {e}")


def send_termux_notification(title, body):
    """Send a notification using Termux."""
    print(f"Sending Termux notification with title: '{title}' and body: '{body}'.")
    try:
        result = subprocess.run(['termux-notification', '--title', title, '--content', body], 
                                check=False, capture_output=True, text=True)
        if result.returncode == 0:
            print("Notification sent successfully via Termux.")
        else:
            print(f"Failed to send notification via Termux. Return code: {result.returncode}")
            print(f"Stderr: {result.stderr}")
            print(f"Stdout: {result.stdout}")
            if "No such file or directory" in result.stderr or "not found" in result.stderr:
                 print("Hint: Is the Termux:API app installed and 'termux-notification' accessible?")
    except FileNotFoundError:
        print("Error: termux-notification command not found. Is Termux:API app installed and configured correctly?")
        print("Ensure 'termux-api' package is installed in Termux and Termux:API app is installed on Android.")
    except Exception as e: 
        print(f"An unexpected error occurred while sending Termux notification: {e}")


def should_send_notification(tracker_file, task_unique_id):
    """Determine if the notification should be sent based on the tracker file."""
    tracker_dir = os.path.dirname(tracker_file)
    if not os.path.exists(tracker_dir):
        try:
            os.makedirs(tracker_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory for tracker file {tracker_dir}: {e}")
            return False 

    sent_notifications = set()
    if os.path.exists(tracker_file):
        try:
            with open(tracker_file, 'r') as f:
                sent_notifications = set(line.strip() for line in f)
        except IOError as e:
            print(f"Error reading tracker file {tracker_file}: {e}")
            
    if task_unique_id in sent_notifications:
        print(f"Notification already sent for this task ID: {task_unique_id}.")
        return False
    
    try:
        with open(tracker_file, 'a') as f: 
            f.write(task_unique_id + '\n')
        print(f"Notification for task ID {task_unique_id} marked as sent.")
        return True
    except IOError as e:
        print(f"Error writing to tracker file {tracker_file}: {e}")
        return False 


def truncate_task_description(task_description, trunc_length):
    """Truncate the task description without cutting off words improperly and ensuring ellipsis fit."""
    if len(task_description) <= trunc_length:
        return task_description
    
    if trunc_length < 3: # Ensure trunc_length is at least 3 for "..."
        return "..."[:trunc_length] 

    end = trunc_length - 3 # Reserve space for "..."
    
    effective_end = end
    while effective_end > 0 and task_description[effective_end] != ' ':
        effective_end -= 1
    
    if effective_end == 0:  # No space found, hard truncate
        truncated = task_description[:end].strip()
    else: # Space found
        truncated = task_description[:effective_end].strip()

    return truncated + '...'


def format_date(dt_obj):
    """Format the date without leading zeros in the month and day (e.g., 5/1/24)."""
    try: # For platforms not supporting '%-' (like Windows sometimes)
        formatted_date = dt_obj.strftime('%-m/%-d/%y')
    except ValueError: # Fallback for systems that don't support '%-'
        month = str(dt_obj.month)
        day = str(dt_obj.day)
        year = dt_obj.strftime('%y')
        formatted_date = f"{month}/{day}/{year}"
    return formatted_date


def pad_task_description_with_date(description, formatted_dt, total_display_length):
    """Pad the task description with spaces to ensure it and the date fit to the specified total length."""
    content_len = len(description) + len(formatted_dt) + 3  # +3 for " ()"
    
    if content_len > total_display_length:
        extra_chars = content_len - total_display_length
        if len(description) > extra_chars:
            description = description[:len(description) - extra_chars -1] + "~" # Indicate further truncation
        else: 
            description = "~" 
        padded_task = f'{description} ({formatted_dt})'
    else:
        space_needed = total_display_length - content_len
        padded_task = f'{description}{" " * space_needed} ({formatted_dt})'
    
    return padded_task


def main():
    print("Starting script.")
    
    config, config_path = load_config()
    if config is None or config_path is None: 
        print("Failed to load or create configuration. Aborting.")
        return 
    
    if 'paths' not in config or 'default' not in config['paths']:
        print("Configuration 'paths' or 'paths.default' section is missing. Initializing and prompting.")
        config['paths'] = config.get('paths', {})
        config['paths']['default'] = {
            "markdown": "", "output_dir": "",
            "pushWidget_target": "", "notification_tracker": ""
        }
        prompt_for_paths(config['paths']['default'])
        save_config(config, config_path) 

    paths_config = get_task_file_paths(config) 

    if not paths_config.get('markdown') or not paths_config.get('output_dir'):
         pass # config is already updated in-memory by prompt_for_paths

    markdown_file = paths_config.get('markdown')
    output_dir = paths_config.get('output_dir')

    if output_dir:
        pushWidget_target_dir = paths_config.get('pushWidget_target')
        notification_tracker_file = paths_config.get('notification_tracker')
        if not pushWidget_target_dir: 
            pushWidget_target_dir = os.path.join(output_dir, 'pushWidget')
            paths_config['pushWidget_target'] = pushWidget_target_dir
        if not notification_tracker_file:
            notification_tracker_file = os.path.join(output_dir, 'notification_tracker.txt')
            paths_config['notification_tracker'] = notification_tracker_file
    else: 
        pushWidget_target_dir = None
        notification_tracker_file = None

    save_config(config, config_path)

    print(f"Markdown file path: {markdown_file}")
    print(f"Output directory path: {output_dir}")
    print(f"PushWidget target path: {pushWidget_target_dir}")
    print(f"Notification tracker path: {notification_tracker_file}")
    
    if not all([markdown_file, output_dir, pushWidget_target_dir, notification_tracker_file]):
        print("One or more required paths are not set. Please check configuration file. Aborting.")
        return
        
    try:
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(pushWidget_target_dir, exist_ok=True) 
    except OSError as e:
        print(f"Error creating output directories: {e}. Aborting.")
        return
        
    now = datetime.now()
    
    if not os.path.exists(markdown_file):
        print(f"Markdown file not found at {markdown_file}. Aborting.")
        return
    
    try:
        with open(markdown_file) as f:
            lines = f.readlines()
    except IOError as e:
        print(f"Error reading markdown file {markdown_file}: {e}. Aborting.")
        return
    
    max_tasks_for_widget = 5 
    widget_line_total_length = 40  
    tasks_found = [] 
    
    i = 0
    while i < len(lines):
        line_content = lines[i].strip()
        if line_content.startswith('- TODO'):
            task_desc = parse_task_line(line_content)
            if not task_desc: 
                i += 1
                continue

            scheduled_dt_obj = None
            next_line_index = i + 1
            if next_line_index < len(lines):
                next_line_content = lines[next_line_index].strip()
                if 'SCHEDULED:' in next_line_content:
                    s_date_str, s_time_str = parse_scheduled_line(next_line_content)
                    if s_date_str:
                        try:
                            full_datetime_str = f'{s_date_str} {s_time_str}'
                            scheduled_dt_obj = datetime.strptime(full_datetime_str, '%Y-%m-%d %H:%M')
                        except ValueError as e:
                            print(f"Warning: Could not parse date/time for task '{task_desc}': {e}. Date string: {s_date_str}, Time string: {s_time_str}")
                    i += 1 
            
            task_id_str_part = scheduled_dt_obj.isoformat() if scheduled_dt_obj else "NoDate"
            task_unique_id = f"{task_desc}_{task_id_str_part}"

            tasks_found.append({'description': task_desc, 'datetime': scheduled_dt_obj, 'id': task_unique_id})
            print(f"Task added: '{task_desc}', Scheduled: {scheduled_dt_obj if scheduled_dt_obj else 'None'}, ID: {task_unique_id}")
        i += 1
    
    tasks_found.sort(key=lambda x: (x['datetime'] is None, x['datetime'] or datetime.max))
    
    for idx in range(max_tasks_for_widget):
        display_line_for_widget: str
        if idx < len(tasks_found):
            current_task = tasks_found[idx]
            task_description_orig = current_task['description']
            scheduled_date_time_obj = current_task['datetime']
            task_id = current_task['id'] 
    
            if scheduled_date_time_obj:
                date_str_formatted = format_date(scheduled_date_time_obj)
                len_for_date_part = len(date_str_formatted) + 3 
                max_desc_len_with_date = widget_line_total_length - len_for_date_part
                
                desc_truncated = truncate_task_description(task_description_orig, max_desc_len_with_date)
                display_line_for_widget = pad_task_description_with_date(desc_truncated, date_str_formatted, widget_line_total_length)
    
                if scheduled_date_time_obj > now : 
                    time_difference_seconds = (scheduled_date_time_obj - now).total_seconds()
                    if 0 <= time_difference_seconds <= 180: # Due soon
                        if should_send_notification(notification_tracker_file, task_id):
                            notif_title = 'Task Reminder'
                            notif_body_desc = truncate_task_description(task_description_orig, 60) 
                            notif_body = f"{notif_body_desc} is due at {scheduled_date_time_obj.strftime('%H:%M')}!"
                            send_termux_notification(notif_title, notif_body)
            else: 
                desc_truncated = truncate_task_description(task_description_orig, widget_line_total_length)
                display_line_for_widget = desc_truncated.ljust(widget_line_total_length) 
        else: 
            display_line_for_widget = ' ' * widget_line_total_length
        
        write_task_file(display_line_for_widget, idx, pushWidget_target_dir)
    
    print("Script finished.")

if __name__ == '__main__':
    main()