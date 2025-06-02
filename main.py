#!/usr/bin/env python3

import os
import re
import json
import subprocess
from datetime import datetime
# from socket import gethostname # Not strictly needed anymore for path logic

# --- Constants ---
APP_NAME = "logseq_notifier_md"
CONFIG_FILE_NAME = "config_markdown.json"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Determine if running in Termux
IS_TERMUX = "com.termux" in os.getenv("PREFIX", "")

# Path for user-specific configuration (preferred on PC)
USER_CONFIG_DIR_PC = os.path.join(os.path.expanduser("~"), 'logseq', 'graphs', 'Omni', 'assets'
USER_CONFIG_PATH_PC = os.path.join(USER_CONFIG_DIR_PC, CONFIG_FILE_NAME)

# Path for configuration local to the script (fallback or for Termux/portable use)
LOCAL_CONFIG_PATH = os.path.join(SCRIPT_DIR, CONFIG_FILE_NAME)
# --- End Constants ---

def create_default_config(config_path, is_termux_env):
    """Create a default configuration file if it doesn't exist."""
    if not os.path.exists(config_path):
        print(f"Creating default Markdown version configuration file at {config_path}.")
        default_config = {
            "paths": {
                "default": {
                    "markdown": "",
                    "output_dir": "",
                    "notification_tracker": "",
                    "ntfy_topic": ""
                }
            }
        }
        
        home_dir = os.path.expanduser("~") # Use expanduser for broader compatibility

        if is_termux_env:
            print("Detected Termux environment. Suggesting default paths for Termux.")
            if home_dir: # HOME is usually set in Termux
                default_config["paths"]["default"]["markdown"] = os.path.join(home_dir, 'storage', 'shared', 'logseq', 'graphs', 'Omni', 'pages', 'Tasks.md')
                # Points directly to asserts assets
                default_config["paths"]["default"]["output_dir"] = os.path.join(home_dir, 'storage', 'shared', 'logseq', 'graphs', 'Omni', 'assets')
        else: # PC environment
            print("Detected PC environment. Suggesting default paths for PC.")
            default_config["paths"]["default"]["output_dir"] = os.path.join(home_dir, 'logseq', 'graphs', 'Omni', 'assets')
        
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4)
            print(f'Default configuration file created at {config_path}. Please review and update it, especially the "markdown" path if it is empty or "Omni"/"YourGraphName" is not your graph name or paths differ.')
        except IOError as e:
            print(f"Error creating default configuration file {config_path}: {e}")
    else:
        print(f"Configuration file already exists at {config_path}.")

def load_config():
    """Load configuration from the JSON file, preferring PC user path then local path."""
    config_to_load = None
    loaded_path = None

    if not IS_TERMUX and os.path.exists(USER_CONFIG_PATH_PC):
        print(f"Loading Markdown config from user path: {USER_CONFIG_PATH_PC}.")
        config_to_load = USER_CONFIG_PATH_PC
    elif os.path.exists(LOCAL_CONFIG_PATH):
        print(f"Loading Markdown config from local script path: {LOCAL_CONFIG_PATH}.")
        config_to_load = LOCAL_CONFIG_PATH
    else:
        print(f"No Markdown configuration file found at user path ('{USER_CONFIG_PATH_PC}') or local script path ('{LOCAL_CONFIG_PATH}').")
        
        path_to_create_at = LOCAL_CONFIG_PATH 
        if not IS_TERMUX:
            path_to_create_at = USER_CONFIG_PATH_PC
        
        print(f"Attempting to create a default Markdown config at: {path_to_create_at}")
        create_default_config(path_to_create_at, IS_TERMUX)

        if os.path.exists(path_to_create_at):
            print(f"Loading newly created Markdown configuration from: {path_to_create_at}.")
            config_to_load = path_to_create_at
        elif not IS_TERMUX and path_to_create_at == USER_CONFIG_PATH_PC and not os.path.exists(LOCAL_CONFIG_PATH):
            print(f"Failed to create at user path, attempting to create at local script path: {LOCAL_CONFIG_PATH}")
            create_default_config(LOCAL_CONFIG_PATH, IS_TERMUX) 
            if os.path.exists(LOCAL_CONFIG_PATH):
                print(f"Loading newly created Markdown configuration from local script path: {LOCAL_CONFIG_PATH}.")
                config_to_load = LOCAL_CONFIG_PATH
            else:
                print("Failed to create any Markdown configuration file.")
                return None, None
        else:
            print("Failed to create or find a Markdown configuration file after creation attempts.")
            return None, None
            
    if config_to_load:
        try:
            with open(config_to_load, 'r', encoding='utf-8') as f:
                loaded_path = config_to_load
                return json.load(f), loaded_path
        except Exception as e:
            print(f"Error loading/parsing Markdown config {config_to_load}: {e}")
            return None, None
            
    return None, None

def save_config(config, config_path):
    """Save configuration to the JSON file."""
    print(f"Saving Markdown version configuration to {config_path}.")
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    except IOError as e:
        print(f"Error saving Markdown version configuration to {config_path}: {e}")

def prompt_for_paths(paths_config_section, is_termux_env):
    """Prompt the user to input file paths and ntfy topic for Markdown version."""
    home_dir = os.path.expanduser("~")
    default_markdown_path = ""
    default_output_dir = ""

    if is_termux_env:
        if os.getenv('HOME'): 
             default_markdown_path = os.path.join(os.getenv('HOME'), 'storage', 'shared', 'logseq', 'graphs', 'Omni', 'pages', 'Tasks.md')
             # Directly points to assets now
             default_output_dir = os.path.join(os.getenv('HOME'), 'storage', 'shared', 'logseq', 'graphs', 'Omni', 'assets')
    else: # PC environment
        default_markdown_path = os.path.join(home_dir, 'logseq', 'graphs', 'Omni', 'pages', 'Tasks.md')
        default_output_dir = os.path.join(home_dir, 'logseq', 'graphs', 'Omni', 'assets')


    if not paths_config_section.get('markdown'):
        prompt_message = "Enter Logseq Markdown file path"
        if default_markdown_path:
            prompt_message += f" (default: {default_markdown_path})"
        prompt_message += ": "
        
        md_path_choice = input(prompt_message).strip()
        paths_config_section['markdown'] = md_path_choice or default_markdown_path
        print(f"Markdown file set to: {paths_config_section['markdown']}")

    if not paths_config_section.get('output_dir'):
        prompt_message = "Enter output directory for script data"
        if default_output_dir:
            prompt_message += f" (default: {default_output_dir})"
        prompt_message += ": "
        output_dir_choice = input(prompt_message).strip()
        paths_config_section['output_dir'] = output_dir_choice or default_output_dir
        print(f"Output directory set to: {paths_config_section['output_dir']}")
    
    if not paths_config_section.get('ntfy_topic'):
        paths_config_section['ntfy_topic'] = input("Enter your ntfy.sh topic name (e.g., my_logseq_alerts_xyz): ").strip()
        print(f"ntfy.sh topic set to: {paths_config_section['ntfy_topic']}")

    output_dir = paths_config_section.get('output_dir')
    if output_dir and not paths_config_section.get('notification_tracker'):
        paths_config_section['notification_tracker'] = os.path.join(output_dir, 'notification_tracker_markdown.txt')
        print(f"Notification tracker path set to: {paths_config_section['notification_tracker']}")
    elif not output_dir:
        print("Warning: Output directory is not set. Cannot automatically configure notification_tracker path.")

def get_task_file_paths(config, is_termux_env):
    """Return file paths based on configuration and prompt user for required inputs."""
    if 'paths' not in config or 'default' not in config['paths']:
        print("Configuration 'paths' or 'paths.default' section is missing. Initializing.")
        config['paths'] = config.get('paths', {})
        config['paths']['default'] = {
            "markdown": "", "output_dir": "", "notification_tracker": "", "ntfy_topic": ""
        }
    
    paths_section = config['paths']['default']
    
    essential_paths_missing = False
    if not paths_section.get('markdown'):
        print("Markdown file path is missing.")
        essential_paths_missing = True
    if not paths_section.get('output_dir'):
        print("Output directory path is missing.")
        essential_paths_missing = True
    if not paths_section.get('ntfy_topic'):
        print("Ntfy topic is missing.")
        essential_paths_missing = True
        
    if essential_paths_missing:
        print("One or more essential configurations are missing. Prompting for input.")
        prompt_for_paths(paths_section, is_termux_env) 

    if paths_section.get('output_dir') and not paths_section.get('notification_tracker'):
        paths_section['notification_tracker'] = os.path.join(paths_section['output_dir'], 'notification_tracker_markdown.txt')
        print(f"Derived Notification tracker path: {paths_section['notification_tracker']}")

    return paths_section

def parse_task_line(line):
    """Extract task description from a line. Handles TODO and - TODO."""
    match = re.match(r"-\s*TODO\s+(.+)|TODO\s+(.+)", line, re.IGNORECASE)
    if match:
        return match.group(1).strip() if match.group(1) else match.group(2).strip()
    return None

def parse_scheduled_line(line):
    """Extract date and time from a scheduling line."""
    schedule_match = re.search(r"SCHEDULED:.*?<(\d{4}-\d{2}-\d{2})[^>]*?(\d{2}:\d{2})?>", line, re.IGNORECASE)
    if schedule_match:
        scheduled_date = schedule_match.group(1)
        scheduled_time = schedule_match.group(2) if schedule_match.group(2) else "00:00"
        return scheduled_date, scheduled_time
    return None, None

def send_ntfy_notification(topic, title, body, priority="default", tags=None):
    """Send a notification using ntfy.sh via curl."""
    if not topic:
        print("Error: ntfy.sh topic is not configured. Cannot send notification.")
        return
    ntfy_server = "https://ntfy.sh"
    full_topic_url = f"{ntfy_server}/{topic}"
    print(f"Sending ntfy notification to topic '{topic}' with title: '{title}' and body: '{body}'.")
    command = ['curl', '-X', 'POST']
    try:
        encoded_title = title.encode('utf-8').decode('latin-1')
    except UnicodeEncodeError:
        encoded_title = title 
    command.extend(['-H', f'Title: {encoded_title}'])
    command.extend(['-H', f'Priority: {priority}'])
    if tags: command.extend(['-H', f'Tags: {tags}'])
    command.extend(['-d', body.encode('utf-8')])
    command.append(full_topic_url)
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=False)
        stdout_decoded = result.stdout.decode('utf-8', errors='replace')
        stderr_decoded = result.stderr.decode('utf-8', errors='replace')
        if result.returncode == 0: print(f"Notification sent successfully. Response: {stdout_decoded}")
        else: print(f"Failed to send notification. Code: {result.returncode}\nStderr: {stderr_decoded}\nStdout: {stdout_decoded}")
    except FileNotFoundError: print("Error: curl not found. Please install curl and ensure it's in your PATH (e.g., on Linux: sudo apt install curl; on Termux: pkg install curl).")
    except Exception as e: print(f"Error sending ntfy notification: {e}")

def should_send_notification(tracker_file, task_unique_id):
    """Determine if the notification should be sent based on the tracker file."""
    if not tracker_file:
        print("Error: Notification tracker file path not configured.")
        return False
    tracker_dir = os.path.dirname(tracker_file)
    if not os.path.exists(tracker_dir) and tracker_dir != "":
        try: os.makedirs(tracker_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory for tracker file {tracker_dir}: {e}")
            return False
    sent_notifications = set()
    if os.path.exists(tracker_file):
        try:
            with open(tracker_file, 'r', encoding='utf-8') as f: sent_notifications = set(line.strip() for line in f)
        except IOError as e: print(f"Error reading tracker file {tracker_file}: {e}")
    if task_unique_id in sent_notifications:
        print(f"Notification previously sent for event ID: {task_unique_id}.")
        return False
    try:
        with open(tracker_file, 'a', encoding='utf-8') as f: f.write(task_unique_id + '\n')
        print(f"Notification for event ID {task_unique_id} marked as sent.")
        return True
    except IOError as e:
        print(f"Error writing to tracker file {tracker_file}: {e}")
        return False

def truncate_task_description(task_description, trunc_length):
    """Truncate the task description, preferring word boundaries."""
    if len(task_description) <= trunc_length: return task_description
    if trunc_length < 3: return "..."[:trunc_length]
    effective_trunc_length = trunc_length - 3
    truncated = task_description[:effective_trunc_length]
    last_space = truncated.rfind(' ')
    return truncated[:last_space] + "..." if last_space != -1 else truncated + "..."

def main():
    if IS_TERMUX: 
        try:
            print("Attempting to acquire Termux wakelock...")
            subprocess.run(['termux-wake-lock'], check=True, timeout=5)
            print("Termux wakelock acquired.")
        except Exception as e:
            print(f"Wakelock attempt failed (this is often ignorable if script is short or battery optimization is off for Termux): {e}")

    actual_exit_code = 1
    try:
        print(f"--- Logseq Markdown ntfy.sh Task Reminder ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
        
        config, config_path = load_config() 
        if config is None or config_path is None: 
            print("Critical error: Failed to load or create Markdown configuration. Aborting.")
            return 1

        paths_config = get_task_file_paths(config, IS_TERMUX) 
        
        if not paths_config.get('markdown') or \
           not paths_config.get('output_dir') or \
           not paths_config.get('ntfy_topic') or \
           not paths_config.get('notification_tracker'):
            print("Essential Markdown configuration is missing after setup attempt (markdown, output_dir, ntfy_topic, or notification_tracker). Aborting.")
            save_config(config, config_path) 
            return 1
        save_config(config, config_path) 

        markdown_file = paths_config.get('markdown')
        output_dir = paths_config.get('output_dir')
        notification_tracker_file = paths_config.get('notification_tracker')
        ntfy_topic = paths_config.get('ntfy_topic')

        print(f"Using Markdown file: {markdown_file}")
        print(f"Using Output directory (for tracker): {output_dir}")
        print(f"Using Notification tracker file: {notification_tracker_file}")
        print(f"Using ntfy.sh topic: {ntfy_topic}")
        
        if not all([markdown_file, output_dir, notification_tracker_file, ntfy_topic]):
            print("Critical path configuration or ntfy_topic is missing or empty. Aborting.")
            return 1
            
        try:
            if not os.path.exists(output_dir) and output_dir != "":
                os.makedirs(output_dir, exist_ok=True)
                print(f"Created output directory: {output_dir}")
        except OSError as e:
            print(f"Error creating output directory {output_dir}: {e}. Aborting.")
            return 1
            
        now = datetime.now()
        
        if not os.path.exists(markdown_file):
            print(f"Markdown file not found at {markdown_file}. Aborting.")
            print(f"Please ensure the 'markdown' path in your configuration file ('{config_path}') is correct.")
            return 1
        
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except IOError as e:
            print(f"Error reading markdown file {markdown_file}: {e}. Aborting.")
            return 1
        
        notifications_to_send = []
        current_task_desc = None
        current_task_line_number = 0 

        for i, line_content_raw in enumerate(lines):
            line_content_stripped = line_content_raw.strip()
            task_match = parse_task_line(line_content_stripped)
            if task_match:
                current_task_desc = task_match
                current_task_line_number = i + 1 
            
            if 'SCHEDULED:' in line_content_stripped.upper() and current_task_desc:
                s_date_str, s_time_str = parse_scheduled_line(line_content_stripped)
                if s_date_str:
                    try:
                        full_datetime_str = f'{s_date_str} {s_time_str}'
                        scheduled_dt_obj = datetime.strptime(full_datetime_str, '%Y-%m-%d %H:%M')
                        sanitized_task_desc_part = re.sub(r'[^\w\s-]', '', current_task_desc).strip().replace(' ', '_')[:30]
                        event_unique_id = f"logseq_md_event_{current_task_line_number}_{sanitized_task_desc_part}_{scheduled_dt_obj.strftime('%Y%m%d%H%M')}"
                        notifications_to_send.append({
                            'description': current_task_desc,
                            'datetime': scheduled_dt_obj,
                            'id': event_unique_id
                        })
                    except ValueError as e:
                        print(f"Warning: Could not parse date/time for task '{current_task_desc}' (line ~{i+1}): {e}. Line: '{line_content_stripped}'")
            elif not line_content_stripped.startswith((" ", "\t", "-", "SCHEDULED:")) and not task_match and "SCHEDULED:" not in line_content_stripped.upper():
                current_task_desc = None


        print(f"Found {len(notifications_to_send)} potential scheduled events from Markdown.")

        for event in notifications_to_send:
            original_task_desc = event['description']
            scheduled_date_time_obj = event['datetime']
            task_id = event['id']
        
            if scheduled_date_time_obj:
                time_difference_seconds = (scheduled_date_time_obj - now).total_seconds()
                
                if 0 <= time_difference_seconds <= 300: 
                    print(f"Markdown Task '{original_task_desc[:50]}...' scheduled for {scheduled_date_time_obj.strftime('%Y-%m-%d %H:%M')} is due soon.")
                    if should_send_notification(notification_tracker_file, task_id):
                        ntfy_title_header = 'Task Reminder'
                        notif_body_desc = truncate_task_description(original_task_desc, 100)
                        details_for_body = f"{notif_body_desc} is due at {scheduled_date_time_obj.strftime('%H:%M')}!"
                        ntfy_message_body = f"{details_for_body}"
                        send_ntfy_notification(ntfy_topic, ntfy_title_header, ntfy_message_body, priority="high", tags="alarm_clock,markdown")
                    else:
                        print(f"Notification for Markdown task ID {task_id} already sent or failed to mark.")
        
        print("--- Markdown Script finished processing. ---")
        actual_exit_code = 0
    
    except Exception as e:
        print(f"An unexpected error occurred in Markdown main execution: {e}")
        import traceback
        traceback.print_exc()
        actual_exit_code = 1
    finally:
        if IS_TERMUX: 
            try:
                print("Attempting to release Termux wakelock...")
                subprocess.run(['termux-wake-unlock'], check=False, timeout=5) 
                print("Termux wakelock release attempted.")
            except Exception as e:
                print(f"Wakelock release attempt failed: {e}")
        
        print(f"Script exiting with code: {actual_exit_code}")
        return actual_exit_code

if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
