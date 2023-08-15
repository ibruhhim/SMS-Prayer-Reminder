import json

class UsersDB:
    def __init__(self, file: str) -> None:
        self.file = file
    
    def get(self) -> dict:
        #Returns all data within the UsersDB file
        with open(self.file, 'r') as f: return json.load(f)

    def search(self, name: str) -> dict:

        #Searches for user within the file
         
        with open(self.file, 'r') as f:
            data = json.load(f)
            for key in data:
                if key == name:
                    return data[key]

    def add(self, name: str, location: str, phone: str) -> None:

        #Adds user to the DB file

        with open(self.file, "r+") as f:
            profiles = json.load(f)
            profiles[name] = {
                "location": location, 
                "phone": phone
            }

    
            f.seek(0) # Move the file pointer to the beginning
            json.dump(profiles, f, indent=4)


UsersDB('data/profiles.json')