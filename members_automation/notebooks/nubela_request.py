import requests

#borja-e-98228088
api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/person/profile-picture'
api_key = 'rGpIpez2GrNYovK2J01xhQ'
header_dic = {'Authorization': 'Bearer ' + api_key}
params = {
    'linkedin_person_profile_url': 'https://www.linkedin.com/in/borja-e-98228088/',
}
response = requests.get(api_endpoint,
                        params=params,
                        headers=header_dic)

pic_url = response.json()["tmp_profile_pic_url"]

picture = requests.get(pic_url).content