import json
import asyncio

class Utils:

    #All extra tools/functions are located here
    
    def __init__(self) -> None:
        pass

    def loop_command(self, seconds: int) -> object:
        def wrapper(func: object):
            async def inner(*args):
                
                while True:
                    await asyncio.sleep(seconds)
                    func(*args)

            return inner
        return wrapper
    
    def grab_file_data(self, file: str) -> object:
        with open(file, 'r') as f: return json.load(f)
    
utils = Utils()