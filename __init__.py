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
from mycroft.util.log import getLogger
from mycroft.skills.context import adds_context, removes_context

API_URL = 'https://mcassist.herokuapp.com'

UNDO_CONTEXT = "OrderFoodContext"

LOGGER = getLogger(__name__)

class AssistMcSkill(MycroftSkill):
	def __init__(self):
		super(AssistMcSkill, self).__init__(name="AssistMcSkill")
		# Initialize working variables used within the skill.

	def initialize(self):
		print '--- initialize AssistMcSkill ---'

	@intent_handler(IntentBuilder('OrderFoodIntent').require("AskFood"))
    @adds_context('OrderFoodContext')
    def handle_tea_intent(self, message):
		self.speak_dialog('order.food.confirm.reply', expect_response=True)

	@intent_handler(IntentBuilder('YesOrderFoodIntent').require("YesKeyword").require('OrderFoodContext').build())
	def handle_yes_food_order_intent(self, message):
		self.speak('from where do you want to order', expect_response=True)

	@intent_handler(IntentBuilder('NoOrderFoodIntent').require("NoKeyword").require('OrderFoodContext').build())
	def handle_no_food_order_intent(self, message):
		self.speak('Ok, Tell me when you are hungry', expect_response=True)







	# @intent_handler(IntentBuilder('UnhandledTeaIntent').require('MilkContext').optionally("Unhandled").build())
	# def handle_tea_unhandled_intent(self, message):
	# 	self.speak('Oops, I didn\'t get that', expect_response=True)
    #
	# @intent_handler(IntentBuilder('NoMilkIntent').require("NoKeyword").require('MilkContext').build())
	# @adds_context('HoneyContext')
	# def handle_yes_milk_intent(self, message):
	# 	self.milk = True
	# 	self.speak('all right, any Honey?', expect_response=True)
    #
	# @intent_handler(IntentBuilder('YesMilkIntent').require("YesKeyword").require('MilkContext').build())
	# @adds_context('HoneyContext')
	# def handle_no_milk_intent(self, message):
	# 	self.speak('What about Honey?', expect_response=True)
    #
	# @intent_handler(IntentBuilder('NoHoneyIntent').require("NoKeyword").require('HoneyContext').build())
	# @removes_context('HoneyContext')
	# def handle_no_honey_intent(self, message):
	# 	self.send_order()
    #
	# @intent_handler(IntentBuilder('YesHoneyIntent').require("YesKeyword").require('HoneyContext').build())
	# @removes_context('HoneyContext')
	# def handle_yes_honey_intent(self, message):
	# 	self.send_order()
    #
	# @intent_handler(IntentBuilder('UnhandledTeaIntent').require('HoneyContext').optionally("Unhandled").build())
	# def handle_honey_unhandled_intent(self, message):
	# 	self.speak('Oops, I didn\'t get that', expect_response=True)
    #
	# def send_order(self):
	# 	try:
	# 		data = {
	# 			'orders': [{
	# 				'menu_id': 1,
	# 				'menu_title': 'Coffee',
	# 				'quantity': 1
	# 			}, {
	# 				'menu_id': 2,
	# 				'menu_title': 'Tea',
	# 				'quantity': 1
	# 			},
	# 			]
	# 		}
	# 		response = requests.post('{}/api/qkr/submit/order/abc'.format(API_URL), json=data)
	# 		result_str = response.text
	# 		result = json.loads(result_str)
    #
	# 		self.speak('Thank you, your order is being prepared. \
	# 			Payment will be done on your default card. Please authenticate on your mobile app to continue.')
	# 	except:
	# 		self.speak('Sorry, unable to send order at this time.')


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
	return AssistMcSkill()
