# SMS-Prayer-Reminder

## Description

SMS-Prayer-Reminder is a Python program that notifies users of Islamic prayer times based on their location. It utilizes the Twilio API to send SMS notifications to users reminding them of prayer times. This tool is especially useful for Muslims who want to receive timely reminders for their daily prayers.

## Usage

1. Clone this repository to your local machine.

2. Install the required Python libraries by running:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Twilio API credentials. Open `.env` and replace the following placeholders with your Twilio account details:

    ```python
    # Twilio API Credentials
    TWILIO_ACCOUNT_SID = 'your_account_sid'
    TWILIO_AUTH_TOKEN = 'your_auth_token'
    TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'
    ```

4. Run the program:

    ```bash
    python main.py
    ```

## Features

- Automatically calculates Islamic prayer times based on the user's geographical location.

- Sends SMS notifications using the Twilio API to remind users of prayer times.

- Customizable notification messages.

- Easily configurable for different geographic locations.
