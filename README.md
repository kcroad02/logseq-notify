----
# !!! This script doesn't work with Logseq's database version yet !!!
----

# Get Logseq Reminders on Your Phone/PC with ntfy.sh

This Python script helps you remember tasks from your Logseq notes. It looks at your `Tasks.md` file for tasks that have a "SCHEDULED" date and time. If a task is going to start in the next 5 minutes, it sends you a push notification using a service called `ntfy.sh`.

You should set up this script to run regularly, for example, every 5 minutes. You can use tools like `cron` on computers (Linux/macOS/Windows) or **Tasker on Android (using Termux)**.

## What it Does

* **Reads Your Tasks:** It goes through your `Tasks.md` file.
* **Finds Scheduled Times:** It spots lines that say `SCHEDULED: <YYYY-MM-DD HH:MM>` under your tasks.
* **Sends Timely Alerts:** If a task is set to start within 5 minutes, you'll get a notification.
* **Uses ntfy.sh:** It sends these notifications through `ntfy.sh`, which lets you get alerts on your phone or other devices.
* **No Repeat Alerts:** It remembers which tasks it's already told you about, so you don't get the same reminder over and over again.
* **Works Everywhere:**
    * It can run on computers with operating systems such as Linux, macOS, Windows if you have Python.
    * It also works on Android phones using an app called Termux. It even handles keeping your phone "awake" so it can run properly.
* **Easy Setup for File Locations:** You can tell the script where your files are. On a PC, it usually has a special spot it checks first. On Android/Termux, or if the special spot isn't used, it looks in the same folder as the script.

## How it Works

1.  **Finds Your Settings:** The script first tries to find a file called `config_markdown.json`.
    * **On a PC:** It first checks in a folder like `~/logseq/graphs/Omni/assets/config_markdown.json`.
    * **On Android (Termux) or if not found on PC:** It then looks for `config_markdown.json` in the same folder where the script itself is.
    * If it can't find any settings, it will create a new `config_markdown.json` file for you. It might also ask you where your Markdown task file is, where it should save its own data, and what your `ntfy.sh` topic name is.
2.  **Reads Your Markdown File:** It opens your `Tasks.md` file and reads it line by line.
    * It finds your tasks, which usually start with `TODO` or `- TODO`.
    * Then, it looks for the `SCHEDULED:` line right below your task.
3.  **Checks the Time:** For each task with a schedule, it compares that time to the current time.
4.  **Sends an Alert:** If a task is due within the next 5 minutes (but not past due), and you haven't been notified yet:
    * It creates a short message.
    * It sends this message to your `ntfy.sh` topic using a tool called `curl`.
    * It saves a note in a file called `notification_tracker_markdown.txt` so it doesn't send the same alert again.
5.  **Keeps Android Awake (Termux):** If you're running this on Termux on Android, the script will try to keep your phone from going to sleep while it's working. It lets go of this "wakelock" when it's done.

## What You Need

* **Python 3:** Make sure Python 3 is installed.
* **`curl`:** You need the `curl` program installed.
    * On Linux: Use `sudo apt install curl` or similar.
    * On Termux: Use `pkg install curl`.
    * On macOS: It's usually already there.
    * On Windows: You can install it with Chocolatey (`choco install curl`) or download it.
* **ntfy.sh Topic:** You need your own `ntfy.sh` topic. This is like your personal channel for notifications. You can use the public `https://ntfy.sh/your_topic` or set up your own ntfy server.
* **Logseq (or similar):** You need a way to write and save your tasks in a Markdown file, following the Logseq format.
* **Tasker (for Android Automation):** To make this script run automatically on your Android phone with Termux, you will need the Tasker app.

## Setup Steps

1.  **Get the Script:** Save the script file as `main.py` in a folder. For Termux, putting it in your home directory (`~`) is a good idea.

2.  **Make it Run (Optional, for Linux/macOS/Termux):**
    Open your terminal or Termux app and type:
    ```bash
    chmod +x main.py
    ```

3.  **First-Time Setup:**
    Run the script once to set it up:
    ```bash
    python3 main.py
    ```
    * If no settings file (`config_markdown.json`) is found, the script will create one for you.
        * On PC: It might create it in `~/logseq/graphs/Omni/assets/config_markdown.json`.
        * On Termux (or if the PC path isn't used): It will create it in the same folder as `main.py`.
    * The script will ask you to type in:
        * The full path to your Logseq `Tasks.md` file.
        * A folder where the script can save its internal files (like the notification tracker).
        * Your `ntfy.sh` topic name.
    * Take a look at the `config_markdown.json` file it created and make sure the paths are correct. The script tries to guess the right paths for your computer or Termux.

    **What `config_markdown.json` looks like:**
    ```json
    {
        "paths": {
            "default": {
                "markdown": "/path/to/your/logseq/graphs/YourGraph/pages/Tasks.md",
                "output_dir": "/path/to/your/logseq/graphs/YourGraph/assets", // Or any other folder you can write to
                "notification_tracker": "/path/to/your/logseq/graphs/YourGraph/assets/notification_tracker_markdown.txt",
                "ntfy_topic": "your_secret_ntfy_topic"
            }
        }
    }
    ```
    *Note: The `notification_tracker` path is usually filled in automatically if you set the `output_dir`.*

## How to Write Your Tasks

The script looks for tasks that look like this in your Markdown file:

```markdown
- TODO Task description
  SCHEDULED: <YYYY-MM-DD HH:MM>
```
Important: The "SCHEDULED:" line must be indented (use Shift + Enter after the task description in Logseq).
