from termcolor import colored
import requests
from Utilities.ConfigManager import ConfigManager
from ConfigUtilities import *


class ProjectUtilities:
    def __init__(self):
        self.actions = ["list", "get","create","current_project"]
        self.config = ConfigManager()
        self.conf_utils = ConfigUtilities()
        self.endpoint = '/scheduler/api/v1.0'
        self.url = "http://" + str(self.config.get('api', 'host')) + ":" + str(self.config.get('api', 'port'))
        self.url = self.url + self.endpoint

    def get_project_doc(self):
        doc = "The " + colored("project", "green") + " command manages project level actions." \
                                                     " set the " + colored("--action",
                                                                           "yellow") + " argument to %s|%s|%s" % (
                  colored("list", "blue"), colored("create", "blue"), colored("delete", "blue"))
        doc = doc + "\n\n The " + colored("list", "blue") + " action lists all projects"
        doc = doc + "\n\n The " + colored("get", "blue") + " action gets a specific project use " + \
              colored("--name", "yellow") + " or " + colored("--id", "yellow")
        doc = doc + "\n\n The " + colored("create", "blue") + " action creates a new project use "+\
            colored("--from-file","yellow")+" to create from json file"
        doc = doc + "\n\n The " + colored("delete", "blue") + " action deletes a project use "+ \
              colored("--name", "yellow") + " or " + colored("--id", "yellow")
        return doc

    def list(self, kwargs):
        r = requests.get(self.url + '/projects')
        projects = r.json()
        print(json.dumps(projects, indent=4))

    def get(self, kwargs):
        if 'name' in kwargs:
            r = requests.get(self.url + '/projects')
            projects = r.json()
            project = [project for project in projects['projects'] if project['name'] == kwargs['name']]
            print(json.dumps(project, indent=4))
        elif 'id' in kwargs:
            r = requests.get(self.url + '/project/' + str(kwargs['id']))
            project = r.json()
            print(json.dumps(project, indent=4))

    def create(self,kwargs):
        if 'from_file' in kwargs:
            try:
                with open(kwargs['from_file']) as f:
                    data = json.loads(f.read())


            except:
                print(colored("File named "+str(kwargs['from_file'])+" not found","red"))
                sys.exit(1)
        else:
            data ={}
            data["name"] = input(colored("Enter project name: ","green"))
            data["description"] = input(colored("Enter project description: ","green"))
            data["creator"] = input(colored("Enter project project creator email: ","green"  ))

        x = requests.post(self.url + '/projects', json=data)
        print(x.text)

    def current_project(self,kwargs):
        if 'set' in kwargs:
            r = requests.get(self.url + '/projects')
            projects = r.json()
            project = [project for project in projects['projects'] if project['name'] == kwargs['set']]
            if len(project) == 0:
                print(colored(kwargs['set']+" is unknown!!","red"))
            self.config.set('projects','default',kwargs['set'])
            self.config.persist()
            sys.exit(0)
        if 'get' in kwargs:
            current=self.config.get('projects','default')
            print(colored("Current project: ","blue")+colored(current,"green"))



        print(kwargs)
        print(self.config.get_all())


    def run(self, action, kwargs):
        if action.lower() in self.actions:
            method = getattr(self, action.lower())
            if self.conf_utils.check_conf(self.config) == False:
                print(colored("CLI incorrectly configured ", "red"))
                sys.exit(1)
            method(kwargs)
