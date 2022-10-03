import os, json
from pathlib import Path


class ConfigManager:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.configs = {}
        self.home_directory = Path.home()
        self.conf_dir_name = "scheduler_cli"
        self.conf_directory = self.home_directory / self.conf_dir_name
        # self.load_config()

    def load_config(self):
        for file_name in os.listdir(self.conf_directory):
            config_name = file_name.split(".")[0]
            with open(self.conf_directory / file_name, "r") as con_file:
                try:
                    self.configs[config_name] = json.loads(con_file.read())
                except:
                    print('%s not formatted properly,please use json formatting' % file_name)

    def get_all(self):
        return self.configs

    def check_config(self,config):
        if config in self.configs.keys():
            return True
        else:
            return False

    def get(self, name, field=None):
        if field != None:
            try:
                return self.configs[name][field]
            except:
                print("configuration %s or field %s are not set" % (name, field))
        else:
            try:
                return self.configs[name]
            except:
                print("configuration %s is not set" % (name))

    def set(self, config, field, value=None ):
        if type(field) == str:
            try:
                self.configs[config][field] = value
            except:
                self.configs[config] = {}
                self.configs[config][field] = value
        elif (type(field) == dict or type(field) == list) and value == None:
            try:
                self.configs[config] = field
            except:
                pass

    def persist_configuration(self,configuration):
        with open(str(self.conf_directory/configuration)+".json","w+") as f:
            data = self.configs[configuration]
            f.write(json.dumps(data))

    def persist(self):
        for configuration in self.configs.keys():
            self.persist_configuration(configuration)

    def check_conf_directory(self):
        if os.path.exists(self.conf_directory):
            return True
        else:
            return False

    def create_conf_directory(self):
        if not self.check_conf_directory():
            try:
                os.mkdir(path=self.conf_directory)
                print("Created")
            except:
                pass

    def get_config_directory(self):
        return self.conf_directory
