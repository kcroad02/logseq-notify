# Logseq Push Tasker (Logpush)

Streamline your productivity with Logpush, a powerful integration of Logseq, Pushbullet, Tasker, KWGT, and Syncthing. This actively maintained project automates tasks, sends notifications, and displays tasks on your home screen, ensuring a seamless experience across Android devices and desktops via Pushbullet's Firefox plugin.

## Features

- **Pushbullet Integration**: Receive notifications for your Logseq tasks.
- **Tasker Automation**: Trigger actions within Logseq based on specified conditions.
- **KWGT Widget**: Display tasks and notifications on your home screen.
- **Syncthing Compatibility**: Sync Logseq files across devices.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo/logseq-push-task-widget.git
   cd logseq-push-task-widget
   ```
2. **Install `requests` library if not already included:**
   ```sh
   pip install requests
   ```
3. **Setup configuration:**
   - Run the script to create a default configuration file.
     ```sh
     python main.py
     ```
   - Update `config.json` with your markdown file paths and Pushbullet API key path.
4. **Configure Tasker:**
   - Import the provided [XML Tasker configuration](https://github.com/kcroad02/logseq-push-tasker/blob/main/LogPush%20Tasker%20Defaults.tsk.xml).
   - Set the Termux execution path and Pushbullet API key.
   - Verify that paths match your setup.
5. **Configure KWGT:**
   - Import the [KWGT widget preset](https://github.com/kcroad02/logseq-push-tasker/blob/main/LogpushWidgetExample.kwgt) or create your own.
   - Ensure Tasker variables match the widget text placeholders.

## Usage

1. **Add TODO tasks in your markdown file:**
   ```markdown
   - TODO Buy groceries
     SCHEDULED: <2023-10-05 09:00>
   - TODO Call mom
   ```
2. **Run the script to parse tasks and generate `.txt` files:**
   ```sh
   python main.py
   ```
3. **Tasker will update the KWGT widget with the `.txt` files.**

## Configuration Details

- **Markdown Path**: Path to your Logseq markdown file (e.g., `~/Sync/Logseq/pages/Logpush.md`)
- **Output Directory**: Directory for task `.txt` files and outputs (e.g., `~/Sync/Logseq/assets/logpush`)
- **PushWidget Target**: Directory for PushWidget files
- **Notification Tracker**: File to track the last notification sent

## API Key Management

1. **Get your Pushbullet API key:**
   - Generate an access token from Pushbullet settings.
2. **Save API key:**
   - The script will prompt you to enter and save the API key if not found.
   ```json
   {
     "api_key": "your_pushbullet_api_key"
   }
   ```

## Creating Symlink (Optional)

For Termux users on Android:
```sh
ln -s ~/storage/shared/Downloads/logpush ~/logpush
```

## Notifications

Notifications are sent via Pushbullet within 3 minutes of the scheduled task time.

## Customization

- **Pushbullet Channels**: Modify notification settings.
- **Tasker Actions**: Adjust automation actions.
- **KWGT Appearance**: Customize widget look and feel.

Refer to the documentation within each folder for detailed customization options.

## Caveats

- Ensure the latest versions of Tasker, Termux, and KWGT are installed for compatibility.
- The KWGT widget is designed for Android and may not function on other operating systems.

## Demo

I plan to create a demo video soon.

~~Watch the demo video here to see Logseq tasks integrating seamlessly with Pushbullet, Tasker, and KWGT.~~

## Credits

- Logseq for task management.
- Pushbullet for notifications.
- Tasker for automation.
- KWGT for the home screen widget.
