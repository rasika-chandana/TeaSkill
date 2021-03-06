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

LOGGER = getLogger(__name__)

class AssistMcSkill(MycroftSkill):
	def __init__(self):
		super(AssistMcSkill, self).__init__(name="AssistMcSkill")

	def initialize(self):
		print '--- initialize AssistMcSkill ---'

	@intent_handler(IntentBuilder('OrderFoodIntent').require("AskFood"))
	@adds_context('OrderFoodContext')
	def handle_tea_intent(self, message):
		self.speak_dialog('order.food.confirm', expect_response=True)

	@intent_handler(IntentBuilder('YesOrderFoodIntent').require("YesKeyword").require('OrderFoodContext').build())
	@adds_context('RestaurantContext')
	def handle_yes_food_order_intent(self, message):
		self.speak_dialog('order.food.from.where', expect_response=True)

	@intent_handler(IntentBuilder('NoOrderFoodIntent').require("NoKeyword").require('OrderFoodContext').build())
	def handle_no_food_order_intent(self, message):
		self.speak_dialog('order.food.confirm.deny', expect_response=True)

	@intent_handler(IntentBuilder('OrderFromWhereIntent').require("Restaurants").require('RestaurantContext').build())
	@adds_context('MenuContext')
	def handle_restaurants_intent(self, message):
		self.speak_dialog('order.food.preference', expect_response=True)

	@intent_handler(IntentBuilder('MenuMoreIntent').require("Menu").require('MenuContext').build())
	@adds_context('MenuContextMore')
	def handle_order_item_intent(self, message):
		self.speak_dialog('order.food.preference.more', expect_response=True)

	@intent_handler(IntentBuilder('CheckoutIntent').require("Checkout").require('MenuContextMore').build())
	@adds_context('CheckoutContext')
	def handle_checkout_order_item_intent(self, message):
		self.remove_context('MenuContext')
		self.remove_context('MenuContextMore')
		self.speak_dialog('which.payment.method.to.use', expect_response=True)

	@intent_handler(IntentBuilder('PaymentMethodIntent').require("PaymentMethod").require('CheckoutContext').build())
	@removes_context('CheckoutContext')
	def handle_payment_method_intent(self, message):
		self.speak_dialog('collect.your.order.from.shop', expect_response=True)

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
