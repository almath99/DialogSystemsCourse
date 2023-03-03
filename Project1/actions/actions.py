# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionConfirmMovieGenre(Action):

    def name(self) -> Text:
        return "action_confirm_movie_genre"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Retrieve movie genre entity
        movie_genre = tracker.get_slot("movie_genre")  
        
        # If movie_genre entity isn't filled
        if not movie_genre:
            dispatcher.utter_message(text='You did not tell me your preferred movie genre.')
        # Return preferred movie genre
        else:
            dispatcher.utter_message(text=f"Your preferred movie genre is {movie_genre}.")
        return []



import requests
import random
import string
from bs4 import BeautifulSoup
from typing import Union

class ActionMakeMovieRecommendation(Action):

    def name(self) -> Text:
        return "action_make_movie_recommendation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Retrieve movie genre entity
        movie_genre = tracker.get_slot("movie_genre")

        # Scrape movie recommendations for given genre from IMDb
        url = f"https://www.imdb.com/search/title/?title_type=feature&genres={movie_genre.lower()}&start=1&ref_=adv_nxt"
        response = requests.get(url)                          # Send an HTTP GET request to the IMDb website for a list of movies of the specified genre 
        soup = BeautifulSoup(response.text, 'html.parser')    # Use BeautifulSoup to parse the HTML response from the website
        movie_tags = soup.select(".lister-item-header a")     # Extract the movie title tags from the soup object
        movies = [movie.text for movie in movie_tags]         # Create a list of movie titles by iterating through the title tags and extracting their text

        # Filter only movie titles in English, to avoid bot's confusion by checking if each title is composed entirely of printable ASCII characters.
        english_titles = []
        for movie in movies:   
            if all(c in string.printable for c in movie):
                english_titles.append(movie)

        # Choose 5 random English movie titles
        recommendations = random.sample(english_titles, k=5)

        # Make movie recommendation
        if recommendations:
            recommendations_str = "\n- ".join(recommendations)
            dispatcher.utter_message(f"Here are 5 recommendations for {movie_genre} movies:\n- {recommendations_str}")
        else:
            dispatcher.utter_message("Sorry, I could not find any recommendations for that genre.")

        return []
    

class ActionRestart(Action):
  '''Triggers default action_restart action.'''
  
  def name(self) -> Text:
      return "action_restart"

  async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
  ) -> List[Dict[Text, Any]]:

      # custom behavior

      return [...]

