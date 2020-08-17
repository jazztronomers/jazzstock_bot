import common.connector_db as db
import config.condition as condition
import config.config as cf
import sys
import os
import jazzstock_bot

PATH_DIC={
}


if 'INSTANCE_ID' in os.environ:
	INSTANCE_ID = os.environ['INSTANCE_ID']

else:
	INSTANCE_ID = 'T01'

PATH_SRC_ROOT = jazzstock_bot.__file__.replace('__init__.py','')
PATH_SIMULATION = os.path.join(PATH_SRC_ROOT, 'simulation')
PATH_CORE = os.path.join(PATH_SRC_ROOT, 'core')
PATH_MAIN = os.path.join(PATH_SRC_ROOT, 'main')
PATH_LOG = os.path.join(PATH_SRC_ROOT, 'log')





