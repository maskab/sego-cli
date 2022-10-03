import os, shutil, sys
import time
from pathlib import Path
import subprocess
from termcolor import colored
from time import sleep
import requests
from zipfile import ZipFile


class SetupUtilities:

    def __init__(self):
        self.sego_home = Path.home() / ".sego"
        self.working_dir = Path(os.getcwd())

    @staticmethod
    def setup_documentation():
        doc = "The setup command setups up the %s environment" % (colored("equant-scheduler", "green"))
        return doc

    def check_setup(self):
        try:
            import fire, termcolor, prettytable
        except:
            return False
        return True

    def setup(self):
        deps = ['fire','termcolor','prettytable']
        for dep in deps:
            self.installer(dep)

    def installer(self, package, req_file=False):
        if req_file:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", package])
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    def virtualenv(self, name, directory):

        current_working_dir = os.getcwd()
        os.chdir(directory)
        subprocess.check_call(["python", "-m", "virtualenv", name, "--python", "python3"])
        os.chdir(current_working_dir)
