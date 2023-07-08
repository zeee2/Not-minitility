import json


class ConfigManager:
    def __init__(self):
        self.config = {
            "Current": "1",
            "Profile_1": {
                "rt": "0",
                "crt": "0",
                "rtus": "10",
                "rtds": "10",
                "lh": "380",
                "uh": "390",
            },
            "Profile_2": {
                "rt": "0",
                "crt": "0",
                "rtus": "10",
                "rtds": "10",
                "lh": "380",
                "uh": "390",
            },
            "Profile_3": {
                "rt": "0",
                "crt": "0",
                "rtus": "10",
                "rtds": "10",
                "lh": "380",
                "uh": "390",
            }
        }

    def save_config(self, filename="profile.json"):
        with open(filename, 'w') as file:
            json.dump(self.config, file, indent=4)

    def load_config(self, filename="profile.json"):
        try:
            with open(filename, 'r') as file:
                self.config = json.load(file)
        except:
            return self.save_config()