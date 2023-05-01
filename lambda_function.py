import logging
import ask_sdk_core.utils as ask_utils
import time
import smtplib
import ssl
from email.message import EmailMessage
import requests
import boto3
import os
import zipfile
import urllib.request
import requests

# from email import utils
# import win32com.client as win32

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.dialog import DelegateDirective
from ask_sdk_model.dialog import ElicitSlotDirective

import re
import random

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#to authenticate and access google API

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from datetime import datetime,timedelta

scope = ["https://www.googleapis.com/auth/calendar"]

dynamodb = boto3.client('dynamodb')         # initialization of dynamodb
table_name = 'sampleTable'

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
API_NAME = 'calendar'
API_VERSION ='v3'

service = build(API_NAME, API_VERSION, credentials=creds, static_discovery=False)           # to access google calendar API

calendar_id = "fcd31d4725c28aa79d693b969b104a248312b7404c1991ecc632611edf74b1b9@group.calendar.google.com"      #calender-id of the user/pro


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = "Schedule an appointment with professor"
        session_attr['source'] = "abc"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


        
# Rock, paper scissors Handler
class RPSIntentHandler(AbstractRequestHandler):
    """Handler for Game Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RPSIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # to extract inputs form the user 
        slots = handler_input.request_envelope.request.intent.slots
        slot_values = (list(slots.values())[0])
        
        print(slot_values.value)
        
        userAction = slot_values.value
        actions = ['rock','paper','scissor']
        
        
        speak_output=''
        reprompt_text = 'What is your next move?'

        if userAction is None:
            speak_output += "Welcome to play Rock Paper Scissors! "
            reprompt_text = 'What is your move?'
        else:
            alexaAction = random.choice(actions)
            combo = userAction + alexaAction

            if combo == 'rockrock':
                speak_output += "you played rock and i played rock, it is a tie! "
            elif combo == 'rockpaper':
                speak_output += "you played rock and i played paper, I win! "
            elif combo == 'rockscissor':
                speak_output += "you played rock and i played scissor, you win! congratulations "
            elif combo == 'paperrock':
                speak_output += "you played paper and i played rock, you win! congratulations "
            elif combo == 'paperpaper':
                speak_output += "you played paper and i played paper, it is a tie! "
            elif combo == 'paperscissor':
                speak_output += "you played paper and i played scissor, I win! "
            elif combo == 'scissorrock':
                speak_output += "you played scissor and i played rock, you win! congratulations "
            elif combo == 'scissorpaper':
                speak_output += "you played scissor and i played paper, I win! "
            elif combo == 'scissorscissor':
                speak_output += "you played scissor and i played scissor, it is a tie! "
            else:
                pass
        
        return handler_input.response_builder.speak(speak_output + reprompt_text).ask(reprompt_text).response
        


# Get Fortune Cookie Handler
class FortuneIntentHandler(AbstractRequestHandler):
    """Handler for Fortune Cookie Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("FortuneCookieIntent")(handler_input)

    def handle(self, handler_input):
            
        speak_output='Fortune Cookie Game!'

        url = "https://fortune-cookie2.p.rapidapi.com/fortune"
        
        headers = {
        	"X-RapidAPI-Key": "94faa779eamsh78bf96c25831d95p165f85jsn328c806f8370",
        	"X-RapidAPI-Host": "fortune-cookie2.p.rapidapi.com"
        }
        
        response = requests.request("GET", url, headers=headers)
        
        fortune = response.json()['answer']
        print(fortune)
        
        speak_output = f"Your fortune is: {fortune}"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



#Get lyrics of a song Handler
class SongLyricIntentHandler(AbstractRequestHandler):
    """Handler for Lyric Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("LyricsIntent")(handler_input)
        
    def handle(self, handler_input):
        speak_output = "Lyrics"
        
        slots = handler_input.request_envelope.request.intent.slots
        song = slots['song'].value

        url = "https://l-yrics.p.rapidapi.com/"
        
        querystring = {"song":song}
        
        headers = {
        	"X-RapidAPI-Key": "94faa779eamsh78bf96c25831d95p165f85jsn328c806f8370",
        	"X-RapidAPI-Host": "l-yrics.p.rapidapi.com"
        }
        
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
        
        # extract first 10 lyrics of a song         
        lyrics = response.json()['lyrics']
        lines = lyrics.split("\n")
        line = "\n".join(lines[:10])
        
        speak_output = f"{line}."
    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    


# Get quote from Avengers handler
class AvengersQuoteIntentHandler(AbstractRequestHandler):
    """Handler for Quote Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AvengersQuote")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
            
        url = "https://marvel-quote-api.p.rapidapi.com/"

        headers = {
        	"X-RapidAPI-Key": "94faa779eamsh78bf96c25831d95p165f85jsn328c806f8370",
        	"X-RapidAPI-Host": "marvel-quote-api.p.rapidapi.com"
        }
        
        response = requests.request("GET", url, headers=headers)
        
        print(response.text)

        
        quote = response.json()['Quote']
        cast = response.json()['Speaker']

        speak_output = f"Here's a quote from avengers by {cast}: {quote}"
    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



# Get translated word/sentence handler
class WordIntentHandler(AbstractRequestHandler):
    """Handler for Word Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("WordIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        slots = handler_input.request_envelope.request.intent.slots
        word = slots['word'].value

        languages = {"english": "en", "spanish": "es", "french": "fr", "german": "de", "italian": "it", "portuguese": "pt", "russian": "ru", "japanese": "ja", "korean": "ko", "chinese": "zh", "arabic": "ar", "swahili": "sw", "dutch": "nl", "turkish": "tr", "hindi": "hi", "urdu": "ur", "bengali": "bn", "indonesian": "id", "malay": "ms", "vietnamese": "vi"}

        lang = slots['lang'].value.lower()

        if lang in languages:
            lang_code = languages[lang]
        else:
            lang_code = "en"
            
        translated_word = self.lambda_handler(word, lang_code)
        
        speak_output = f"{translated_word}"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
    def lambda_handler(self, word, lang_code):
        url = "https://nlp-translation.p.rapidapi.com/v1/translate"
        
        querystring = {"text":word,"to":lang_code,"from":"en"}
        
        headers = {
            "X-RapidAPI-Key": "94faa779eamsh78bf96c25831d95p165f85jsn328c806f8370",
            "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"
        }
        
        response = requests.request("GET", url, headers=headers, params=querystring)
        
        print(response.text)
        translated_word = response.json()['translated_text'][lang_code]
        
        return translated_word





# Get top playlist of an artist handler
class PlaylistIntentHandler(AbstractRequestHandler):
    """Handler for Playlist Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("PlaylistIntent")(handler_input)
        
    
    def handle(self, handler_input):
        speak_output = "Playlist"
        
        slots = handler_input.request_envelope.request.intent.slots
        artist = slots['artist'].value

        url = "https://deezerdevs-deezer.p.rapidapi.com/search"
        
        querystring = {"q":artist}
        
        headers = {
        	"X-RapidAPI-Key": "94faa779eamsh78bf96c25831d95p165f85jsn328c806f8370",
        	"X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
        }
        
        response = requests.request("GET", url, headers=headers, params=querystring)
        
        # print(response.text)
                
        
        playlist = response.json()['data']
        titles = set(item["title"] for item in playlist if item["type"] == "track")
        unique_titles = list(titles)[:10]
        print(unique_titles)
        
        speak_output = "You might enjoy this playlist of popular songs: " + ",\n".join(unique_titles) + "."
    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )




# Get space news
class SpaceNewsIntentHandler(AbstractRequestHandler):
    """Handler for news Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NewsSpaceIntent")(handler_input)
        
    
    def handle(self, handler_input):

        url = "https://news-space.p.rapidapi.com/"
        
        headers = {
        	"X-RapidAPI-Key": "94faa779eamsh78bf96c25831d95p165f85jsn328c806f8370",
        	"X-RapidAPI-Host": "news-space.p.rapidapi.com"
        }
        
        response = requests.request("GET", url, headers=headers)
        
        print(response.text)
        news = response.json()
        new = set(item["title"] for item in news)
        titles = list(new)[:5]
        print(titles)
        speak_output = f"Here's the recent news," + ",\n".join(titles) 
    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )




# Weather Forecast of any city for any number of days
class WeatherIntentHandler(AbstractRequestHandler):
    """Handler for Forecast Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("WeatherForecast")(handler_input)
        
    
    def handle(self, handler_input):
        
        slots = handler_input.request_envelope.request.intent.slots
        city = slots['area'].value
        days = int(slots['day'].value)
        print(city,days)
        
        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
        
        querystring = {"q":city,"days":days}
        
        headers = {
        	"X-RapidAPI-Key": "94faa779eamsh78bf96c25831d95p165f85jsn328c806f8370",
        	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }
        
        response = requests.request("GET", url, headers=headers, params=querystring)
        
        print(response.text)
        
        location = response.json()['location']['name']
        condition = response.json()['current']['condition']['text']
        temp = response.json()['current']['temp_f']
        
        forecasts = response.json()['forecast']['forecastday']
        speak_output = f"Weather in {location} is {condition} and the forecast for the next {days} days is "
        
        for i in range(days):
            date = forecasts[i]['date']
            condition = forecasts[i]['day']['condition']['text']
            max_temp = forecasts[i]['day']['maxtemp_f']
            min_temp = forecasts[i]['day']['mintemp_f']
            speak_output += f"on {date}, the condition will be {condition} with a high of {max_temp} and a low of {min_temp} degrees. "
             
             
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        



# Get details of professor's expertise        
class ExpertiseIntentHandler(AbstractRequestHandler):
    """Handler for professor Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ExpertiseIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"Professor's area of expertise includes web programming, especially in Perl and Java, semi-structured query languages (Lorel and AUCQL), temporal query languages (TSQL2), and data cubes."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
 


# Get details of professor's achievements        
class AchievementIntentHandler(AbstractRequestHandler):
    """Handler for professor Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AchievementIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"In 2015, the professor was honored with the SIGMOD Contributions Award."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
    

# Get details of professor's education        
class ProfessorEducationIntentHandler(AbstractRequestHandler):
    """Handler for professor Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ProfessorEducation")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"Professor is a graduate of New College and obtained Ph.D. from the University of Arizona under the direction of Richard T. Snodgrass"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
   
    
    
# Get an overview of softwares developed by the professor        
class SoftwareOverviewIntentHandler(AbstractRequestHandler):
    """Handler for Software Overview Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SoftwareOverview")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Get the slot values from the request
        slots = handler_input.request_envelope.request.intent.slots
        print("role")
        print(slots)
        speak_output = ""
        
        softwareLen = 7
        keys_to_get = []
        
        # Construct the keys to fetch from DynamoDB
        for val in range(1, softwareLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'SoftwareOverview' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        software = dict()
        
        for element in items:
            software[element['key']['S']] = [element['value']['S']]
        
        print(software)
        
        # software = {'AUCQL':  ['A prototype semi structured DB. Written in (object-oriented) Perl, with extensive POD.'],
        #         'Incomplete Data Cube': ['A prototype incomplete data cube. Written in both Perl and Java. The code needs to be updated'],
        #         'Jumping Spider': ['A web spider and indexer. Written in Perl, with a fair bit of documentation'],
        #         'Educational software for the Web':['Quizzes, surveys, and self-assessments. These have been battle tested by the students at JCU and Bond for the last six years.'],
        #         'Fast Calendar I/O':['Timegm and gmtime, only faster, in C. These are probably faster, and are 64-bit friendly'],
        #         'MultiCal':  ['C code to add calendar and time support to databases. A C++ interface may now be available.'],
        #         'Indeterminacy' : ['C code for indeterminate timestamp support.']}


        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="software"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()

            true_tag = {}
            for key, value in software.items():
                true_tag[key] = False
                

            print('......',slot_values)
            speak_output = ""
            course = course.lower()
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            print(course_list)  
            
            # Search for matching details for each search term
            for course_value in course_list:
                flag = False
                print((course_value == "" or course_value == " "))
                if (course_value == "" or course_value == " "):
                    continue
                
                # Search for exact matches between the search term and keys
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in software.items() if (pattern.match(key))]
                print("matching")
                print(matching_keys)
                print(f"Keys in the material dictionary that match the search term '{course_value}':")
                for value, key in matching_keys:
                    print(true_tag)
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        speak_output += f"Here's an overview of {key} :{course_names[0]} " 
                        true_tag[key] = True
                        flag = True

                
                for key, value in software.items():
                    if not true_tag[key]:
                        print(value)
                        for val in value[-1]:
                            if (pattern.match(val)):
                                print(val)
                                speak_output += f"Here's an overview of {key}: {value[0]} "
                                true_tag[key] = True
                                flag = True
                                break
                
                if not flag and len(matching_keys) == 0 and course_value not in completed:
                    speak_output += f"No details found for {course_value}" 
                    completed.add(course_value)


    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  

# Get details of softwares developed by the professor        
class SoftwareIntentHandler(AbstractRequestHandler):
    """Handler for Software Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SoftwareIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"Softwares developed are AUCQL, Incomplete Data Cube, Jumping Spider, Educational software for the Web, Fast Calendar I/O, MultiCal and Indeterminacy"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    


# Get details of past teachings of the professor    
class TeachingIntentHandler(AbstractRequestHandler):
    """Handler for Teaching Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TeachingIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"Professor taught at James Cook University, Bond University, and Washington State University and a visiting assistant professor at Aalborg University!"


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# Get professor's department
class DepartmentIntentHandler(AbstractRequestHandler):
    """Handler for Department Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DepartmentIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"Professor belongs to the Department of Computer Science!"


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



# Get email id of the professor        
class EmailIntentHandler(AbstractRequestHandler):
    """Handler for Email Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("EmailIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"Email to contact the professor is curtis.dyreson@usu.edu!"


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )




# Get phone number of the professor        
class PhoneNumberIntentHandler(AbstractRequestHandler):
    """Handler for PhoneNumber Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("PhoneNumberIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"Phone number to contact the professor is (435) 797-0742!"


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



# Get contact details of professor
class ContactDetailsIntentHandler(AbstractRequestHandler):
    """Handler for professor Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ContactDetailsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"You can reach out to the professor through email or phone!"


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# Get professor's publications
class PublicationsIntentHandler(AbstractRequestHandler):
    """Handler for professor Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("PublicationsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"Publications of Curtis Dyreson can be found on DBLP ,Google Scholar, Semantic Scholar, ResearchGate and ACM Author pages"


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )




# Get previous projects 
class PreviousIntentHandler(AbstractRequestHandler):
    """Handler for professor Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("PreviousIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"The professor has worked on a variety of projects, including XML, incomplete information in databases, educational software for the web, and temporal databases, such as TTXPath, METAXPath, Incomplete Data Cubes, and TSQL2, among others. You can find more detailed information on his website!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# overview of projects
class OverviewIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("OverviewIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("role")
        print(slots)
        speak_output = ""
        
        projectLen = 4
        keys_to_get = []
        
        
        for val in range(1, projectLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'OverviewIntent' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        projects = dict()
        
        for element in items:
            projects[element['key']['S']] = [element['value']['S']]
        
        print(projects)

        # projects = {'XMorph':  ['an XML data transformation language'],
        #         'Virtual Hierarchies': ['combines XMorph with eXistdb, a native XML database engine'],
        #         'Aspect oriented data ': ['application of aspect-oriented techniques to databases to manage and query metadata'],
        #         'Data Sieve':['a data stream filter and data cube builder']}

        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="project"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()

            true_tag = {}
            for key, value in projects.items():
                true_tag[key] = False
                

            print('......',slot_values)
            speak_output = ""
            course = course.lower()
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            print(course_list)    
            for course_value in course_list:
                flag = False
                print((course_value == "" or course_value == " "))
                if (course_value == "" or course_value == " "):
                    continue
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in projects.items() if (pattern.match(key))]
                print("matching")
                print(matching_keys)
                print(f"Keys in the material dictionary that match the search term '{course_value}':")
                for value, key in matching_keys:
                    print(true_tag)
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        speak_output += f"{key} {course_names[0]} " 
                        true_tag[key] = True
                        flag = True

                
                for key, value in projects.items():
                    if not true_tag[key]:
                        print(value)
                        for val in value[-1]:
                            if (pattern.match(val)):
                                print(val)
                                speak_output += f"{key} {value[0]} "
                                true_tag[key] = True
                                flag = True
                                break
                
                if not flag and len(matching_keys) == 0 and course_value not in completed:
                    speak_output += f"No details found for {course_value}" 
                    completed.add(course_value)


    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  



# current projects of professor
class CurrentProjectIntentHandler(AbstractRequestHandler):
    """Handler for professor Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CurrentProjectIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"Professor's ongoing projects are XMorph, Virtual Hierarchies, Aspect-oriented data and Data Sieve!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



# professor details
class AboutProfessorIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AboutProfessorIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = f"Research interests include temporal databases, XML databases, data cubes, and providing support for proscriptive metadata!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



# About course mode of delivery
class ClassDeliveryIntentHandler(AbstractRequestHandler):
    """Handler for class Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ClassDeliveryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("role")
        print(slots)
        speak_output = ""
        
        classLen = 4
        keys_to_get = []
        
        for val in range(1, classLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'ClassDelivery' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        delivery = dict()
        
        for element in items:
            delivery[element['key']['S']] = [element['value']['S']]
        
        print(delivery)
        # delivery = {'introduction to database systems':  ['Will be delivered In-person, however, class recordings can be found on canvas',['databases','CS 5800','dbms']],
        #         'advanced databases': ['Will be delivered In-person, however, class recordings can be found on canvas',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['Will be delivered In-person, however, class recordings can be found on canvas',['CS 4700','pl']],
        #         'introduction to computer science':['Will be delivered In-person, however, class recordings can be found on canvas',['computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="class"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()
            true_tag = {}
            printed_courses = set()
            for key, value in delivery.items():
                true_tag[key] = False
            
            speak_output = ""
            course = course.lower()
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            
            for course_value in course_list:
                if course_value == "" or course_value == " ":
                    continue
            
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in delivery.items() if pattern.match(key)]
            
                for value, key in matching_keys:
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        course_name = course_names[0]
                        if course_name not in printed_courses:
                            speak_output += f"Course {course_name}"
                            printed_courses.add(course_name)
                        true_tag[key] = True
            
                for key, value in delivery.items():
                    if not true_tag[key]:
                        for val in value[-1]:
                            if pattern.match(val):
                                course_name = value[0]
                                if course_name not in printed_courses:
                                    speak_output += f"Course {course_name} "
                                    printed_courses.add(course_name)
                                true_tag[key] = True
                                break
            
                if not true_tag[key] and not matching_keys and course_value not in completed:
                    speak_output += f"No details found for {course_value}" 
                    completed.add(course_value)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  


# get roles of discussions of each course 
class RoleIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RoleIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("role")
        print(slots)
        speak_output = ""
        
        roleLen = 4
        keys_to_get = []
        
        
        for val in range(1, roleLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'Role' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        roles = dict()
        
        for element in items:
            roles[element['key']['S']] = [element['value']['S']]
        
        print(roles)
        

        # roles = {'introduction to database systems':  ['Designated Answers, Questioners and Note Takers',['databases','CS 5800','dbms']],
        #         'advanced databases': ['Designated Answers, Questioners and Note Takers ',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['Designated Answers, Questioners and Note Takers',['CS 4700','pl']],
        #         'computer science':['Designated Answers, Questioners and Note Takers',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if not course:
        # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="roles"))
                    .response)

        else:
            print(course)
            completed = set()
            true_tag = {}
            printed_courses = set()
            for key, value in roles.items():
                true_tag[key] = False
            
            speak_output = ""
            course = course.lower()
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            
            for course_value in course_list:
                if course_value == "" or course_value == " ":
                    continue
            
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in roles.items() if pattern.match(key)]
            
                for value, key in matching_keys:
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        course_name = course_names[0]
                        if course_name not in printed_courses:
                            speak_output += f"Roles are {course_name}"
                            printed_courses.add(course_name)
                        true_tag[key] = True
            
                for key, value in roles.items():
                    if not true_tag[key]:
                        for val in value[-1]:
                            if pattern.match(val):
                                course_name = value[0]
                                if course_name not in printed_courses:
                                    speak_output += f"Roles are {course_name} "
                                    printed_courses.add(course_name)
                                true_tag[key] = True
                                break
            
                if not true_tag[key] and not matching_keys and course_value not in completed:
                    speak_output += f"No details found for {course_value}" 
                    completed.add(course_value)


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  




# get course drop details
class SignatureIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SignatureIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        speak_output = ""
        
        
        signatureLen = 4
        keys_to_get = []
        
        
        for val in range(1, signatureLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'Signature' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        signature = dict()
        
        for element in items:
            signature[element['key']['S']] = [element['value']['S']]
        
        print(signature)

        # signature = {'introduction to database systems':  ['Students can drop courses within the first week but post that a signature is required from the instructor. ',['databases','CS 5800','dbms']],
        #         'advanced databases': ['Students can drop courses within the first week but post that a signature is required from the instructor. ',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['Students can drop courses within the first week but post that a signature is required from the instructor. ',['CS 4700','pl']],
        #         'computer science':['Students can drop courses within the first week but post that a signature is required from the instructor. ',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="signature"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()
            true_tag = {}
            printed_courses = set()
            for key, value in signature.items():
                true_tag[key] = False
            
            speak_output = ""
            course = course.lower()
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            
            for course_value in course_list:
                if course_value == "" or course_value == " ":
                    continue
            
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in signature.items() if pattern.match(key)]
            
                for value, key in matching_keys:
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        course_name = course_names[0]
                        if course_name not in printed_courses:
                            speak_output += f"{course_name}"
                            printed_courses.add(course_name)
                        true_tag[key] = True
            
                for key, value in signature.items():
                    if not true_tag[key]:
                        for val in value[-1]:
                            if pattern.match(val):
                                course_name = value[0]
                                if course_name not in printed_courses:
                                    speak_output += f"{course_name} "
                                    printed_courses.add(course_name)
                                true_tag[key] = True
                                break
            
                if not true_tag[key] and not matching_keys and course_value not in completed:
                    speak_output += f"No details found for {course_value}" 
                    completed.add(course_value)

    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  



# get course dropping criteria
class DropCourseIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DropCourseIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("drop")
        speak_output = ""

        
        dropLen = 4
        keys_to_get = []
        
        
        for val in range(1, dropLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'DropCourse' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        drop = dict()
        
        for element in items:
            drop[element['key']['S']] = [element['value']['S']]
        
        print(drop)
        
        

        # drop = {'introduction to database systems':  ['Instructors may drop students who do not attend the first week or second class meeting, students can drop courses within the first 20% without a notation, and dropping after that time results in a permanent W on the record',['databases','CS 5800','dbms']],
        #         'advanced databases': ['Instructors may drop students who do not attend the first week or second class meeting, students can drop courses within the first 20% without a notation, and dropping after that time results in a permanent W on the record',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['Instructors may drop students who do not attend the first week or second class meeting, students can drop courses within the first 20% without a notation, and dropping after that time results in a permanent W on the record',['CS 4700','pl']],
        #         'computer science':['Instructors may drop students who do not attend the first week or second class meeting, students can drop courses within the first 20% without a notation, and dropping after that time results in a permanent W on the record',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="drop"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()
            true_tag = {}
            printed_courses = set()
            for key, value in drop.items():
                true_tag[key] = False
            
            speak_output = ""
            course = course.lower()
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            
            for course_value in course_list:
                if course_value == "" or course_value == " ":
                    continue
            
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in drop.items() if pattern.match(key)]
            
                for value, key in matching_keys:
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        course_name = course_names[0]
                        if course_name not in printed_courses:
                            speak_output += f"{course_name}"
                            printed_courses.add(course_name)
                        true_tag[key] = True
            
                for key, value in drop.items():
                    if not true_tag[key]:
                        for val in value[-1]:
                            if pattern.match(val):
                                course_name = value[0]
                                if course_name not in printed_courses:
                                    speak_output += f"{course_name} "
                                    printed_courses.add(course_name)
                                true_tag[key] = True
                                break
            
                if not true_tag[key] and not matching_keys and course_value not in completed:
                    speak_output += f"No details found for {course_value}" 
                    completed.add(course_value)

    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  





# get information on grading policy
class GradingPolicyIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GradingPolicyIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("grading")
        speak_output = ""
        
        policyLen = 4
        keys_to_get = []
        
        
        for val in range(1, policyLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'GradingPolicy' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        policy = dict()
        
        for element in items:
            policy[element['key']['S']] = [element['value']['S']]
        
        print(policy)
        
        
        # policy = {'introduction to database systems':  ['Grades will be returned within a week of the due date, and students have one week to request a re-grading by submitting a detailed explanation to the professor via lecture or email.',['databases','CS 5800','dbms']],
        #         'advanced databases': ['Grades will be returned within a week of the due date, and students have one week to request a re-grading by submitting a detailed explanation to the professor via lecture or email.',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['Grades will be returned within a week of the due date, and students have one week to request a re-grading by submitting a detailed explanation to the professor via lecture or email.',['CS 4700','pl']],
        #         'computer science':['Grades will be returned within a week of the due date, and students have one week to request a re-grading by submitting a detailed explanation to the professor via lecture or email.',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="grade"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()
            true_tag = {}
            printed_courses = set()
            for key, value in policy.items():
                true_tag[key] = False
            
            speak_output = ""
            course = course.lower()
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            
            for course_value in course_list:
                if course_value == "" or course_value == " ":
                    continue
            
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in policy.items() if pattern.match(key)]
            
                for value, key in matching_keys:
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        course_name = course_names[0]
                        if course_name not in printed_courses:
                            speak_output += f"{course_name}"
                            printed_courses.add(course_name)
                        true_tag[key] = True
            
                for key, value in policy.items():
                    if not true_tag[key]:
                        for val in value[-1]:
                            if pattern.match(val):
                                course_name = value[0]
                                if course_name not in printed_courses:
                                    speak_output += f"{course_name} "
                                    printed_courses.add(course_name)
                                true_tag[key] = True
                                break
            
                if not true_tag[key] and not matching_keys and course_value not in completed:
                    speak_output += f"No details found for {course_value}" 
                    completed.add(course_value)


    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  
  
        


# Get grade allocation for each course
class GradeAlloctionIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GradeAlloctionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("grades")
        speak_output = ""
        
        
        gradeLen = 4
        keys_to_get = []
        
        
        for val in range(1, gradeLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'GradeAlloction' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        grade = dict()
        
        for element in items:
            grade[element['key']['S']] = [element['value']['S']]
        
        print(grade)
        
        # grade = {'introduction to database systems':  ['Homeworks 65%, Discussions 10% and Final Exam 25%',['databases','CS 5800','dbms']],
        #         'advanced databases': ['Homeworks 58%, Midterm 15% and Final Exam 27%',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['Homeworks 50%, Midterm 20%, Discussions 5% and Final Exam 25%',['CS 4700','pl']],
        #         'computer science':['Homeworks 50%, Midterm 45% and Discussions 5%',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="grade"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()

            true_tag = {}
            for key, value in grade.items():
                true_tag[key] = False
                

            print('......',slot_values)
            speak_output = ""
            course = course.lower()
            print('hjhj---',course)
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            print(course_list)    
            for course_value in course_list:
                flag = False
                print((course_value == "" or course_value == " "))
                if (course_value == "" or course_value == " "):
                    continue
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in grade.items() if (pattern.match(key))]
                print("matching")
                print(matching_keys)
                print(f"Keys in the material dictionary that match the search term '{course_value}':")
                for value, key in matching_keys:
                    print(true_tag)
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        speak_output += f"Here’s the breakdown of the grades for {key} {course_names[0]}. "
                        true_tag[key] = True
                        flag = True
                        
                
                for key, value in grade.items():
                    if not true_tag[key]:
                        print(value)
                        for val in value[-1]:
                            if (pattern.match(val)):
                                print(val)
                                speak_output += f"Here’s the breakdown of the grades for {key} {value[0]}. "
                                true_tag[key] = True
                                flag = True
                                break
                
                if not flag and len(matching_keys) == 0 and course_value not in completed:
                    speak_output += f"No details found for {course_value}." 
                    completed.add(course_value)


        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  


# get objectives of each course 
class CourseObjectiveIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CourseObjectiveIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("course")
        speak_output = ""
        
        courseLen = 4
        keys_to_get = []
        
        
        for val in range(1, courseLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'CourseObjective' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        objective = dict()
        
        for element in items:
            objective[element['key']['S']] = [element['value']['S']]
        
        print(objective)

        # objective = {'introduction to database systems':  ['enable students to develop a conceptual model of a database, gain familiarity with a database management system, and learn how to implement a database.',['databases','CS 5800','dbms']],
        #         'advanced databases': ['teach students new data querying and modeling techniques, while also introducing them to the evolving role of database technology.',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['teach the principles and components of programming language design, explore different paradigms like functional languages, use multiple programming languages, specify language syntax and semantics, and gain a basic understanding of language implementation and its impact on design.',['CS 4700','pl']],
        #         'computer science':['provide an introduction to Java programming and cover topics such as data types, conditional statements, loops, arrays, classes, inheritance, polymorphism, interfaces, exception handling, file operations, recursion, sorting algorithms, and data structures like linked lists, stacks, queues, and binary search trees.',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="objective"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()

            true_tag = {}
            for key, value in objective.items():
                true_tag[key] = False
                

            print('......',slot_values)
            speak_output = ""
            course = course.lower()
            print('hjhj---',course)
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            print(course_list)    
            for course_value in course_list:
                flag = False
                print((course_value == "" or course_value == " "))
                if (course_value == "" or course_value == " "):
                    continue
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in objective.items() if (pattern.match(key))]
                print("matching")
                print(matching_keys)
                print(f"Keys in the material dictionary that match the search term '{course_value}':")
                for value, key in matching_keys:
                    print(true_tag)
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        speak_output += f"This course aims to {course_names[0]}. "
                        true_tag[key] = True
                        flag = True
                        
                
                for key, value in objective.items():
                    if not true_tag[key]:
                        print(value)
                        for val in value[-1]:
                            if (pattern.match(val)):
                                print(val)
                                speak_output += f"This course aims to {value[0]}. "
                                true_tag[key] = True
                                flag = True
                                break
                
                if not flag and len(matching_keys) == 0 and course_value not in completed:
                    speak_output += f"No details found for {course_value}." 
                    completed.add(course_value)


    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  


# get course background details
class CourseBackgroundIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CourseBackgroundIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("background")
        speak_output = ""
        
        courseLen = 4
        keys_to_get = []
        
        
        for val in range(1, courseLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'CourseBackground' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        background = dict()
        
        for element in items:
            background[element['key']['S']] = [element['value']['S']]
        
        print(background)
        
        # background = {'introduction to database systems':  ['comparison of various database systems, normal forms, protection, concurrency, security and integrity, and distributed and object-oriented systems.',['databases','CS 5800','dbms']],
        #         'advanced databases': ['advanced study of non-relational data models,the internals of a database management system, and database frontiers.',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['theories of programming language design and implementation. Introduction to a variety of programming languages, showing how they represent trade-offs with respect to these theories.',['CS 4700','pl']],
        #         'computer science':['problem solving, programming, algorithm analysis, and data structures.',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="background"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()

            true_tag = {}
            for key, value in background.items():
                true_tag[key] = False
                

            print('......',slot_values)
            speak_output = ""
            course = course.lower()
            print('hjhj---',course)
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            print(course_list)    
            for course_value in course_list:
                flag = False
                print((course_value == "" or course_value == " "))
                if (course_value == "" or course_value == " "):
                    continue
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in background.items() if (pattern.match(key))]
                print("matching")
                print(matching_keys)
                print(f"Keys in the material dictionary that match the search term '{course_value}':")
                for value, key in matching_keys:
                    print(true_tag)
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        speak_output += f"This course {key} covers {course_names[0]}"
                        true_tag[key] = True
                        flag = True
                        
                
                for key, value in background.items():
                    if not true_tag[key]:
                        print(value)
                        for val in value[-1]:
                            if (pattern.match(val)):
                                print(val)
                                speak_output += f"This course covers {value[0]}"
                                true_tag[key] = True
                                flag = True
                                break
                
                if not flag and len(matching_keys) == 0 and course_value not in completed:
                    speak_output += f"No details found for {course_value}." 
                    completed.add(course_value)


    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  


# class discussion details
class DiscussionIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DiscussionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("discussion")
        speak_output = ""
        
        discussionLen = 4
        keys_to_get = []
        
        
        for val in range(1, discussionLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'Discussion' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        discussion = dict()
        
        for element in items:
            discussion[element['key']['S']] = [element['value']['S']]
        
        print(discussion)

        # discussion = {'introduction to database systems':  ['0%',['databases','CS 5800','dbms']],
        #         'advanced databases': ['10%',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['5%',['CS 4700','pl']],
        #         'computer science':['5%',['introduction to computer science','intro','CS 1410']]}

        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="discussion"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()

            true_tag = {}
            for key, value in discussion.items():
                true_tag[key] = False
                

            print('......',slot_values)
            speak_output = ""
            course = course.lower()
            print('hjhj---',course)
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            print(course_list)    
            for course_value in course_list:
                flag = False
                print((course_value == "" or course_value == " "))
                if (course_value == "" or course_value == " "):
                    continue
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in discussion.items() if (pattern.match(key))]
                print("matching")
                print(matching_keys)
                print(f"Keys in the material dictionary that match the search term '{course_value}':")
                for value, key in matching_keys:
                    print(true_tag)
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        speak_output += f"Discussion weightage for {key} towards final grade is {course_names[0]}. "
                        true_tag[key] = True
                        flag = True
                        
                
                for key, value in discussion.items():
                    if not true_tag[key]:
                        print(value)
                        for val in value[-1]:
                            if (pattern.match(val)):
                                print(val)
                                speak_output += f"Discussion weightage for {val} towards final grade is {value[0]}. "
                                true_tag[key] = True
                                flag = True
                                break
                
                if not flag and len(matching_keys) == 0 and course_value not in completed:
                    speak_output += f"None for {course_value}." 
                    completed.add(course_value)


    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  


# final exam details of each course 
class FinalExamIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("FinalExamIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("final")
        speak_output = ""
        
        finalLen = 4
        keys_to_get = []
        
        
        for val in range(1, finalLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'FinalExam' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        final = dict()
        
        for element in items:
            final[element['key']['S']] = [element['value']['S']]
        
        print(final)
        
        

        # final = {'introduction to database systems':  ['27%',['databases','CS 5800','dbms']],
        #         'advanced databases': ['25%',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['30%',['CS 4700','pl']],
        #         'computer science':['0%',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="final"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()

            true_tag = {}
            for key, value in final.items():
                true_tag[key] = False
                

            print('......',slot_values)
            speak_output = ""
            course = course.lower()
            print('hjhj---',course)
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            print(course_list)    
            for course_value in course_list:
                flag = False
                print((course_value == "" or course_value == " "))
                if (course_value == "" or course_value == " "):
                    continue
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in final.items() if (pattern.match(key))]
                print("matching")
                print(matching_keys)
                print(f"Keys in the material dictionary that match the search term '{course_value}':")
                for value, key in matching_keys:
                    print(true_tag)
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        speak_output += f"Final weightage for {key} towards final grade is {course_names[0]}. "
                        true_tag[key] = True
                        flag = True
                        
                
                for key, value in final.items():
                    if not true_tag[key]:
                        print(value)
                        for val in value[-1]:
                            if (pattern.match(val)):
                                print(val)
                                speak_output += f"Final weightage for {val} towards final grade is {value[0]}. "
                                true_tag[key] = True
                                flag = True
                                break
                
                if not flag and len(matching_keys) == 0 and course_value not in completed:
                    speak_output += f"None for {course_value}." 
                    completed.add(course_value)


    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  

# mid exam details of each course 
class MidIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MidIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("mid")
        speak_output = ""
        
        
        midLen = 4
        keys_to_get = []
        
        
        for val in range(1, midLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'MidIntent' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        midterm = dict()
        
        for element in items:
            midterm[element['key']['S']] = [element['value']['S']]
        
        print(midterm)
        # midterm = {'introduction to database systems':  ['15%',['databases','CS 5800','dbms']],
        #         'advanced databases': ['0%',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['20%',['CS 4700','pl']],
        #         'computer science':['45%',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="midterm"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()

            true_tag = {}
            for key, value in midterm.items():
                true_tag[key] = False
                

            print('......',slot_values)
            speak_output = ""
            course = course.lower()
            print('hjhj---',course)
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            print(course_list)    
            for course_value in course_list:
                flag = False
                print((course_value == "" or course_value == " "))
                if (course_value == "" or course_value == " "):
                    continue
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in midterm.items() if (pattern.match(key))]
                print("matching")
                print(matching_keys)
                print(f"Keys in the material dictionary that match the search term '{course_value}':")
                for value, key in matching_keys:
                    print(true_tag)
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        speak_output += f"Midterm weightage for {key} towards final grade is {course_names[0]}. "
                        true_tag[key] = True
                        flag = True
                        
                
                for key, value in midterm.items():
                    if not true_tag[key]:
                        print(value)
                        for val in value[-1]:
                            if (pattern.match(val)):
                                print(val)
                                speak_output += f"Midterm weightage for {val} towards final grade is {value[0]}. "
                                true_tag[key] = True
                                flag = True
                                break
                
                if not flag and len(matching_keys) == 0 and course_value not in completed:
                    speak_output += f"None for {course_value}." 
                    completed.add(course_value)


    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  



# get homework details of each course 
class HomeworkIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HomeworkIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("homework")
        speak_output = ""
        
        homeworkLen = 4
        keys_to_get = []
        
        for val in range(1, homeworkLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'Homework' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        homework = dict()
        
        for element in items:
            homework[element['key']['S']] = [element['value']['S']]
        
        print(homework)
        
        # homework = {'introduction to database systems':  ['58%',['databases','CS 5800','dbms']],
        #         'advanced databases': ['65%',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['50%',['CS 4700','pl']],
        #         'computer science':['50%',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="homework"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print(course)
            completed = set()

            true_tag = {}
            for key, value in homework.items():
                true_tag[key] = False
                

            print('......',slot_values)
            speak_output = ""
            course = course.lower()
            print('hjhj---',course)
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            print(course_list)    
            for course_value in course_list:
                flag = False
                print((course_value == "" or course_value == " "))
                if (course_value == "" or course_value == " "):
                    continue
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in homework.items() if (pattern.match(key))]
                print("matching")
                print(matching_keys)
                print(f"Keys in the material dictionary that match the search term '{course_value}':")
                for value, key in matching_keys:
                    print(true_tag)
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        speak_output += f"Homework weightage for {key} towards final grade is {course_names[0]}. "
                        true_tag[key] = True
                        flag = True
                        
                
                for key, value in homework.items():
                    if not true_tag[key]:
                        print(value)
                        for val in value[-1]:
                            if (pattern.match(val)):
                                print(val)
                                speak_output += f"Homework weightage for {val} towards final grade is {value[0]}. "
                                true_tag[key] = True
                                flag = True
                                break
                
                if not flag and len(matching_keys) == 0 and course_value not in completed:
                    speak_output += f"None for {course_value}." 
                    completed.add(course_value)


    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
  

# Location and timing details of each course 
class ClassPlaceIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ClassPlaceIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("PlaceIntent")
        speak_output = ""
        
        locationLen = 4
        keys_to_get = []
        
        
        for val in range(1, locationLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'ClassPlace' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        location = dict()
        
        for element in items:
            location[element['key']['S']] = [element['value']['S']]
        
        print(location)
        

        # location = {'introduction to database systems':  ['Tu-Th at 13:30-14:45 PM, Old Main 115',['databases','CS 5800','dbms']],
        #         'advanced databases': ['Tu-Th 9:00-10:15, Eccles Business Building 214',['advanced database systems','adb','CS 6800']],
        #         'programming languages': [' MWF 10:30-11:20 am, Family Life 105',['CS 4700','pl']],
        #         'computer science':['Tu-Th 10:30 - 11:45, Huntsman 315',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="location"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        
        if course.lower() not in location:
            speak_output = f"Sorry, I could not find any information for the course {course}. Please specify a valid course name."
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )
        
        
        
        print(course)
        completed = set()

        true_tag = {}
        for key, value in location.items():
            true_tag[key] = False
            

        print('......',slot_values)
        speak_output = ""
        course = course.lower()
        print('hjhj---',course)
        course = course.replace("and", '')
        course.replace("or", '')
        course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
        course_list = course.strip().split(' ')
        print(course_list)    
        for course_value in course_list:
            flag = False
            print((course_value == "" or course_value == " "))
            if (course_value == "" or course_value == " "):
                continue
            pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
            matching_keys = [(value, key) for key, value in location.items() if (pattern.match(key))]
            print("matching")
            print(matching_keys)
            print(f"Keys in the material dictionary that match the search term '{course_value}':")
            for value, key in matching_keys:
                print(true_tag)
                if not true_tag[key]:
                    course_names = " and ".join(value) if isinstance(value, str) else value
                    speak_output += f"Location and Timings for {key} are {course_names[0]}. "
                    true_tag[key] = True
                    flag = True
                    
            
            for key, value in location.items():
                if not true_tag[key]:
                    print(value)
                    for val in value[-1]:
                        if (pattern.match(val)):
                            print(val)
                            speak_output += f"Location and Timings for {val} are {value[0]}. "
                            true_tag[key] = True
                            flag = True
                            break
            
            if not flag and len(matching_keys) == 0 and course_value not in completed:
                speak_output += f"No information found for {course_value}. Please specify valid course name " 
                completed.add(course_value)



        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )




# get course materials 
class CourseMaterialIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CourseMaterialIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("material")
        speak_output = ""
        
        
        materialLen = 4
        keys_to_get = []
        
        
        for val in range(1, materialLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'CourseMaterial' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        material = dict()
        
        for element in items:
            material[element['key']['S']] = [element['value']['S']]
        
        print(material)    
        
        

        # material = {'introduction to database systems':  ['Canvas',['databases','CS 5800','dbms']],
        #         'advanced databases': ['Canvas',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['Canvas',['CS 4700','pl']],
        #         'computer science':['Canvas',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="material"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print('it is in book')
            completed = set()
            true_tag = {}
            printed_courses = set()
            for key, value in material.items():
                true_tag[key] = False
            
            speak_output = ""
            course = course.lower()
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            
            for course_value in course_list:
                if course_value == "" or course_value == " ":
                    continue
            
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in material.items() if pattern.match(key)]
            
                for value, key in matching_keys:
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        course_name = course_names[0]
                        if course_name not in printed_courses:
                            speak_output += f"You can access the course materials through {course_name}"
                            printed_courses.add(course_name)
                        true_tag[key] = True
            
                for key, value in material.items():
                    if not true_tag[key]:
                        for val in value[-1]:
                            if pattern.match(val):
                                course_name = value[0]
                                if course_name not in printed_courses:
                                    speak_output += f"You can access the course materials through {course_name} "
                                    printed_courses.add(course_name)
                                true_tag[key] = True
                                break
            
                if not true_tag[key] and not matching_keys and course_value not in completed:
                    speak_output += f"No details found for {course_value}" 
                    completed.add(course_value)

    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )





# prerequisites of each course
class RequirementIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RequirementIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        print("requirement")
        speak_output = ""
        
        
        preLen = 4
        keys_to_get = []
        
        
        for val in range(1, preLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'Requirement' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        prerequisite = dict()
        
        for element in items:
            prerequisite[element['key']['S']] = [element['value']['S']]
        
        print(prerequisite) 

        # prerequisite = {'introduction to database systems':  ['CS 2420 w/grade C-',['databases','CS 5800','dbms']],
        #         'advanced databases': ['CS 5800 B-',['advanced database systems','adb','CS 6800']],
        #         'programming languages': ['CS 2420 w/grade C-',['CS 4700','pl']],
        #         'computer science':['CS 1410 w/grade C-',['introduction to computer science','intro','CS 1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value

    
        if(not course):
                # check if the required slot has been filled
                speech_text = "What is your input for the My Slot?"
                reprompt_text = "Please provide your input for the My Slot."
                return  (handler_input.response_builder
                        .speak(speech_text)
                        .ask(reprompt_text)
                        .add_directive(ElicitSlotDirective(slot_to_elicit="subject"))
                        .response)
                        
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            print('it is in book')
            print(course)
            completed = set()

            true_tag = {}
            for key, value in prerequisite.items():
                true_tag[key] = False
                

            print('......',slot_values)
            speak_output = ""
            course = course.lower()
            print('hjhj---',course)
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            print(course_list)    
            for course_value in course_list:
                flag = False
                print((course_value == "" or course_value == " "))
                if (course_value == "" or course_value == " "):
                    continue
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in prerequisite.items() if (pattern.match(key))]
                print("matching")
                print(matching_keys)
                print(f"Keys in the prerequisite dictionary that match the search term '{course_value}':")
                for value, key in matching_keys:
                    print(true_tag)
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        speak_output += f"Prerequisites required for {key} are: {course_names[0]}. "
                        true_tag[key] = True
                        flag = True
                        
                
                for key, value in prerequisite.items():
                    if not true_tag[key]:
                        print(value)
                        for val in value[-1]:
                            if (pattern.match(val)):
                                print(val)
                                speak_output += f"Prerequisites required for {val} are: {value[0]}. "
                                true_tag[key] = True
                                flag = True
                                break
                
                if not flag and len(matching_keys) == 0 and course_value not in completed:
                    speak_output += f"None for {course_value}." 
                    completed.add(course_value)

    
    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )




# textbooks recommended for each course
class CourseTextIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CourseTextIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        speak_output = ""
        
        
        bookLen = 4
        keys_to_get = []
        
        
        for val in range(1, bookLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'CourseText' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        textbook = dict()
        
        for element in items:
            textbook[element['key']['S']] = [element['value']['S']]
        
        print(textbook) 
        

        # textbook = {'introduction to database systems':['Fundamentals of Database systems 7th edition by Ramez Elmasri',['databases','5800','dbms']],
        #             'advanced databases':['Database System Concepts,7th Edition by A. Silberschatz, H. Korth, S. Sudarshan',['advanced database systems','adb','6800']],
        #             'programming languages':['Programming Language Concepts, Third Edition by Carlo Ghezzi and Mehdi Jazayeri and Concepts of Programming Languages eBook 12e by Sebesta', ['4700','pl']],
        #             'computer science': ['Introduction to Java; Programming and Data Structures, Y. Daniel Liang',['introduction to computer science','intro','1410']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
            speech_text = "What is your input for the My Slot?"
            reprompt_text = "Please provide your input for the My Slot."
            return  (handler_input.response_builder
                    .speak(speech_text)
                    .ask(reprompt_text)
                    .add_directive(ElicitSlotDirective(slot_to_elicit="rec"))
                    .response)
                    
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            completed = set()
            true_tag = {}
            printed_courses = set()
            for key, value in textbook.items():
                true_tag[key] = False
            
            speak_output = ""
            course = course.lower()
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            
            for course_value in course_list:
                if course_value == "" or course_value == " ":
                    continue
            
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in textbook.items() if pattern.match(key)]
            
                for value, key in matching_keys:
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        course_name = course_names[0]
                        if course_name not in printed_courses:
                            speak_output += f"Recommended textbooks for {key} are {course_name}. "
                            printed_courses.add(course_name)
                        true_tag[key] = True
            
                for key, value in textbook.items():
                    if not true_tag[key]:
                        for val in value[-1]:
                            if pattern.match(val):
                                course_name = value[0]
                                if course_name not in printed_courses:
                                    speak_output += f"Recommended textbooks for {key} are {course_name}. "
                                    printed_courses.add(course_name)
                                true_tag[key] = True
                                break
            
                if not true_tag[key] and not matching_keys and course_value not in completed:
                    speak_output += f"No details found for {course_value}" 
                    completed.add(course_value)

    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )






# get courses being offered in each semester
class SemesterTermIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SemesterTermIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        speak_output = ""
        
        
        termLen = 4
        keys_to_get = []
        
        
        for val in range(1, termLen + 1):
            # Read the item from the table
            keys_to_get.append({'id': {'S': 'Semester' + str(val) }})
        
        # create a dictionary with the request parameters
        request_items = {
            table_name: {
                'Keys': keys_to_get
            }
        }
    
        # read the items from DynamoDB
        response = dynamodb.batch_get_item(RequestItems=request_items)
    
        # get the items data from the response
        items = response.get('Responses').get(table_name)
        
        term = dict()
        
        for element in items:
            term[element['key']['S']] = [element['value']['S']]
        
        print(term) 
        

        # term = {'spring':['CS 1410 Introduction to Computer Science, CS 6800 Advanced Database Systems',['spring semester']],
        #             'fall': ['CS 5800 Introduction to Database Systems, CS 4700 Programming Languages',['fall semester']],
        #             'winter': ['none',['winter semester']], 'summer': ['none',['summer semester']]}

        
        slot_values = (list(slots.values())[0])
        
        print(slot_values)
        course = slot_values.value
        
        if(not course):
                # check if the required slot has been filled
                speech_text = "What is your input for the My Slot?"
                reprompt_text = "Please provide your input for the My Slot."
                return  (handler_input.response_builder
                        .speak(speech_text)
                        .ask(reprompt_text)
                        .add_directive(ElicitSlotDirective(slot_to_elicit="semester"))
                        .response)
                        
                # speak_output += f"please re-enter the question again with the course name specified" 
        else:
            completed = set()

            true_tag = {}
            for key, value in term.items():
                true_tag[key] = False
                

            print('......',slot_values)
            speak_output = ""
            course = course.lower()
            course = course.replace("and", '')
            course.replace("or", '')
            course = re.sub(r"[^a-zA-Z0-9 ]", "", course)
            course_list = course.strip().split(' ')
            for course_value in course_list:
                flag = False
                print((course_value == "" or course_value == " "))
                if (course_value == "" or course_value == " "):
                    continue
                pattern = re.compile(f".*{course_value}.*", re.IGNORECASE)
                matching_keys = [(value, key) for key, value in term.items() if (pattern.match(key))]
                print("matching")
                print(matching_keys)
                print(f"Keys in the prerequisite dictionary that match the search term '{course_value}':")
                for value, key in matching_keys:
                    print(true_tag)
                    if not true_tag[key]:
                        course_names = " and ".join(value) if isinstance(value, str) else value
                        speak_output += f"Courses being taught by the professor for {key} are: {course_names[0]}. "
                        true_tag[key] = True
                        flag = True
                        
                
                for key, value in term.items():
                    if not true_tag[key]:
                        print(value)
                        for val in value[-1]:
                            if (pattern.match(val)):
                                print(val)
                                speak_output += f"Courses being taught by the professor for {val} are: {value[0]}. "
                                true_tag[key] = True
                                flag = True
                                break
                
                if not flag and len(matching_keys) == 0 and course_value not in completed:
                    speak_output += f"None offered for {course_value}." 
                    completed.add(course_value)

    
    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



# reserve an appointment with the professor
class SampleIntentHandler(AbstractRequestHandler):
    """Handler for Schedule Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SampleIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.request_envelope.request.intent.slots
        date = str(session_attr['date'].value)
        time = str(session_attr['time'].value)
        print(date)
        print(time)
        
        dateSlot = datetime.strptime(date, "%Y-%m-%d")
        hour = int(time.split(":")[0])
        mins = int(time.split(":")[1])
        time_min= datetime(dateSlot.year, dateSlot.month, dateSlot.day, hour, mins)
        time_max = time_min + timedelta (hours=1)
        print(time_min,time_max)
        reserve_appointment (time_min, time_max)
        
        
        speak_output = f"your appointment is scheduled on {date} at {time}"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        print(handler_input)
        print(handler_input.request_envelope.request.intent.slots)
        print(handler_input.request_envelope.request.intent)
        print(handler_input.request_envelope)
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SampleIntentHandler())
sb.add_request_handler(SemesterTermIntentHandler())
# sb.add_request_handler(ReferenceBooksIntentHandler())
sb.add_request_handler(RequirementIntentHandler())
sb.add_request_handler(CourseMaterialIntentHandler())
sb.add_request_handler(ClassPlaceIntentHandler())
sb.add_request_handler(HomeworkIntentHandler())
sb.add_request_handler(MidIntentHandler())
sb.add_request_handler(FinalExamIntentHandler())
sb.add_request_handler(DiscussionIntentHandler())
sb.add_request_handler(CourseBackgroundIntentHandler())
sb.add_request_handler(CourseObjectiveIntentHandler())
sb.add_request_handler(GradeAlloctionIntentHandler())
sb.add_request_handler(GradingPolicyIntentHandler())
sb.add_request_handler(DropCourseIntentHandler())
sb.add_request_handler(SignatureIntentHandler())
sb.add_request_handler(RoleIntentHandler())
sb.add_request_handler(ClassDeliveryIntentHandler())
sb.add_request_handler(AboutProfessorIntentHandler())
sb.add_request_handler(CurrentProjectIntentHandler())
sb.add_request_handler(RPSIntentHandler())
sb.add_request_handler(FortuneIntentHandler())
# sb.add_request_handler(SudokuIntentHandler())
sb.add_request_handler(SongLyricIntentHandler())
sb.add_request_handler(OverviewIntentHandler())
sb.add_request_handler(PreviousIntentHandler())
sb.add_request_handler(PublicationsIntentHandler())
sb.add_request_handler(ContactDetailsIntentHandler())
sb.add_request_handler(PhoneNumberIntentHandler())
sb.add_request_handler(EmailIntentHandler())
sb.add_request_handler(DepartmentIntentHandler())
sb.add_request_handler(TeachingIntentHandler())
sb.add_request_handler(SoftwareIntentHandler())
sb.add_request_handler(SoftwareOverviewIntentHandler())
sb.add_request_handler(ProfessorEducationIntentHandler())
sb.add_request_handler(AchievementIntentHandler())
sb.add_request_handler(ExpertiseIntentHandler())
sb.add_request_handler(CourseTextIntentHandler())
sb.add_request_handler(AvengersQuoteIntentHandler())
sb.add_request_handler(WordIntentHandler())
sb.add_request_handler(PlaylistIntentHandler())
sb.add_request_handler(SpaceNewsIntentHandler())
sb.add_request_handler(WeatherIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

def convert_to_RFC_datetime(a):
    nowdt = datetime.now()
    nowtuple = nowdt.timetuple()
    nowtimestamp = time.mktime(nowtuple)
    return utils.formatdate(nowtimestamp)
    
hour_adjustment = -8

# function to reserve appointment slot
def reserve_appointment (time_min, time_max):
    time_min = time_min + timedelta(hours=6)
    time_max = time_max + timedelta(hours=6)
    
    event = {
                'summary': 'test summary',
                'description': "description test",
                'start': {
                            'dateTime': time_min.strftime ("%Y-%m-%dT%H:%M:%S.000Z"),
                             'timeZone': 'America/Denver'
                         },
                'end': {
                            'dateTime': time_max.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                             'timeZone': 'America/Denver'
                        },
                "reminders": {
                    "useDefault": False,
                    'overrides': [
                                    {
                                        "method": 'popup', 
                                        'minutes': 30
                                    },
                                 ],
                }
          }
    
    print(event)
    # event_request_body = {
    #     'start': {
    #         'dateTime': '2023-03-09T17:06:02.000Z',
    #         'timeZone': 'America/Denver'
    #     },
    #     'end': {
    #         'dateTime': '2023-03-09T19:06:02.000Z',
    #         'timeZone': 'America/Denver'
    #     },
    #     'summary': 'Family Lunch',
    #     'description': 'Having lunch with the parents',
    #     'colorId': 5,
    #     'status': 'confirmed',
    #     'transparency': 'opaque',
    # }
    # print(event_request_body)
    print (service.events().insert(calendarId=calendar_id, body=event).execute())


    # Define email sender and receiver
    email_sender = 'alavalanithya@gmail.com'
    email_password = 'fcogdlflneldqxpk'
    email_receiver = 'anithya.niths@gmail.com'
    
    # Set the subject and body of the email
    subject = 'Appointment Reminder!'
    body = "Your appointment is scheduled on " + str(time_min - timedelta(hours=6))
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    
    # Add SSL (layer of security)
    context = ssl.create_default_context()
    
    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
