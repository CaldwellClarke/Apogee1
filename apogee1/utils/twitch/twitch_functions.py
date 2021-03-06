import requests
from decouple import config
import json

def get_twitch_details(code, user_obj):
	try:
		twitch_client_id = config('TWITCH_CLIENT_ID')
		twitch_secret = config('TWITCH_SECRET')
		twitch_redirect_uri = config('TWITCH_REDIRECT_URI')
		headers = {
			'content-type': 'application/json',
			'Client-id': twitch_client_id
		}
		data = {
			"grant_type":"authorization_code",
			'client_id': twitch_client_id,
			"client_secret": twitch_secret,
			"code": code,
			"redirect_uri": twitch_redirect_uri
		}
		twitch_response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=json.dumps(data))
		twitch_dict=json.loads(twitch_response.text)
		context={}
		try:
			context['authenticated']=True
			twitch_oauth_token = twitch_dict['access_token']
			twitch_refresh_token = twitch_dict['refresh_token']
			auth_string = 'OAuth '
			auth_string+= twitch_oauth_token
			headers = {
				'Accept': 'application/vnd.twitchtv.v5+json',
				'Client-ID': twitch_client_id,
				'Authorization': auth_string,
			}
			response = requests.get('https://api.twitch.tv/kraken/user', headers=headers)
			twitch_dict2 = json.loads(response.text)
			print(twitch_dict2)
			twitch_id = twitch_dict2['_id']

			user_obj.profile.twitch_id = twitch_id
			user_obj.profile.twitch_refresh_token = twitch_refresh_token
			user_obj.profile.twitch_OAuth_token = twitch_oauth_token
			user_obj.profile.save(update_fields=['twitch_id'])
			user_obj.profile.save(update_fields=['twitch_refresh_token'])
			user_obj.profile.save(update_fields=['twitch_OAuth_token'])
			return 1
		except Exception as e:
			return 0
	except:
		#failure on authenticating code from twitch
		return -1


# def getOAuth(code, user_obj):
# 	print(1)
# 	headers = {
# 	    'content-type': 'application/json',
# 	    'Client-id': 'f054futox6ybt8p07bndbqbuaw0v48'
# 	}
# 	data = {"grant_type":"authorization_code",'client_id': 'f054futox6ybt8p07bndbqbuaw0v48',
# 	"client_secret": "anu2ub103e0or8had2cn1h3d6yxtld","code":
# 	code,"redirect_uri": "https://granite.gg/profiles/twitchauth/confirmation/"}
# 	twitch_response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=json.dumps(data))
# 	twitch_dict=json.loads(twitch_response.text)
# 	print(twitch_dict)
# 	return twitch_dict

# def getChannelInfo(OAuth):
# 	auth_string = 'OAuth '
# 	auth_string+= OAuth
# 	print(OAuth)
# 	headers = {
#         'Accept': 'application/vnd.twitchtv.v5+json',
#         'Client-ID': 'k6pbewo0iifuw2fu73rn9wz7k0beu1',
#         'Authorization': auth_string,
# 	}

# 	response = requests.get('https://api.twitch.tv/kraken/channel', headers=headers)
# 	return response

def is_twitch_sub(party_owner, party_joiner):
	print("Checking that ")
	print(party_joiner.username)
	print(party_joiner.profile.twitch_id)
	print("is subscribed to")
	print(party_owner.username)
	print(party_owner.profile.twitch_id)
	try:
		twitch_client_id = config('TWITCH_CLIENT_ID')
		twitch_secret = config('TWITCH_SECRET')
		twitch_redirect_uri = config('TWITCH_REDIRECT_URI')
		print(0)
		if party_owner.profile.twitch_id=="" or party_joiner.profile.twitch_id=="":
			return False
		print(1)
		auth_string = 'OAuth '
		auth_string+= party_owner.profile.twitch_OAuth_token
		headers = {'Accept': 'application/vnd.twitchtv.v5+json','Client-ID': twitch_client_id,'Authorization': auth_string,}
		new_url = 'https://api.twitch.tv/kraken/channels/'
		new_url+=party_owner.profile.twitch_id
		new_url+='/subscriptions/'
		new_url+=party_joiner.profile.twitch_id
		print(new_url)
		response = requests.get(new_url, headers=headers)
		twitch_dict=json.loads(response.text)
		print("TWITCH DICT IN TWITCH SUB")
		print(twitch_dict)
		has_sub = twitch_dict['sub_plan']
		if has_sub:
			print(2)
			return True
		else:
			print(3)
			return False
	except Exception as e:
		print(e)
		refresh_twitch_credentials(party_owner)
		print("EXCEPTION IN TWITCH SUB")
		return False



def refresh_twitch_credentials(user_obj):
	try:
		twitch_client_id = config('TWITCH_CLIENT_ID')
		twitch_secret = config('TWITCH_SECRET')
		twitch_redirect_uri = config('TWITCH_REDIRECT_URI')
		params = (('grant_type', 'refresh_token'), ('refresh_token', user_obj.profile.twitch_refresh_token), ('Client-id', twitch_client_id), ('client_secret', twitch_secret),)

		response = requests.post('https://id.twitch.tv/oauth2/token?client_id='+twitch_client_id, params=params)
		twitch_dict=json.loads(response.text)
		print(twitch_dict)
		user_obj.profile.twitch_refresh_token = twitch_dict['refresh_token']
		user_obj.profile.twitch_OAuth_token = twitch_dict['access_token']
		user_obj.profile.save(update_fields=['twitch_refresh_token'])
		user_obj.profile.save(update_fields=['twitch_OAuth_token'])
		return True
	except Exception as e:
		print("refresh")
		print(e)
		return False