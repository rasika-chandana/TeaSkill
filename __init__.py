# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.
import json
import time

import requests
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from mycroft.skills.context import adds_context, removes_context

API_URL = 'https://mcassist.herokuapp.com'


class AssistMcSkill(MycroftSkill):
	def __init__(self):
		super(AssistMcSkill, self).__init__(name="AssistMcSkill")

		# Initialize working variables used within the skill.
		self.count = 0

	def initialize(self):
		print '--- initialize AssistMcSkill ---'
		# self.schedule_repeating_event(self.on_poll, None, 1.0)

	def on_poll(self):
		print '-- poll at {} --'.format(time.time())

	# The "handle_xxxx_intent" function is triggered by Mycroft when the
	# skill's intent is matched.  The intent is defined by the IntentBuilder()
	# pieces, and is triggered when the user's utterance matches the pattern
	# defined by the keywords.  In this case, the match occurs when one word
	# is found from each of the files:
	#    vocab/en-us/Hello.voc
	#    vocab/en-us/World.voc
	# In this example that means it would match on utterances like:
	#   'Hello world'
	#   'Howdy you great big world'
	#   'Greetings planet earth'
	@intent_handler(IntentBuilder("").require("Hello").require("World"))
	def handle_hello_world_intent(self, message):
		# In this case, respond by simply speaking a canned response.
		# Mycroft will randomly speak one of the lines from the file
		#    dialogs/en-us/hello.world.dialog
		self.speak_dialog("hello.world")

	@intent_handler(IntentBuilder('').require('Call').require('Person'))
	def handle_call_intent(self, message):
		person = message.data.get('Person')
		self.speak_dialog('calling.person', data={'person': person})
		self.speak('Calling {}...'.format(person))

	@intent_handler(IntentBuilder('').require('RemindMeIn').require('Minutes'))
	def handle_call_intent(self, message):
		remind = message.data.get('RemindMeIn')
		self.speak('Sure, I will remind u again in {}.'.format(remind))

	@intent_handler(IntentBuilder("").require("Count").require("Dir"))
	def handle_count_intent(self, message):
		if message.data["Dir"] == "up":
			self.count += 1
		else:  # assume "down"
			self.count -= 1
		self.speak_dialog("count.is.now", data={"count": self.count})

	# The "stop" method defines what Mycroft does when told to stop during
	# the skill's execution. In this case, since the skill's functionality
	# is extremely simple, there is no need to override it.  If you DO
	# need to implement stop, you should return True to indicate you handled
	# it.
	#
	# def stop(self):
	#    return False

	@intent_handler(IntentBuilder('').require("WhatApiUrl"))
	def handle_api_url(self):
		self.speak('Your API URL is {}'.format(API_URL))

	@intent_handler(IntentBuilder('TeaIntent').require("TeaKeyword"))
	@adds_context('MilkContext')
	def handle_tea_intent(self, message):
		self.milk = False
		self.speak('Of course, would you like Milk with that?', expect_response=True)

	@intent_handler(IntentBuilder('UnhandledTeaIntent').require('MilkContext').optionally("Unhandled").build())
	def handle_tea_unhandled_intent(self, message):
		self.speak('Oops, I didn\'t get that', expect_response=True)

	@intent_handler(IntentBuilder('NoMilkIntent').require("NoKeyword").require('MilkContext').build())
	@adds_context('HoneyContext')
	def handle_yes_milk_intent(self, message):
		self.milk = True
		self.speak('all right, any Honey?', expect_response=True)

	@intent_handler(IntentBuilder('YesMilkIntent').require("YesKeyword").require('MilkContext').build())
	@adds_context('HoneyContext')
	def handle_no_milk_intent(self, message):
		self.speak('What about Honey?', expect_response=True)

	@intent_handler(IntentBuilder('NoHoneyIntent').require("NoKeyword").require('HoneyContext').build())
	@removes_context('HoneyContext')
	def handle_no_honey_intent(self, message):
		self.send_order()

	@intent_handler(IntentBuilder('YesHoneyIntent').require("YesKeyword").require('HoneyContext').build())
	@removes_context('HoneyContext')
	def handle_yes_honey_intent(self, message):
		self.send_order()

	@intent_handler(IntentBuilder('UnhandledTeaIntent').require('HoneyContext').optionally("Unhandled").build())
	def handle_honey_unhandled_intent(self, message):
		self.speak('Oops, I didn\'t get that', expect_response=True)

	def send_order(self):
		try:
			data = {
				'orders': [{
					'menu_id': 1,
					'menu_title': 'Coffee',
					'quantity': 1
				}, {
					'menu_id': 2,
					'menu_title': 'Tea',
					'quantity': 1
				},
				]
			}
			response = requests.post('{}/api/qkr/submit/order/abc'.format(API_URL), json=data)
			result_str = response.text
			result = json.loads(result_str)

			self.speak('Thank you, your order is being prepared. \
				Payment will be done on your default card. Please authenticate on your mobile app to continue.')
		except:
			self.speak('Sorry, unable to send order at this time.')


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
	return AssistMcSkill()
