from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted
from sanic.request import Request
from rasa_sdk.executor import CollectingDispatcher

import requests
import json

# dfki test
import random

from rasa_sdk import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, Restarted, AllSlotsReset
from rasa_sdk.types import DomainDict
####

class CourseSet(Action):
	def name(self):
		return "action_course_set"

	def run(self, dispatcher, tracker, domain):
		currentCourse = tracker.get_slot('current_course_title')
		if currentCourse:
			return [SlotSet('course-set', True)]
		else:
			return [SlotSet('course-set', False)]

class PrintAllSlots(Action):
	def name(self):
		return "action_all_slots"

	def run(self, dispatcher, tracker, domain):
		currentCourse = tracker.get_slot('current_course_title')
		return []

class SetCurrentCourse(Action):
	def name(self):
		return "action_set_current_course"

	def run(self, dispatcher, tracker, domain):
		currentCourse = tracker.latest_message['text']
		return [SlotSet('current_course_title', currentCourse)]


class ActionGetCourses(Action):
	def name(self) -> Text:
		return "action_get_courses_buttons"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		current_state = tracker.current_state()
		token = current_state['sender_id']
		r = requests.get('https://learn.ki-campus.org/bridges/chatbot/my_courses',
		headers={
			"content-type": "application/json",
			"Authorization": 'Bearer {0}'.format(token)
		})
		status = r.status_code
		if status == 200:
			response = json.loads(r.content)
			if len(response) < 1:
				dispatcher.utter_message('Du bist derzeit in keinem Kursen eingeschrieben.')
				return [SlotSet('courses_available', False)]
			else:
				dispatcher.utter_message('Du bist derzeit in diesen Kursen eingeschrieben:')
				buttonGroup = []
				for course in response:
					title = course['title']
					buttonGroup.append({"title": title, "payload": '{0}'.format(title)})
				dispatcher.utter_message(buttons = buttonGroup)
				return [SlotSet('all_courses', response), SlotSet('courses_available', True)]
		elif status == 401: # Status-Code 401 None
			dispatcher.utter_message('Du bist derzeit in keinem Kursen eingeschrieben.')
			return [SlotSet('courses_available', False)]
		else:
			return []

class ActionGetCourses(Action):
	def name(self) -> Text:
		return "action_get_courses"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		current_state = tracker.current_state()
		token = current_state['sender_id']
		r = requests.get('https://learn.ki-campus.org/bridges/chatbot/my_courses',
		headers={
			"content-type": "application/json",
			"Authorization": 'Bearer {0}'.format(token)
		})
		status = r.status_code
		if status == 200:
			response = json.loads(r.content)
			if len(response) < 1:
				dispatcher.utter_message('Du bist derzeit in keinem Kursen eingeschrieben.')
				return [SlotSet('courses_available', False)]
			else:
				dispatcher.utter_message('Du bist derzeit in diesen Kursen eingeschrieben:')
				for course in response:
					title = course['title']
					dispatcher.utter_message(title)
				return [SlotSet('all_courses', response), SlotSet('courses_available', True)]
		elif status == 401: # Status-Code 401 None
			dispatcher.utter_message('Du bist derzeit in keinem Kursen eingeschrieben.')
			return [SlotSet('courses_available', False)]
		else:
			return []

class ActionGetAchievements(Action):
	def name(self) -> Text:
		return "action_get_achievements"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		course_achieved = False
		currentCourse = []
		courseId = 0
		currentAchievements = []
		current_state = tracker.current_state()
		token = current_state['sender_id']
		currentCourseTitle = tracker.slots['current_course_title']
		allCourses = tracker.slots['all_courses']
		for course in allCourses:
			if currentCourseTitle in course['title']:
				courseId = course['id']
				currentCourse = course
				break
		if courseId != 0:	
			r = requests.get('https://learn.ki-campus.org/bridges/chatbot/my_courses/{0}/achievements'.format(courseId), 
			headers={
				"content-type": "application/json",
				"Authorization": 'Bearer {0}'.format(token), 
				"Accept-Language": "de"
			})
			status = r.status_code
			if status == 200:
				response = json.loads(r.content)
				currentAchievements = response['certificates']
				for achievement in currentAchievements:
					dispatcher.utter_message('{0}'.format(achievement['description']))
					if achievement['achieved'] and not course_achieved:
						course_achieved = True
			return[SlotSet('current_course_achieved', course_achieved), SlotSet('current_course', currentCourse), SlotSet('current_achievements', currentAchievements)]
		else:
			dispatcher.utter_message('Es tut mir sehr leid! Ich konnte den Kurs, den du suchst, nicht finden. Bitte versuche es erneut, indem du mir den Kurstitel nennen.')
			return[SlotSet('current_course_achieved', course_achieved), SlotSet('current_course', currentCourse), SlotSet('current_achievements', currentAchievements)]


class ActionGetCertificate(Action):
	def name(self) -> Text:
		return "action_download_certificate"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		currentAchievements = tracker.slots['current_achievements']
		for achievement in currentAchievements:
			if achievement['achieved']:
				if achievement['download']['available']:
					dispatcher.utter_message('Hier kannst du {0}: {1} herunterladen!'.format(achievement['name'], achievement['download']['url']))
				else:
					dispatcher.utter_message('Es tut mir sehr leid! Das {0} ist nicht mehr verfügbar und kann leider nicht mehr heruntergeladen werden!'.format(achievement['name']))
		return []

############# DFKI ###############

# ALLOWED_LANGUAGES = ['deutsch', 'englisch']
# ALLOWED_TOPICS = ['ki-einführung', 'ki-vertiefung', 'ki-berufsfelder', 'ki-gesellschaft', 'data science', 'maschinelles lernen', 'egal']

class ActionFetchProfile(Action):
    
    def name(self) -> Text:
        return "action_fetch_profile"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        AllSlotsReset()
            
        if random.randint(0,9) > 4: user_id = "22218451-41f0-23dd-c50f-cdd8096610c1"
        else: return [SlotSet("user_id", None), SlotSet("enrollments", []), SlotSet("course_visits", []), SlotSet("search_terms", []), dispatcher.utter_message(text="User ist nicht eingeloggt.")]
        # if re.search(".*", user_id): SlotSet("user_id", user_id) # create regex
        # else: return [SlotSet("user_id", None), dispatcher.utter_message("User ist nicht eingeloggt.")]

        enrollments = ["Einführung in die KI", "Mensch-Maschine-Interaktion"]
        # if not enrollments: SlotSet("enrollments", None)
        # else: SlotSet("enrollments", enrollments)

        course_visits = ["Big Data Analytics"]
        # if not course_visits: SlotSet("course_visits", None)
        # else: SlotSet("course_visits", course_visits)

        search_terms = ["KI", "Machine Learning"]
        # if not search_terms: SlotSet("search_terms", None)
        # else: SlotSet("search_terms", search_terms)

        dispatcher.utter_message(text="action ausgeführt")
        return [SlotSet("user_id", user_id), SlotSet("enrollments", enrollments), SlotSet("course_visits", course_visits), SlotSet("search_terms", search_terms)]

class ActionRestart(Action):

    def name(self) -> Text:
            return "action_restart"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # custom behavior
        dispatcher.utter_message(response="utter_restart")

        return [Restarted()]

class ActionGetLearningRecommendation(Action):

    def name(self) -> Text:
        return "action_get_learning_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        language = str(tracker.get_slot("language"))
        topic = str(tracker.get_slot("topic"))
        level = str(tracker.get_slot("level"))
        max_duration = int(tracker.get_slot("max_duration")) 
        certificate = int(tracker.get_slot("certificate"))
        enrollments = tracker.get_slot("enrollments")
        course_visits = tracker.get_slot("course_visits")
        search_terms = tracker.get_slot("search_terms")
        
        return []

# class ValidateCourseSearchForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_coursesearch_form"

#     def validate_language(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         """Validate `language` value."""

#         if slot_value.lower() not in ALLOWED_LANGUAGES:
#             dispatcher.utter_message(text=f"Momentan bieten wir nur Kurse in den Sprachen Deutsch und Englisch an!")
#             return {"language": None}
#         dispatcher.utter_message()
#         return {"language": slot_value.lower()}

#     def validate_topic(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         """Validate `topic` value."""

#         if slot_value not in ALLOWED_TOPICS:
#             dispatcher.utter_message(text=f"Wir bieten zu diesem Themenfeld keine Kurse an! Bitte wähle eins der aufgelisteten Themen.")
#             return {"topic": None}
#         dispatcher.utter_message()
#         return {"topic": slot_value.lower()}
