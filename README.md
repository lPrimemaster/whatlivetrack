# whatlivetrack
A simple python script that checks for Garmin Live Track emails and sends the url for spectating your session to your contacts via whatsapp.
# Manual Installing

0. If you want to create a venv.
```
python -m venv .env
source ./.env/Scripts/activate
```

1. Setup google api for gmail.
    - Sign in to Google Cloud console and create a New Project or continue with an existing project.
    - Go to APIs and Services.
    - Enable Gmail API for the selected project.
    - Configure the Consent screen by clicking on OAuth Consent Screen if it is not already configured.
    - Enter the Application name and save it.
    - Go to Credentials.
    - Click on Create credentials, and go to OAuth Client ID.
    - Choose application type as Desktop Application.
    - Enter the Application name, and click on the Create button.
    - The Client ID will be created. Download it to your computer and save it as credentials.json on this README's directory.

2. Setup the project dependecies.
```
pip install -r requirements.txt
```

3. Allow your application to access your email by running it once manually.
    - If running scripts is enabled on your system
    ```
    ./run_task.ps1
    ```
    - If running scripts is disabled on your system
    ```
    powershell -ExecutionPolicy ByPass -File .\run_task.ps1
    ```

4. Create a schedule on the command at stage 3. if you wish to check for emails periodically, and send messages.
