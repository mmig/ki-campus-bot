import re
import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, Restarted, SlotSet, AllSlotsReset
from rasa_sdk.types import DomainDict

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

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
