
import fire
from DocUtilities import *
from ApplicationUtilities import *
from ControllerUtilities import *
from ListUtilities import *
from models.targets import Targets
from termcolor import colored
from orator.exceptions.query import QueryException


@doc(main_docstring())
class Sego(object):
    def __init__(self):
        pass

    @doc(ApplicationUtilities().get_application_doc())
    def app(self,task,**kwargs):
        application_utilities = ApplicationUtilities()
        application_utilities.run(task=task,kwargs=kwargs)

    @doc(ControllerUtilities().get_controller_doc())
    def controller(self,task,**kwargs):
        controller_utilities = ControllerUtilities()
        controller_utilities.run(task=task,kwargs=kwargs)

    



if __name__ == '__main__':
    setup_utils = SetupUtilities()
    db = DatabaseUtilities()
    db_path = db.get_database_path()
    home = setup_utils.get_home_dir()
    if os.path.exists(db_path):
        fire.Fire(Sego)
    else:
        setup_utils.setup()

