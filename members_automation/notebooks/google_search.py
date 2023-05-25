from serpapi import GoogleSearch

profile_url = "https://www.linkedin.com/in/pauagullo/"


def get_current_role(profile_url, api_key):
  params = {
    "engine": "google", # serpapi parsing engine
    "q": profile_url, # search query
    "hl": "en", # language of the search
    "gl": "es", # country from where search initiated
    "api_key": api_key # your serpapi API key
  }

  search = GoogleSearch(params)
  results = search.get_dict()
  for result in results["organic_results"]:
    current_role = result["title"]
    result_link = result["link"]
    if result_link == profile_url:
      return current_role
  raise Exception(f"Profile not found for url {profile_url}")
