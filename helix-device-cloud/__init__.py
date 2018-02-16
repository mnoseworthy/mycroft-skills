# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


from random import randrange

import re
import traceback
from adapt.intent import IntentBuilder
from os.path import join, dirname

from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util import read_stripped_lines
from mycroft.util.log import getLogger
from mycroft.skills.context import *

__author__ = 'mnoseworthy'

LOGGER = getLogger(__name__)


class HelixDeviceCloudSkill(MycroftSkill):
    def __init__(self):
        """
            Initialize
        """
        # Run parent constructor
        super(HelixDeviceCloudSkill, self).__init__(name="HelixDeviceCloudSkill")
        # Load attributes required for implementing skill
        self.feedback_prefix = read_stripped_lines(
            join(dirname(__file__), 'dialog', self.lang,
                 'FeedbackPrefix.dialog')
        )
        self.feedback_run = read_stripped_lines(
            join(dirname(__file__), 'dialog', self.lang,
                 'FeedbackRun.dialog')
        )

        # Load device config file & decalre variables required for connecting
        # to Helix Device Cloud

    def initialize(self):
        """
            Load and initialize the various intent's requried for skill
        """
        # Load request intent, which is the trigger point for the conversation
        # used to run methods against Helix Device Cloud
        #request_method = IntentBuilder("HelixDeivceCloudIntent").require(
        #    "HelixDeviceCloudKeyword").require("MethodRequest").build()
        #request_method = IntentBuilder("HelixDeivceCloudIntent").require("MethodRequest").build()
        #run_method = IntentBuilder("HelixDeviceCloudIntent").require("method").require("HelixMethodContext").build()

        # Register callbacks against loaded intent structures
        #self.register_intent(request_method, self.request_method)
        #self.register_intent(run_method, self.run_method)

        # Create connection to HDC and store in attribute

    @intent_handler(IntentBuilder("RequestMethodIntent").require("MethodRequest").build())
    @adds_context("HelixMethodContext")
    def request_method(self, message):
        """
            Asks user for the method they would like to run against
            helix
        """
        try:
            self.speak("What method would you like to execute?", expect_response=True)
        except Exception as e:
            traceback.print_exc()

    @intent_handler(IntentBuilder("RunMethodIntent").require("method").require("HelixMethodContext").build())
    @removes_context("HelixMethodContext")
    def run_method(self, message):
        """
            Executes a method at HDC and returns the result
        """
        print(message)
        try:
            # Respond that mycroft is attempting to execute the method
            #self.speak("Hello from helix device cloud. You ran method : {}".format(message.data))
            for key, value in message.data.items():
                self.speak("Key: {}, Value: {} \n".format(key, value))
            # Use the open connection to HDC to execute the requested method
        except Exception as e:
            LOGGER.error("Error: {0}".format(e))
            traceback.print_exc()
            
    def stop(self):
        pass


def create_skill():
    """
        Just returns an object of the skill we've defined in the rest of this file,
        presumably used by mycroft on load-time to load up everything in parllel.
    """
    return HelixDeviceCloudSkill()
