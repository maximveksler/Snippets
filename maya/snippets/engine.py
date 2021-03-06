#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2009 - 2013 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#**********************************************************************************************************************

"""
**loader.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Engine module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os

#**********************************************************************************************************************
#***	Dependencies globals manipulation.
#**********************************************************************************************************************
import foundations.globals.constants
from snippets.globals.constants import Constants

def _overrideDependenciesGlobals():
	"""
	This definition overrides dependencies globals.

	:return: Definition success. ( Boolean )
	"""

	foundations.globals.constants.Constants.logger = Constants.logger
	return True

_overrideDependenciesGlobals()

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose
import snippets.libraries.common
from snippets.globals.runtimeGlobals import RuntimeGlobals
from snippets.managers.modulesManager import ModulesManager

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Ui_Loader_Setup", "Ui_Loader_Type", "Loader"]

LOGGER = foundations.verbose.installLogger()

# Remove existing handlers.
del logging.root.handlers[:]

foundations.verbose.getLoggingConsoleHandler()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def _setModulesManager():
	"""
	This definition sets the global modules manager instance.
	"""

	if not isinstance(RuntimeGlobals.modulesManager, ModulesManager):
		RuntimeGlobals.modulesManager = ModulesManager([RuntimeGlobals.librariesDirectory])
		RuntimeGlobals.modulesManager.registerAll()

def run():
	"""
	This definition starts the Application.

	:return: Definition success. ( Boolean )
	"""

	RuntimeGlobals.librariesDirectory = os.path.join(os.path.dirname(__file__), Constants.librariesDirectory)
	RuntimeGlobals.resourcesDirectory = os.path.join(os.path.dirname(__file__), Constants.resourcesDirectory)

	_setModulesManager()
