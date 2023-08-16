import json
import requests
import pytz as tz
from datetime import datetime


class Prayer_API:
    def __init__(self) -> None:
        self.link = "https://api.aladhan.com/v1/calendarByAddress/"

    def api_request(self, year: int, month: int, address: str) -> dict:
        return json.loads(requests.get(self.link + f'{year}/{month}?address={address}&method=2&school=1').text)
    
    def get_timezone(self, location: str):

        #Finds prayer timezone based off location
        times = datetime.now()
        j_data = self.api_request(times.year, times.month, location)
        return j_data['data'][0]['meta']['timezone']

    def get_all_times(self, location: str):

        #Returns datetime object for the specified location
        timezone = tz.timezone(self.get_timezone(location))
        return datetime.now(timezone)

        
    def get_prayer_times(self, location: str) -> str:

        #Retrieves prayer timings from the API and returns them as datetime objects
        times = self.get_all_times(location)
        j_data = self.api_request(times.year, times.month, location)

        prayer_times = j_data['data'][times.day-1]['timings']

        for key in prayer_times:
            time = prayer_times[key][:5]
            format = "%H:%M"
            prayer_times[key] = datetime.strptime(time, format).time()
            
        return prayer_times

