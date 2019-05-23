from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import *
# https://pypi.org/project/weather-api/
from weather import Weather, Unit

class ElicitCheckBalance(Action):
    def name(self):
        return 'elicit_check_balance'

    def run(self, dispatcher, tracker, domain):
        # Prepare the requirements string
        requirementString = "The system should allow the user to check account balance.\n"
        # Write to requirements.txt file
        file_name = "elicitedRequirements.txt"
        f = open(file_name, "a")
        f.write(requirementString)
        f.close()
        # Reply with affirmation
        response = "Check balance feature added."
        dispatcher.utter_message(response)
        return 

class ElicitOpenAccount(Action):
    def name(self):
        return 'elicit_open_account'

    def run(self, dispatcher, tracker, domain):
        
        # Extract the entities
        accountType = tracker.get_slot('ACCOUNT_TYPE')
        # Prepare the requirements string
        requirementString = "The system should allow the user to open " + accountType +" account.\n"
        # Write to requirements.txt file
        file_name = "elicitedRequirements.txt"
        f = open(file_name, "a")
        f.write(requirementString)
        f.close()
        # Reply with affirmation
        response = "Open Account feature noted."
        dispatcher.utter_message(response)
        return 

class ElicitSpeed(Action):
    def name(self):
        return 'elicit_speed'

    def run(self, dispatcher, tracker, domain):
        # Extract the entities
        load_time = tracker.get_slot('TIME')
        # Prepare the requirements string
        requirementString = "The system should be fast, and load within " +load_time+ ".\n"
        # Write to requirements.txt file
        file_name = "elicitedRequirements.txt"
        f = open(file_name, "a")
        f.write(requirementString)
        f.close()
        # Reply with affirmation
        response = "Load time feature noted."
        dispatcher.utter_message(response)
        return

class ElicitPortability(Action):
    def name(self):
        return 'elicit_portability'

    def run(self, dispatcher, tracker, domain):
        # Extract the entities
        platform_type = tracker.get_slot('PLATFORM_TYPE')
        # Prepare the requirements string
        requirementString = "The system should support " +platform_type+ ".\n"
        # Write to requirements.txt file
        file_name = "elicitedRequirements.txt"
        f = open(file_name, "a")
        f.write(requirementString)
        f.close()
        # Reply with affirmation
        response = "Portability feature noted."
        dispatcher.utter_message(response)
        return 
class ActionGetWeather(Action):
    def name(self):
        return 'action_get_weather'

    def run(self, dispatcher, tracker, domain):
        # weather = Weather(unit=Unit.CELSIUS)
        # gpe = ('Auckland', tracker.get_slot('GPE'))[bool(tracker.get_slot('GPE'))]
        # result = weather.lookup_by_location(gpe)
        # if result:
        #     condition = result.condition
        #     city = result.location.city
        #     country = result.location.country
        #     dispatcher.utter_message('It\'s ' + condition.text + ' and ' + condition.temp + '°C in ' +
        #                              city + ', ' + country + '.')
        # else:
        #     dispatcher.utter_message('We did not find any weather information for ' + gpe + '. Search by a city name.')
        #dispatcher.utter_message('Its quite hot')
        from apixu.client import ApixuClient
        api_key = '0191841c0d7a4a91b81115516191404'
        client = ApixuClient(api_key)

        loc = tracker.get_slot('GPE')
        current = client.current(q=loc)
        country = current['location']['country']
        city = current['location']['name']
        condition = current['current']['condition']['text']
        temperature_c = current['current']['temp_c']
        humidity = current['current']['humidity']
        wind_mph = current['current']['wind_mph']

        response = """It is currently {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)                        
        dispatcher.utter_message(response)
        return