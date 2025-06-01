import os
import re
import json
import subprocess
import sqlite3 # For interacting with SQLite databases
from datetime import datetime
from socket import gethostname

# Determine the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_PATH = os.path.join(SCRIPT_DIR, 'config_db.json') # Separate config for DB version

home_dir_alt = os.getenv('HOME')
if home_dir_alt:
    ALTERNATIVE_CONFIG_PATH = os.path.join(home_dir_alt, 'storage', 'shared', 'Logseq', 'assets', 'logseq-task-notifier', 'config_db.json')
else:
    ALTERNATIVE_CONFIG_PATH = os.path.join(SCRIPT_DIR, 'alternative_config_db.json')

def create_default_config(config_path):
    """Create a default configuration file for the DB version."""
    if not os.path.exists(config_path):
        print(f"Creating default DB configuration file at {config_path}.")
        default_config = {
            "database_path": "", # IMPORTANT: Path to your Logseq database file(s)
            "graph_name": "default", # Optional: if tasks are per-graph and graph needs to be specified in query
            "output_dir": "",
            "notification_tracker": "",
            "ntfy_topic": ""
        }
        
        if gethostname() == 'localhost' or "com.termux" in os.getenv("PREFIX", ""):
            print("Detected Termux environment. Please configure paths for your Logseq DB, output, and ntfy.sh topic.")
            if home_dir_alt:
                # Example placeholder - actual path will depend on Logseq's new structure
                default_config["database_path"] = os.path.join(home_dir_alt, 'storage', 'shared', 'Logseq', 'databases', 'logseq.db') 
                default_config["output_dir"] = os.path.join(home_dir_alt, 'storage', 'shared', 'Logseq', 'assets', 'logseq-db-task-notifier-data')
        
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4)
            print(f'Default DB configuration file created at {config_path}. Please update it.')
        except IOError as e:
            print(f"Error creating default DB configuration file {config_path}: {e}")
    else:
        print(f"DB Configuration file already exists at {config_path}.")

def load_config():
    """Load configuration for the DB version."""
    config_path_to_try = None
    if os.path.exists(ALTERNATIVE_CONFIG_PATH):
        print(f"Loading DB configuration from alternative path: {ALTERNATIVE_CONFIG_PATH}.")
        config_path_to_try = ALTERNATIVE_CONFIG_PATH
    elif os.path.exists(DEFAULT_CONFIG_PATH):
        print(f"Loading DB configuration from default path: {DEFAULT_CONFIG_PATH}.")
        config_path_to_try = DEFAULT_CONFIG_PATH
    else:
        print(f"No DB configuration file found at expected locations.")
        print(f"Attempting to create a default DB config at: {DEFAULT_CONFIG_PATH}")
        default_dir = os.path.dirname(DEFAULT_CONFIG_PATH)
        if not os.path.exists(default_dir) and default_dir != "":
            try:
                os.makedirs(default_dir, exist_ok=True)
            except OSError as e:
                print(f"Error creating directory {default_dir}: {e}")
                return None, None
        create_default_config(DEFAULT_CONFIG_PATH)
        if os.path.exists(DEFAULT_CONFIG_PATH):
             print(f"Loading newly created DB configuration from default path: {DEFAULT_CONFIG_PATH}.")
             config_path_to_try = DEFAULT_CONFIG_PATH
        else:
            print("Failed to create or find a DB configuration file.")
            return None, None
    
    if config_path_to_try:
        try:
            with open(config_path_to_try, 'r', encoding='utf-8') as f:
                return json.load(f), config_path_to_try
        except Exception as e:
            print(f"Error loading/parsing DB config {config_path_to_try}: {e}")
            return None, None
    return None, None

def save_config(config, config_path):
    """Save DB configuration."""
    print(f"Saving DB configuration to {config_path}.")
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    except IOError as e:
        print(f"Error saving DB configuration to {config_path}: {e}")

def prompt_for_paths(paths_config_section):
    """Prompt for DB version specific paths."""
    home_dir = os.getenv('HOME')
    default_db_path = ""
    default_output_dir = ""

    if home_dir:
        # These are GUESSES. The actual path will depend on Logseq's implementation.
        default_db_path = os.path.join(home_dir, 'storage', 'shared', 'Logseq', 'logseq.sqlite3') # Example
        default_output_dir = os.path.join(home_dir, 'storage', 'shared', 'Logseq', 'assets', 'logseq-db-task-notifier-data')

    if not paths_config_section.get('database_path'):
        db_path_prompt = f"Enter Logseq database file path"
        if default_db_path:
            db_path_prompt += f" (e.g., {default_db_path})"
        db_path_prompt += ": "
        paths_config_section['database_path'] = input(db_path_prompt).strip()
        print(f"Logseq database path set to: {paths_config_section['database_path']}")

    if not paths_config_section.get('output_dir'):
        if default_output_dir:
            output_dir_choice = input(f"Enter output directory for script data (default: {default_output_dir}): ").strip()
            paths_config_section['output_dir'] = output_dir_choice or default_output_dir
        else:
            paths_config_section['output_dir'] = input("Enter the output directory path: ").strip()
        print(f"Output directory set to: {paths_config_section['output_dir']}")
    
    if not paths_config_section.get('ntfy_topic'):
        paths_config_section['ntfy_topic'] = input("Enter your ntfy.sh topic name: ").strip()
        print(f"ntfy.sh topic set to: {paths_config_section['ntfy_topic']}")

    output_dir = paths_config_section.get('output_dir')
    if output_dir and not paths_config_section.get('notification_tracker'):
        paths_config_section['notification_tracker'] = os.path.join(output_dir, 'notification_tracker_db.txt')
        print(f"Notification tracker path set to: {paths_config_section['notification_tracker']}")


def get_db_config(config):
    """Get DB specific configurations."""
    if 'database_path' not in config or \
       'output_dir' not in config or \
       'ntfy_topic' not in config:
        print("Essential DB configuration (database_path, output_dir, or ntfy_topic) is missing. Prompting.")
        prompt_for_paths(config) # Pass the whole config dict or a specific section

    if config.get('output_dir') and not config.get('notification_tracker'):
        config['notification_tracker'] = os.path.join(config['output_dir'], 'notification_tracker_db.txt')
        print(f"Derived DB Notification tracker path: {config['notification_tracker']}")
    return config


def fetch_tasks_from_db(db_path):
    """
    Fetch tasks from the Logseq SQLite database.
    THIS IS A TEMPLATE FUNCTION. You WILL need to adapt the SQL query.
    """
    tasks = []
    if not db_path or not os.path.exists(db_path):
        print(f"Error: Database path '{db_path}' is invalid or file does not exist.")
        return tasks

    try:
        conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True) # Read-only connection
        cursor = conn.cursor()

        # --- IMPORTANT ---
        # The following SQL query is a GUESS. You need to replace it with the
        # correct query based on Logseq's actual database schema.
        # You'll need to find out:
        # 1. Which table stores tasks (e.g., 'tasks', 'blocks', 'items').
        # 2. The column name for the task description/content.
        # 3. How scheduled dates/times are stored (e.g., a dedicated column, a property in a JSON field).
        # 4. How to identify tasks that are "TODO" or "SCHEDULED".
        #
        # Example placeholder query:
        # Assume tasks are in a 'blocks' table, content in 'content' or 'properties' (JSON),
        # and scheduled info might be parsed from 'content' or a specific property.
        # This query likely needs significant changes.
        #
        # A more realistic approach might involve looking for blocks with "SCHEDULED:"
        # or specific task markers if they are stored similarly to markdown.
        # Or, there might be dedicated columns like `is_task`, `status`, `scheduled_at_timestamp`.
        #
        # For instance, if tasks have a 'scheduled' timestamp column (unix epoch) and a 'content' column:
        # query = """
        # SELECT uuid, content, scheduled -- Replace 'uuid', 'content', 'scheduled' with actual column names
        # FROM blocks -- Replace 'blocks' with the actual table name
        # WHERE status = 'TODO' AND scheduled IS NOT NULL;
        # """
        #
        # If scheduled info is in a text property you need to parse:
        query = """
        SELECT id, content_field, scheduled_at_field -- REPLACE THESE with actual column names
        FROM your_task_table -- REPLACE THIS with the actual table name
        WHERE task_status_field = 'TODO' -- REPLACE THIS with actual status check
          AND (scheduled_at_field IS NOT NULL OR content_field LIKE '%SCHEDULED:%'); -- Example condition
        """
        print(f"Executing placeholder query (NEEDS REVIEW): {query} on DB: {db_path}")
        # cursor.execute(query)
        # rows = cursor.fetchall()
        # For now, returning an empty list as the query is a placeholder
        rows = [] 
        print("Placeholder query executed. No actual data fetched as schema is unknown.")


        # Process rows if the query were real
        # for row in rows:
        #     task_id_from_db = str(row[0]) # Example: first column is a unique ID
        #     task_content = row[1]         # Example: second column is the task text
        #     scheduled_info = row[2]       # Example: third column has schedule data
            
        #     scheduled_dt_obj = None
        #     # You'll need robust parsing for scheduled_info from the DB
        #     # This is highly dependent on how it's stored.
        #     # For example, if it's a UNIX timestamp:
        #     # if isinstance(scheduled_info, (int, float)):
        #     #    scheduled_dt_obj = datetime.fromtimestamp(scheduled_info)
        #     # If it's a string like "YYYY-MM-DD HH:MM":
        #     # try:
        #     #    scheduled_dt_obj = datetime.strptime(scheduled_info, '%Y-%m-%d %H:%M')
        #     # except (ValueError, TypeError):
        #     #    pass # Handle cases where parsing fails

        #     # If scheduled info is embedded in task_content like Markdown:
        #     # date_match = re.search(r"SCHEDULED:.*?<(\d{4}-\d{2}-\d{2})", task_content)
        #     # time_match = re.search(r"(\d{2}:\d{2})", task_content) # Within the SCHEDULED part
        #     # if date_match:
        #     #     s_date_str = date_match.group(1)
        #     #     s_time_str = time_match.group(1) if time_match else "00:00"
        #     #     try:
        #     #         scheduled_dt_obj = datetime.strptime(f'{s_date_str} {s_time_str}', '%Y-%m-%d %H:%M')
        #     #     except ValueError:
        #     #         print(f"Could not parse SCHEDULED from DB content: {task_content}")


        #     if task_content and scheduled_dt_obj:
        #         # Create a unique ID for notification tracking
        #         # Using the DB's own task ID is best if available and persistent
        #         unique_event_id = f"db_task_{task_id_from_db}_{scheduled_dt_obj.strftime('%Y%m%d%H%M')}"
        #         tasks.append({
        #             'description': task_content,
        #             'datetime': scheduled_dt_obj,
        #             'id': unique_event_id 
        #         })
        #     elif task_content and not scheduled_dt_obj:
        #         print(f"Task '{task_content[:50]}' found but no valid schedule info could be parsed/found from DB row: {row}")


        conn.close()
    except sqlite3.Error as e:
        print(f"SQLite error when connecting or querying DB at '{db_path}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred in fetch_tasks_from_db: {e}")
    
    if not tasks:
        print("No tasks fetched from DB (or placeholder query returned none). Check DB path, schema, and SQL query.")
    return tasks

# --- Utility functions (send_ntfy_notification, should_send_notification, truncate_task_description) ---
# These can be largely the same as in the Markdown version, so I'll include them for completeness.

def send_ntfy_notification(topic, title, body, priority="default", tags=None):
    if not topic:
        print("Error: ntfy.sh topic is not configured.")
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
    except FileNotFoundError: print("Error: curl not found. Install with: pkg install curl")
    except Exception as e: print(f"Error sending ntfy notification: {e}")

def should_send_notification(tracker_file, task_unique_id):
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
    if len(task_description) <= trunc_length: return task_description
    if trunc_length < 3: return "..."[:trunc_length]
    effective_trunc_length = trunc_length - 3
    truncated = task_description[:effective_trunc_length]
    last_space = truncated.rfind(' ')
    return truncated[:last_space] + "..." if last_space != -1 else truncated + "..."

# --- Main Function ---
def main():
    is_termux = "com.termux" in os.getenv("PREFIX", "")
    if is_termux:
        try:
            print("Attempting to acquire Termux wakelock...")
            subprocess.run(['termux-wake-lock'], check=True, timeout=5)
            print("Termux wakelock acquired.")
        except Exception as e:
            print(f"Wakelock attempt failed: {e}")

    actual_exit_code = 1
    try:
        print(f"--- Logseq DB ntfy.sh Task Reminder ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
        
        config_data, config_path = load_config()
        if config_data is None or config_path is None:
            print("Critical error: Failed to load or create DB configuration. Aborting.")
            return 1

        # Use get_db_config to ensure all necessary keys are present or prompted for
        # This expects config_data to be the dictionary containing the paths, not config_data['paths']['default']
        paths_config = get_db_config(config_data) 
        save_config(paths_config, config_path) # Save if prompts occurred

        db_file_path = paths_config.get('database_path')
        notification_tracker_file = paths_config.get('notification_tracker')
        ntfy_topic = paths_config.get('ntfy_topic')
        output_dir = paths_config.get('output_dir') # For creating dir if needed

        print(f"Using Logseq DB path: {db_file_path}")
        print(f"Using Notification tracker file: {notification_tracker_file}")
        print(f"Using ntfy.sh topic: {ntfy_topic}")

        if not all([db_file_path, notification_tracker_file, ntfy_topic, output_dir]):
            print("Critical DB configuration (DB path, tracker, topic, or output_dir) is missing. Aborting.")
            return 1
        
        try: # Ensure output directory exists
            if not os.path.exists(output_dir) and output_dir != "":
                os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating output directory {output_dir}: {e}. Aborting.")
            return 1

        now = datetime.now()
        
        # Fetch tasks from the database
        # THIS IS WHERE THE CORE LOGIC CHANGES FROM THE MARKDOWN VERSION
        tasks_from_db = fetch_tasks_from_db(db_file_path)
        
        if not tasks_from_db:
            print("No tasks retrieved from the database. Ensure DB path is correct and `fetch_tasks_from_db` is properly implemented.")
        else:
            print(f"Retrieved {len(tasks_from_db)} tasks from DB (after parsing).")


        for event in tasks_from_db:
            original_task_desc = event['description']
            scheduled_date_time_obj = event['datetime']
            task_id = event['id']
        
            if scheduled_date_time_obj:
                time_difference_seconds = (scheduled_date_time_obj - now).total_seconds()
                
                if 0 <= time_difference_seconds <= 180: # Notify if due within 3 minutes
                    print(f"DB Task '{original_task_desc[:50]}...' scheduled for {scheduled_date_time_obj.strftime('%Y-%m-%d %H:%M')} is due soon.")
                    if should_send_notification(notification_tracker_file, task_id):
                        ntfy_title_header = 'Task Reminder (DB)'
                        notif_body_desc = truncate_task_description(original_task_desc, 100)
                        details_for_body = f"{notif_body_desc} is due at {scheduled_date_time_obj.strftime('%H:%M')}!"
                        ntfy_message_body = f"Task Reminder: {details_for_body}"
                        
                        send_ntfy_notification(ntfy_topic, ntfy_title_header, ntfy_message_body, priority="high", tags="alarm_clock,database")
                    else:
                        print(f"Notification for DB task ID {task_id} already sent or failed to mark.")
        
        print("--- DB Script finished processing. ---")
        actual_exit_code = 0
    
    except Exception as e:
        print(f"An unexpected error occurred in DB main execution: {e}")
        import traceback
        traceback.print_exc()
        actual_exit_code = 1
    finally:
        if is_termux:
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

