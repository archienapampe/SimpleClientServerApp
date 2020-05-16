import logging
import os

basedir = os.path.abspath(os.path.dirname(__file__))

COFFEE_MACHINE_DB = f'{basedir}/menu.sqlite'
TABLE_NAME_FOR_DRINKS = 'drinks'
TABLE_NAME_FOR_INGREDIENTS = 'ingredients'

LOGGER_CONFIG = dict(level=logging.INFO,
                     file=f'{basedir}/history.log',
                     formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                    )