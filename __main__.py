from Utilities.ConfigManager import ConfigManager

try:
    import fire
except ModuleNotFoundError:
    pass
try:
    from termcolor import colored
except ModuleNotFoundError:
    pass
from DocUtilities import *
from SetupUtilities import *
from ProjectUtilities import *
from ConfigUtilities import *




@doc(main_docstring())
class Scheduler(object):
    def __init__(self):
        pass

    @doc(ConfigUtilities().get_config_doc())
    def config(self,action,**kwargs):
        config_utilities = ConfigUtilities()
        config_utilities.run(action=action,kwargs=kwargs)

    @doc(ProjectUtilities().get_project_doc())
    def project(self, action, **kwargs):
        project_utilities = ProjectUtilities()
        project_utilities.run(action=action, kwargs=kwargs)


if __name__ == '__main__':
    config = ConfigManager()
    config.create_conf_directory()
    config.load_config()
    setup_utils = SetupUtilities()

    if setup_utils.check_setup():
        fire.Fire(Scheduler)
    else:
        setup_utils.setup()
        print("dd")
