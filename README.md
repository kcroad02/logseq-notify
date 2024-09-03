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
   - Import the provided XML Tasker configuration.
   - Set the Termux execution path and Pushbullet API key.
   - Verify that paths match your setup.
5. **Configure KWGT:**
   - Import the KWGT widget preset or create your own.
   - Ensure Tasker variables match the widget text placeholders.

## Usage

1. **Add TODO tasks in your markdown file:**
   ```markdown
   - TODO Buy groceries SCHEDULED: <2023-10-05 09:00>
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

## Tasker Configuration Example
<details>
  <summary>Click to toggle the XML Example</summary>

 ```xml
 <TaskerData sr="" dvi="1" tv="6.3.13">
 	<Task sr="task6">
 		<cdate>1725020470664</cdate>
 		<edate>1725403643059</edate>
 		<id>6</id>
 		<nme>LogPush</nme>
 		<pri>6</pri>
 		<Kid sr="Kid">
 			<launchID>6</launchID>
 			<pkg>com.rogbone</pkg>
 			<vTarg>29</vTarg>
 			<vnme>1.0</vnme>
 			<vnum>3</vnum>
 		</Kid>
 		<Action sr="act0" ve="7">
 			<code>1256900802</code>
 			<Bundle sr="arg0">
 				<Vals sr="val">
 					<com.termux.execute.arguments>&lt;null&gt;</com.termux.execute.arguments>
 					<com.termux.execute.arguments-type>java.lang.String</com.termux.execute.arguments-type>
 					<com.termux.tasker.extra.BACKGROUND_CUSTOM_LOG_LEVEL>&lt;null&gt;</com.termux.tasker.extra.BACKGROUND_CUSTOM_LOG_LEVEL>
 					<com.termux.tasker.extra.BACKGROUND_CUSTOM_LOG_LEVEL-type>java.lang.String</com.termux.tasker.extra.BACKGROUND_CUSTOM_LOG_LEVEL-type>
 					<com.termux.tasker.extra.EXECUTABLE>../../logpush/main.py</com.termux.tasker.extra.EXECUTABLE>
 					<com.termux.tasker.extra.EXECUTABLE-type>java.lang.String</com.termux.tasker.extra.EXECUTABLE-type>
 					<com.termux.tasker.extra.SESSION_ACTION>&lt;null&gt;</com.termux.tasker.extra.SESSION_ACTION>
 					<com.termux.tasker.extra.SESSION_ACTION-type>java.lang.String</com.termux.tasker.extra.SESSION_ACTION-type>
 					<com.termux.tasker.extra.STDIN></com.termux.tasker.extra.STDIN>
 					<com.termux.tasker.extra.STDIN-type>java.lang.String</com.termux.tasker.extra.STDIN-type>
 					<com.termux.tasker.extra.TERMINAL>false</com.termux.tasker.extra.TERMINAL>
 					<com.termux.tasker.extra.TERMINAL-type>java.lang.Boolean</com.termux.tasker.extra.TERMINAL-type>
 					<com.termux.tasker.extra.VERSION_CODE>6</com.termux.tasker.extra.VERSION_CODE>
 					<com.termux.tasker.extra.VERSION_CODE-type>java.lang.Integer</com.termux.tasker.extra.VERSION_CODE-type>
 					<com.termux.tasker.extra.WAIT_FOR_RESULT>true</com.termux.tasker.extra.WAIT_FOR_RESULT>
 					<com.termux.tasker.extra.WAIT_FOR_RESULT-type>java.lang.Boolean</com.termux.tasker.extra.WAIT_FOR_RESULT-type>
 					<com.termux.tasker.extra.WORKDIR>&lt;null&gt;</com.termux.tasker.extra.WORKDIR>
 					<com.termux.tasker.extra.WORKDIR-type>java.lang.String</com.termux.tasker.extra.WORKDIR-type>
 					<com.twofortyfouram.locale.intent.extra.BLURB>../../logpush/main.py
 
 Working Directory ✕
 Stdin ✕
 Custom Log Level null
 Terminal Session ✕
 Wait For Result ✓</com.twofortyfouram.locale.intent.extra.BLURB>
 					<com.twofortyfouram.locale.intent.extra.BLURB-type>java.lang.String</com.twofortyfouram.locale.intent.extra.BLURB-type>
 					<net.dinglisch.android.tasker.RELEVANT_VARIABLES>&lt;StringArray sr=""&gt;&lt;_array_net.dinglisch.android.tasker.RELEVANT_VARIABLES0&gt;%stdout
 Standard Output
 The &amp;lt;B&amp;gt;stdout&amp;lt;/B&amp;gt; of the command.&lt;/_array_net.dinglisch.android.tasker.RELEVANT_VARIABLES0&gt;&lt;_array_net.dinglisch.android.tasker.RELEVANT_VARIABLES1&gt;%stdout_original_length
 Standard Output Original Length
 The original length of &amp;lt;B&amp;gt;stdout&amp;lt;/B&amp;gt;.&lt;/_array_net.dinglisch.android.tasker.RELEVANT_VARIABLES1&gt;&lt;_array_net.dinglisch.android.tasker.RELEVANT_VARIABLES2&gt;%stderr
 Standard Error
 The &amp;lt;B&amp;gt;stderr&amp;lt;/B&amp;gt; of the command.&lt;/_array_net.dinglisch.android.tasker.RELEVANT_VARIABLES2&gt;&lt;_array_net.dinglisch.android.tasker.RELEVANT_VARIABLES3&gt;%stderr_original_length
 Standard Error Original Length
 The original length of &amp;lt;B&amp;gt;stderr&amp;lt;/B&amp;gt;.&lt;/_array_net.dinglisch.android.tasker.RELEVANT_VARIABLES3&gt;&lt;_array_net.dinglisch.android.tasker.RELEVANT_VARIABLES4&gt;%result
 Exit Code
 The &amp;lt;B&amp;gt;exit code&amp;lt;/B&amp;gt; of the command.0 often means success and anything else is usually a failure of some sort.&lt;/_array_net.dinglisch.android.tasker.RELEVANT_VARIABLES4&gt;&lt;/StringArray&gt;</net.dinglisch.android.tasker.RELEVANT_VARIABLES>
 					<net.dinglisch.android.tasker.RELEVANT_VARIABLES-type>[Ljava.lang.String;</net.dinglisch.android.tasker.RELEVANT_VARIABLES-type>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>com.termux.tasker.extra.EXECUTABLE com.termux.execute.arguments com.termux.tasker.extra.WORKDIR com.termux.tasker.extra.STDIN com.termux.tasker.extra.SESSION_ACTION com.termux.tasker.extra.BACKGROUND_CUSTOM_LOG_LEVEL</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>java.lang.String</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>
 					<net.dinglisch.android.tasker.subbundled>true</net.dinglisch.android.tasker.subbundled>
 					<net.dinglisch.android.tasker.subbundled-type>java.lang.Boolean</net.dinglisch.android.tasker.subbundled-type>
 				</Vals>
 			</Bundle>
 			<Str sr="arg1" ve="3">com.termux.tasker</Str>
 			<Str sr="arg2" ve="3">com.termux.tasker.EditConfigurationActivity</Str>
 			<Int sr="arg3" val="10"/>
 			<Int sr="arg4" val="0"/>
 		</Action>
 		<Action sr="act1" ve="7">
 			<code>417</code>
 			<Str sr="arg0" ve="3">Sync/Logseq/assets/logpush/pushWidget/pushWidget0.txt</Str>
 			<Str sr="arg1" ve="3">%TASK1</Str>
 			<Int sr="arg2" val="0"/>
 		</Action>
 		<Action sr="act10" ve="7">
 			<code>1186637727</code>
 			<Bundle sr="arg0">
 				<Vals sr="val">
 					<com.twofortyfouram.locale.intent.extra.BLURB>Set: task5</com.twofortyfouram.locale.intent.extra.BLURB>
 					<com.twofortyfouram.locale.intent.extra.BLURB-type>java.lang.String</com.twofortyfouram.locale.intent.extra.BLURB-type>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>org.kustom.tasker.VAR_NAME org.kustom.tasker.VAR_VALUE</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>java.lang.String</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>
 					<net.dinglisch.android.tasker.subbundled>true</net.dinglisch.android.tasker.subbundled>
 					<net.dinglisch.android.tasker.subbundled-type>java.lang.Boolean</net.dinglisch.android.tasker.subbundled-type>
 					<org.kustom.tasker.VAR_NAME>task5</org.kustom.tasker.VAR_NAME>
 					<org.kustom.tasker.VAR_NAME-type>java.lang.String</org.kustom.tasker.VAR_NAME-type>
 					<org.kustom.tasker.VAR_VALUE>%TASK5</org.kustom.tasker.VAR_VALUE>
 					<org.kustom.tasker.VAR_VALUE-type>java.lang.String</org.kustom.tasker.VAR_VALUE-type>
 					<org.kustom.tasker.extra.INT_VERSION_CODE>376422110</org.kustom.tasker.extra.INT_VERSION_CODE>
 					<org.kustom.tasker.extra.INT_VERSION_CODE-type>java.lang.Integer</org.kustom.tasker.extra.INT_VERSION_CODE-type>
 				</Vals>
 			</Bundle>
 			<Str sr="arg1" ve="3">org.kustom.widget</Str>
 			<Str sr="arg2" ve="3">org.kustom.lib.editor.tasker.EditVarActivity</Str>
 			<Int sr="arg3" val="0"/>
 			<Int sr="arg4" val="1"/>
 		</Action>
 		<Action sr="act11" ve="7">
 			<code>523</code>
 			<Str sr="arg0" ve="3">LogPush</Str>
 			<Str sr="arg1" ve="3">Push complete!</Str>
 			<Str sr="arg10" ve="3"/>
 			<Str sr="arg11" ve="3">Logpush</Str>
 			<Str sr="arg12" ve="3"/>
 			<Img sr="arg2" ve="2">
 				<nme>hd_navigation_refresh</nme>
 			</Img>
 			<Int sr="arg3" val="0"/>
 			<Int sr="arg4" val="0"/>
 			<Int sr="arg5" val="2"/>
 			<Int sr="arg6" val="0"/>
 			<Int sr="arg7" val="0"/>
 			<Int sr="arg8" val="0"/>
 			<Str sr="arg9" ve="3"/>
 		</Action>
 		<Action sr="act2" ve="7">
 			<code>417</code>
 			<Str sr="arg0" ve="3">Sync/Logseq/assets/logpush/pushWidget/pushWidget1.txt</Str>
 			<Str sr="arg1" ve="3">%TASK2</Str>
 			<Int sr="arg2" val="0"/>
 		</Action>
 		<Action sr="act3" ve="7">
 			<code>417</code>
 			<Str sr="arg0" ve="3">Sync/Logseq/assets/logpush/pushWidget/pushWidget2.txt</Str>
 			<Str sr="arg1" ve="3">%TASK3</Str>
 			<Int sr="arg2" val="0"/>
 		</Action>
 		<Action sr="act4" ve="7">
 			<code>417</code>
 			<Str sr="arg0" ve="3">Sync/Logseq/assets/logpush/pushWidget/pushWidget3.txt</Str>
 			<Str sr="arg1" ve="3">%TASK4</Str>
 			<Int sr="arg2" val="0"/>
 		</Action>
 		<Action sr="act5" ve="7">
 			<code>417</code>
 			<Str sr="arg0" ve="3">Sync/Logseq/assets/logpush/pushWidget/pushWidget4.txt</Str>
 			<Str sr="arg1" ve="3">%TASK5</Str>
 			<Int sr="arg2" val="0"/>
 		</Action>
 		<Action sr="act6" ve="7">
 			<code>1186637727</code>
 			<Bundle sr="arg0">
 				<Vals sr="val">
 					<com.twofortyfouram.locale.intent.extra.BLURB>Set: task1</com.twofortyfouram.locale.intent.extra.BLURB>
 					<com.twofortyfouram.locale.intent.extra.BLURB-type>java.lang.String</com.twofortyfouram.locale.intent.extra.BLURB-type>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>org.kustom.tasker.VAR_NAME org.kustom.tasker.VAR_VALUE</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>java.lang.String</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>
 					<net.dinglisch.android.tasker.subbundled>true</net.dinglisch.android.tasker.subbundled>
 					<net.dinglisch.android.tasker.subbundled-type>java.lang.Boolean</net.dinglisch.android.tasker.subbundled-type>
 					<org.kustom.tasker.VAR_NAME>task1</org.kustom.tasker.VAR_NAME>
 					<org.kustom.tasker.VAR_NAME-type>java.lang.String</org.kustom.tasker.VAR_NAME-type>
 					<org.kustom.tasker.VAR_VALUE>%TASK1</org.kustom.tasker.VAR_VALUE>
 					<org.kustom.tasker.VAR_VALUE-type>java.lang.String</org.kustom.tasker.VAR_VALUE-type>
 					<org.kustom.tasker.extra.INT_VERSION_CODE>376422110</org.kustom.tasker.extra.INT_VERSION_CODE>
 					<org.kustom.tasker.extra.INT_VERSION_CODE-type>java.lang.Integer</org.kustom.tasker.extra.INT_VERSION_CODE-type>
 				</Vals>
 			</Bundle>
 			<Str sr="arg1" ve="3">org.kustom.widget</Str>
 			<Str sr="arg2" ve="3">org.kustom.lib.editor.tasker.EditVarActivity</Str>
 			<Int sr="arg3" val="0"/>
 			<Int sr="arg4" val="1"/>
 		</Action>
 		<Action sr="act7" ve="7">
 			<code>1186637727</code>
 			<Bundle sr="arg0">
 				<Vals sr="val">
 					<com.twofortyfouram.locale.intent.extra.BLURB>Set: task2</com.twofortyfouram.locale.intent.extra.BLURB>
 					<com.twofortyfouram.locale.intent.extra.BLURB-type>java.lang.String</com.twofortyfouram.locale.intent.extra.BLURB-type>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>org.kustom.tasker.VAR_NAME org.kustom.tasker.VAR_VALUE</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>java.lang.String</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>
 					<net.dinglisch.android.tasker.subbundled>true</net.dinglisch.android.tasker.subbundled>
 					<net.dinglisch.android.tasker.subbundled-type>java.lang.Boolean</net.dinglisch.android.tasker.subbundled-type>
 					<org.kustom.tasker.VAR_NAME>task2</org.kustom.tasker.VAR_NAME>
 					<org.kustom.tasker.VAR_NAME-type>java.lang.String</org.kustom.tasker.VAR_NAME-type>
 					<org.kustom.tasker.VAR_VALUE>%TASK2</org.kustom.tasker.VAR_VALUE>
 					<org.kustom.tasker.VAR_VALUE-type>java.lang.String</org.kustom.tasker.VAR_VALUE-type>
 					<org.kustom.tasker.extra.INT_VERSION_CODE>376422110</org.kustom.tasker.extra.INT_VERSION_CODE>
 					<org.kustom.tasker.extra.INT_VERSION_CODE-type>java.lang.Integer</org.kustom.tasker.extra.INT_VERSION_CODE-type>
 				</Vals>
 			</Bundle>
 			<Str sr="arg1" ve="3">org.kustom.widget</Str>
 			<Str sr="arg2" ve="3">org.kustom.lib.editor.tasker.EditVarActivity</Str>
 			<Int sr="arg3" val="0"/>
 			<Int sr="arg4" val="1"/>
 		</Action>
 		<Action sr="act8" ve="7">
 			<code>1186637727</code>
 			<Bundle sr="arg0">
 				<Vals sr="val">
 					<com.twofortyfouram.locale.intent.extra.BLURB>Set: task3</com.twofortyfouram.locale.intent.extra.BLURB>
 					<com.twofortyfouram.locale.intent.extra.BLURB-type>java.lang.String</com.twofortyfouram.locale.intent.extra.BLURB-type>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>org.kustom.tasker.VAR_NAME org.kustom.tasker.VAR_VALUE</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>java.lang.String</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>
 					<net.dinglisch.android.tasker.subbundled>true</net.dinglisch.android.tasker.subbundled>
 					<net.dinglisch.android.tasker.subbundled-type>java.lang.Boolean</net.dinglisch.android.tasker.subbundled-type>
 					<org.kustom.tasker.VAR_NAME>task3</org.kustom.tasker.VAR_NAME>
 					<org.kustom.tasker.VAR_NAME-type>java.lang.String</org.kustom.tasker.VAR_NAME-type>
 					<org.kustom.tasker.VAR_VALUE>%TASK3</org.kustom.tasker.VAR_VALUE>
 					<org.kustom.tasker.VAR_VALUE-type>java.lang.String</org.kustom.tasker.VAR_VALUE-type>
 					<org.kustom.tasker.extra.INT_VERSION_CODE>376422110</org.kustom.tasker.extra.INT_VERSION_CODE>
 					<org.kustom.tasker.extra.INT_VERSION_CODE-type>java.lang.Integer</org.kustom.tasker.extra.INT_VERSION_CODE-type>
 				</Vals>
 			</Bundle>
 			<Str sr="arg1" ve="3">org.kustom.widget</Str>
 			<Str sr="arg2" ve="3">org.kustom.lib.editor.tasker.EditVarActivity</Str>
 			<Int sr="arg3" val="0"/>
 			<Int sr="arg4" val="1"/>
 		</Action>
 		<Action sr="act9" ve="7">
 			<code>1186637727</code>
 			<Bundle sr="arg0">
 				<Vals sr="val">
 					<com.twofortyfouram.locale.intent.extra.BLURB>Set: task4</com.twofortyfouram.locale.intent.extra.BLURB>
 					<com.twofortyfouram.locale.intent.extra.BLURB-type>java.lang.String</com.twofortyfouram.locale.intent.extra.BLURB-type>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>org.kustom.tasker.VAR_NAME org.kustom.tasker.VAR_VALUE</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS>
 					<net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>java.lang.String</net.dinglisch.android.tasker.extras.VARIABLE_REPLACE_KEYS-type>
 					<net.dinglisch.android.tasker.subbundled>true</net.dinglisch.android.tasker.subbundled>
 					<net.dinglisch.android.tasker.subbundled-type>java.lang.Boolean</net.dinglisch.android.tasker.subbundled-type>
 					<org.kustom.tasker.VAR_NAME>task4</org.kustom.tasker.VAR_NAME>
 					<org.kustom.tasker.VAR_NAME-type>java.lang.String</org.kustom.tasker.VAR_NAME-type>
 					<org.kustom.tasker.VAR_VALUE>%TASK4</org.kustom.tasker.VAR_VALUE>
 					<org.kustom.tasker.VAR_VALUE-type>java.lang.String</org.kustom.tasker.VAR_VALUE-type>
 					<org.kustom.tasker.extra.INT_VERSION_CODE>376422110</org.kustom.tasker.extra.INT_VERSION_CODE>
 					<org.kustom.tasker.extra.INT_VERSION_CODE-type>java.lang.Integer</org.kustom.tasker.extra.INT_VERSION_CODE-type>
 				</Vals>
 			</Bundle>
 			<Str sr="arg1" ve="3">org.kustom.widget</Str>
 			<Str sr="arg2" ve="3">org.kustom.lib.editor.tasker.EditVarActivity</Str>
 			<Int sr="arg3" val="0"/>
 			<Int sr="arg4" val="1"/>
 		</Action>
 		<Img sr="icn" ve="2">
 			<nme>hl_navigation_refresh</nme>
 		</Img>
 	</Task>
 </TaskerData>
 ```
</details>

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
