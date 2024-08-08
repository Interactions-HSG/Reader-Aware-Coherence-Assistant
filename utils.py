import json
def load_config():
    d = dict()
    with open("config.json", "r") as f:
        config_str = f.read()
        d = json.loads(config_str)
    return d