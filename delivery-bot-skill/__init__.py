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


class DeliveryBotSkill(MycroftSkill):
    def __init__(self):
        """
            Initialize
        """
        # Run parent constructor
        super(DeliveryBotSkill, self).__init__(name="DeliveryBotSkill")
        # Load attributes required for implementing skill
        self.feedback_prefix = read_stripped_lines(
            join(dirname(__file__), 'dialog', self.lang,
                 'FeedbackPrefix.dialog')
        )
        self.feedback_run = read_stripped_lines(
            join(dirname(__file__), 'dialog', self.lang,
                 'FeedbackRun.dialog')
        )

        # Configure API endpoint for hooking into navigation control system

    @intent_handler(IntentBuilder("RequestDeliveryIntent").require("DeliveryBotKeyword").require("RequestDelivery").build())
    @adds_context("DeliveryRequestContext")
    def request_delivery(self, message):
        """
            Asks user for the method they would like to run against
            helix
        """
        try:
            # Speak
            self.speak("Where should I go to?", expect_response=True)
            # Initialize required variables
            self.message = None
            self.destination = None
        except Exception as e:
            traceback.print_exc()

    @intent_handler(IntentBuilder("GiveDeliveryMessageIntent").require("destination").require("DeliveryRequestContext").build())
    @adds_context("DeliveryMessageContext")
    def give_delivery_message(self, message):
        """
            Gets the user's message to be spoken on delivery, when the bot reaches
            the endpoint.
        """
        try:
            # Ask user about where we should go next, talk first so user knows stuff is happening
            self.speak("Where should I go to?", expect_response=True)
            # Parse endpoint for delivery
            destination = message.data['destination']
            # Might be a name or cube # ?
            # Lookup result in respective map dictionary
            # store resolved endpoint to navigation stack
            self.destination = destination
        except Exception as e:
            LOGGER.error("Error: {}".format(e))
            traceback.print_exc()


    @intent_handler(IntentBuilder("RunDeliveryIntent").require("delivery_message").require("DeliveryRequestContext").require("DeliveryMessageContext").build())
    @removes_context("DeliveryMessageContext")
    @removes_context("DeliveryRequestContext")
    def run_delivery(self, message):
        """
            Gets the user's desired destination, sends the drive request to the navigation
            stack, waits for the bot to reach the destination and then speaks the requested
            message to the recipitant.
        """
        try:
            # Store delivery message and speak to user that the delivery is begining
            self.message = message.data["utterance"]
            self.speak("Starting journey to {}".format(self.destination))
            # Pass destination to navigation stack and wait for trip result
            # speak delivery message, which may have been changed depending
            # on the trip result
            self.speak(self.message)
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
