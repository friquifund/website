"""Doesnt work because I need a redirect URL that i cant seem to get"""
from nb_linkedin import linkedin

# Configure your LinkedIn API credentials
API_KEY = "86z9vctb2v1i02"
API_SECRET = "r1Vji1nRmMhii0Q9"
# Need to add redirect URL
RETURN_URL = "http://localhost:8000"

# Create a LinkedIn authentication object
authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())

# Get the authorization URL
authorization_url = authentication.authorization_url

print(authorization_url)
# Print the authorization URL and manually authorize your app

# Get the PIN code from the authorization process
pin_code = input("Enter the PIN code from the authorization process: ")

# Retrieve the access token
authentication.authorization_code = pin_code
access_token = authentication.get_access_token()

# Create a LinkedIn application object
application = linkedin.LinkedInApplication(token=access_token)

# Retrieve the profile information
profile = application.get_profile()

# Extract desired information from the profile
first_name = profile['firstName']
last_name = profile['lastName']
headline = profile['headline']

# Print the extracted information
print("First Name:", first_name)
print("Last Name:", last_name)
print("Headline:", headline)