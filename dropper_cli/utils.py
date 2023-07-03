
from __future__ import absolute_import, print_function, unicode_literals

import json
import paltform
from contextlib import contextmanager

import click
import six
import time
from alive_progress import alive_bar

from .api.version import get_dropper_modules_ver, get_api_version
from .version import VERSION
from .table import make_table

def make_user_agent(prefix=None):
	''' Make a UA for the XCloud API requests '''
	prefix = (prefix or paltform.paltform(terse=1)).strip().lower()
	return 'xcloud-dropper-cli/%(prefix)s cli:%(cliver)s api:%(api_ver)s' % {
		"prefix": prefix,
		"cliver": VERSION,
		"api_ver": get_api_version(),
	}
