
import json
import asyncio
import requests
import pytz as tz
from os import getenv

from User import UsersDB
from MoreTools import utils
from Prayer import Prayer_API

from random import choice
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client
from time import time

load_dotenv()

salah = Prayer_API()
profiles = UsersDB("data/profiles.json")

islamic_data = utils.grab_file_data('data/islam.json')




class Twilio:
    def __init__(self, phone: str, token: str, sid: str) -> None:

        self.phone = phone
        self.auth_token = getenv(token)
        self.account_sid = getenv(sid)
        self.client = Client(self.account_sid, self.auth_token)

        self.signoff = [
            "Have a great day!", 
            "Sincerely,", 
            "May Allah SWT guide us all.",
            "Keep it up!",
            "Good luck!",
            "Thanks,",
            "You got this!"
        ]

        self.author = "\n - Ibrahim's Islamic Reminder"
        self.disclaimer = "\n\n***DISCLAIMER*** \n This automated process will not view or respond to your messages"

        self.limit_user_reminders = {}

    def limit_reminders(self, phone: str, message_type: str) -> bool:

        #Adds a 70 second cooldown between reminder sms messages

        if message_type != 'Reminder':
            return
        
        limit_seconds = 70
        limit = False
        current_time = time()

        limited_users = [user for user in self.limit_user_reminders]

        if phone in limited_users:
            limit = True
            time_elasped = current_time - self.limit_user_reminders[phone]

            if time_elasped > limit_seconds:
                limit = False
                del self.limit_user_reminders[phone]
        
        else:
            self.limit_user_reminders[phone] = current_time

        return limit
    
    def sms(self, phone: str, content: str, message_type: str = None) -> None:
        
        #Limits sms message being sent to users, primarily the reminders.
        if self.limit_reminders(phone=phone, message_type=message_type):
            return

        print(f'{content} sent to {phone} | {message_type}')

        signoff = "\n\n" + choice(self.signoff) if not message_type == 'Fact' else ''

        message = self.client.messages.create(
           from_=self.phone,
           body= content + (signoff) + self.author + self.disclaimer,
           to=phone
         )
        

        


twilio = Twilio(phone='+12512443133', token="TWILIO_AUTH_TOKEN", sid="TWILIO_ACCOUNT_SID")

@utils.loop_command(seconds=60*60*12)
def islamic_fact() -> None:

    """
    ------------------>
    
    Sends an Islamic Fact to each user everyday!
    Keeps users educated on religion, practices and history.

    <------------------
    """

    facts = islamic_data['facts']
    all_profiles = profiles.get()
    fact = choice(facts[choice([t for t in facts])])

    for name in all_profiles:

        profile = all_profiles[name]
        phone = profile['phone']

        twilio.sms(phone=phone, content=fact, message_type='Fact')




@utils.loop_command(seconds=30)
def remind_prayer() -> None:

    """
    ------------------>
    
    Reminds users of prayer timings.
    Updates every 30 seconds to check times based off of user's location.
    Makes use of the Prayer API and datetime import to calculate times.
    Uses Twilio API to send sms messages and remind each profile.

    <------------------
    """

    all_profiles = profiles.get()
    for name in all_profiles:
        


        if name != "Ibrahim Ellahi":
            continue




        profile = all_profiles[name]
        phone = profile['phone']
        location = profile['location']

        #Get current time in the user's location, as well as the respective prayer times
        current_time = salah.get_all_times(location=location).time()
        prayer_times = salah.get_prayer_times(location=location)


        all_prayers = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
        for prayer in prayer_times:

            #Timings like sunrise and midnight aren't included
            if not prayer in all_prayers:
                continue

            time = prayer_times[prayer]
            
            t_time = (time.hour, time.minute)
            t_current_time = (current_time.hour, current_time.minute)

            if t_time == t_current_time:
                
                first_name, last_name = name.split()

                #Convert time values to strings checking lengths
                t_str = [len(str(t)) <= 1 for t in t_time]

                #Place holders for single digit numbers for example 4, 5 => 04:05
                pholders = {True: '0', False: ''}

                message = f"""
                Salam, {first_name}!\n
                Just a friendly reminder that it is time for {prayer} ({pholders[t_str[0]]}{t_time[0]}:{pholders[t_str[1]]}{t_time[1]}).
                Please perform wudhu and make Ibadat to Allah SWT, he's calling upon you as of right now.
                A Muslim is not defined solely by their beliefs; rather, their identity as a Muslim is also shaped by their actions. 
                To truly be a Muslim, it is essential to embrace both faith and deeds.
            """

                benefits = f'\nWhy? -> {choice(islamic_data["prayer"])}'
                

                twilio.sms(phone=phone, content=message+benefits, message_type='Reminder')


def welcome_users() -> None:

    all_profiles = profiles.get()

    for name in all_profiles:

        first_name, last_name = name.split()
        profile = all_profiles[name]
        phone = profile['phone']

        welcome_message = f"""
        Hi {first_name}, you're one of the users who've been added to Ibrahim's Islamic Reminders!
        As we move forward, the introduction of new features may be a possiblity. For now, you can expect to receive prayer reminders based on your profile's location and interesting Islamic Facts. 
        Please note that this project is in its initial stages, and testing will persist as we refine its functionality.
        Let us collectively strive to expand our knowledge and evolve into the finest versions of ourselves. This application serves as a conduit for us to forge a deeper connection with our Creator and enhance our journey as devout Muslims. It is important to acknowledge that perfection eludes us all, and our shared pursuit is not without its challenges. With this understanding, we embark on a path of continuous improvement, nurturing our spiritual growth and aligning ourselves with the teachings of Islam. Let the purpose of this platform be a source of inspiration, urging us to pursue excellence while recognizing the inherent imperfections that make us human.
        Thank you for your time.
        (Report Any Bugs at @ibra.himo on Discord)
        """
        twilio.sms(phone=phone, content=welcome_message)




async def main() -> None:

    #Adding all tasks to run asynchronously
    tasks = [
        asyncio.create_task(remind_prayer()),
        asyncio.create_task(islamic_fact())
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())



