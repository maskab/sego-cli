from termcolor import colored
import requests,sys
from Utilities.ConfigManager import *

def validate_config():
    def document(func):
        func.__doc__ = docstring
        return func

    return document

class ConfigUtilities:
    def __init__(self):
        self.actions = ["show", "create"]
        self.config = ConfigManager()
        self.config.create_conf_directory()
        self.config.load_config()


    def get_config_doc(self):
        doc = "The " + colored("config", "green") + " command manages configuration actions." \
                                                    " set the " + colored("--action",
                                                                          "yellow") + " argument to %s|%s" % (
                  colored("show", "blue"), colored("create", "blue"))
        doc = doc + "\n\n The " + colored("show", "blue") + " action shows the current configrations"
        doc = doc + "\n\n The " + colored("create", "blue") + " action creates/updates the configurations"
        return doc

    def check_conf(self, cm):
        if cm.check_config('api') == True:
            api = cm.get('api')
            checksum = {'host', 'port'}
            if checksum.issubset(api.keys()) == True:
                try:
                    url = "http://" + str(api["host"] )+ ":" + str(api["port"])
                    r = requests.get(url + '/health')
                    if r.status_code == 200:
                        return True
                except:
                    return False
        return False

    def show(self, kwargs):
        print(json.dumps(self.config.get_all(), indent=4))

    def create(self, kwargs):
        print(colored("Configure scheduler backend:", "blue"))
        host = input(colored("scheduler backend host address:", "green"))
        port = input(colored("scheduler backend host port:", "green"))
        self.config.set('api',{'host':host, 'port':port})
        if self.check_conf(self.config) == False:
            print(colored("CLI incorrectly configured ", "red") )
            sys.exit(1)
        self.config.persist()

    def run(self, action, kwargs):
        if action.lower() in self.actions:
            method = getattr(self, action.lower())
            method(kwargs)
