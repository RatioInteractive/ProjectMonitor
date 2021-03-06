from toto.invocation import *
from toto.exceptions import *
from toto.events import EventManager
import view
from time import time

ERROR_INVALID_PROJECT = 2002

ARGS = ['name','hours_spent','hours_budgeted','story_progress','project_progress']

@requires(*ARGS)
def invoke(handler, params):
  if not handler.connection.db.projects.find_one({'name': params['name']}):
    raise TotoException(ERROR_INVALID_PROJECT, "No project exists with that name.")
  values = dict([[k, params[k]] for k in ARGS])
  values['story_progress'] /= 100.0
  values['project_progress'] /= 100.0
  values['timestamp'] = time()
  handler.connection.db.updates.insert(values)
  EventManager.instance().send("project_updated", {'name': params['name']})
  return view.invoke(handler, {'name': params['name']})
