# django-salesforce
#
# by Phil Christensen
# (c) 2012 Working Today
# See LICENSE.md for details
#

"""
Salesforce database backend for Django.
"""

import logging

from django.core.exceptions import ImproperlyConfigured
from django.db.backends import BaseDatabaseFeatures, BaseDatabaseWrapper

from django.db.backends.postgresql_psycopg2.base import PostgresqlDatabaseOperations

from salesforce.backend.client import DatabaseClient
from salesforce.backend.creation import DatabaseCreation
from salesforce.backend.introspection import DatabaseIntrospection
from salesforce.backend.validation import DatabaseValidation
from salesforce.backend.operations import DatabaseOperations

from salesforce import sfauth

log = logging.getLogger(__name__)

class DatabaseError(Exception):
	pass

class IntegrityError(DatabaseError):
	pass

class DatabaseFeatures(BaseDatabaseFeatures):
	pass

class DatabaseWrapper(BaseDatabaseWrapper):
	vendor = 'salesforce'
	operators = {
		'exact': '= %s',
		'iexact': 'LIKE %s',
		'contains': 'LIKE BINARY %s',
		'icontains': 'LIKE %s',
		'regex': 'REGEXP BINARY %s',
		'iregex': 'REGEXP %s',
		'gt': '> %s',
		'gte': '>= %s',
		'lt': '< %s',
		'lte': '<= %s',
		'startswith': 'LIKE BINARY %s',
		'endswith': 'LIKE BINARY %s',
		'istartswith': 'LIKE %s',
		'iendswith': 'LIKE %s',
	}

	def __init__(self, settings_dict, alias='default'):
		super(DatabaseWrapper, self).__init__(settings_dict, alias)
		
		self.features = DatabaseFeatures(self)
		self.ops = DatabaseOperations(self)
		self.client = DatabaseClient(self)
		self.creation = DatabaseCreation(self)
		self.introspection = DatabaseIntrospection(self)
		self.validation = DatabaseValidation(self)
	
	def _cursor(self):
		from salesforce.backend.query import CursorWrapper
		cursor = CursorWrapper(self.settings_dict)
		return cursor
	
	def quote_name(self, name):
		return name
