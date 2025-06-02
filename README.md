# Logseq Notify via ntfy.sh

This Python script looks through a Logseq Markdown file named `Tasks.md` for tasks with `SCHEDULED:` timestamps. It sends push notifications via a self-hosted or public `ntfy.sh` server for tasks that are due to start within the next 5 minutes.

The script is designed to be run periodically (e.g., every 5 minutes) by a scheduler like `cron` (on Linux/macOS/PC) or Tasker (on Android via Termux).

## Features

* **Markdown Task Parsing:** Reads tasks from a Logseq-specific Markdown file.
* **Scheduled Time Detection:** Recognizes `SCHEDULED: <YYYY-MM-DD HH:MM>` entries associated with tasks.
* **Timely Notifications:** Sends alerts for tasks scheduled to occur between the current time and 5 minutes into the future.
* **ntfy.sh Integration:** Leverages `ntfy.sh` for customizable push notifications.
* **Duplicate Prevention:** Keeps track of sent notifications to avoid redundant alerts for the same task instance.
* **Cross-Platform Compatibility:**
    * Works on standard PC environments (Linux, macOS, Windows with Python).
    * Supports Android via Termux, including wakelock handling to ensure script execution.
* **Flexible Path Configuration:** Allows user-specific configuration paths on PC and script-local paths for portability/Termux.

## How it Works

1.  **Load Configuration:** The script first tries to load `config_markdown.json`.
    * On a PC, it looks in `~/logseq/graphs/Omni/assets/config_markdown.json`.
    * If not found (or on Termux), it looks for `config_markdown.json` in the same directory as the script.
    * If no configuration is found, it creates a default one and may prompt for initial setup of paths (Markdown file, output directory, ntfy topic).
2.  **Parse Markdown File:** It reads the specified Markdown file line by line.
    * It identifies tasks typically marked with `TODO` (or `- TODO`).
    * It then looks for `SCHEDULED: <YYYY-MM-DD HH:MM>` lines associated with these tasks.
3.  **Check Schedule:** For each found scheduled task, it compares the scheduled datetime with the current time.
4.  **Send Notification:** If a task's scheduled time is between 0 and 300 seconds (inclusive) from the current time, and a notification hasn't been sent for it already:
    * It constructs a message.
    * It sends a POST request to the configured `ntfy.sh` topic using `curl`.
    * It records the task's unique ID in a tracker file (`notification_tracker_markdown.txt`) to prevent re-notification.
5.  **Termux Wakelock:** If running in Termux, it attempts to acquire a wakelock at the start and release it at the end to prevent the system from sleeping during execution.

## Prerequisites

* **Python 3:** Ensure Python 3 is installed on your system.
* **`curl`:** The `curl` command-line utility must be installed and accessible in your system's PATH.
    * On Linux: `sudo apt install curl` or similar for your distribution.
    * On Termux: `pkg install curl`
    * On macOS: Usually pre-installed. If not, `brew install curl`.
    * On Windows: Can be installed via Chocolatey (`choco install curl`) or downloaded manually.
* **ntfy.sh Topic:** You need an ntfy.sh topic. You can use the public `https://ntfy.sh/your_topic` or your own self-hosted ntfy server.
* **Logseq (or other Markdown editor):** A way to create and manage your Markdown task file in the expected format.

## Setup

1.  **Download the Script:**
    Save the script as `main.py` in a directory of your choice (home directory recommended for Termux).

2.  **Make it Executable (Optional, for Linux/macOS/Termux):**
    ```bash
    chmod +x main.py
    ```

3.  **Initial Configuration:**
    Run the script for the first time:
    ```bash
    python3 main.py
    ```
    * If a configuration file is not found, the script will create a default one (`config_markdown.json`).
        * On PC: `~/.config/logseq_notifier_md/config_markdown.json`
        * On Termux (or if the PC user path fails): in the same directory as `main.py`.
    * It will then prompt you to enter:
        * The full path to your Logseq Markdown tasks file.
        * The full path to an output directory where the script can store its data (like the notification tracker).
        * Your `ntfy.sh` topic name.
    * Review the created `config_markdown.json` and adjust paths if necessary. The script will suggest defaults based on your environment (PC or Termux).

    **Example `config_markdown.json` structure:**
    ```json
    {
        "paths": {
            "default": {
                "markdown": "/path/to/your/logseq/graphs/YourGraph/pages/Tasks.md",
                "output_dir": "/path/to/your/logseq/graphs/YourGraph/assets", // Or any other writable directory
                "notification_tracker": "/path/to/your/logseq/graphs/YourGraph/assets/notification_tracker_markdown.txt", // Automatically derived from output_dir
                "ntfy_topic": "your_secret_ntfy_topic"
            }
        }
    }
    ```
    *Note: The `notification_tracker` path is usually derived automatically if `output_dir` is set.*

## Usage

### The script looks for tasks formatted like this:

```markdown
- TODO Task description
  SCHEDULED: <YYYY-MM-DD HH:MM>
```

The second line must be shift+entered.
