

class SocialNetworks:
	def __init__(self, user):
		self.user = user

	def facebook_user_id(self):
		return self.get_from_extra_data('facebook', 'id')

	def facebook_access_token(self):
		return self.get_from_extra_data('facebook', 'access_token')

	def facebook_username(self):
		facebook_username = None
		facebook_username = self.get_from_extra_data('facebook', 'username')

	 	if not facebook_username:
			facebook_username = self.get_from_extra_data('facebook', 'name')

		return facebook_username

	def twitter_username(self):
		twitter_username = None
		twitter_username = self.get_from_extra_data('twitter', 'screen_name')

		if twitter_username:
			twitter_username = '@' + twitter_username
    	
		return twitter_username

	def get_from_extra_data(self, provider, field_name):
		field = None

		try:
			provider_user = self.provider_user(provider)
			details = provider_user.extra_data

			field = details.get(field_name, None)       
		except UserSocialAuth.DoesNotExist:
		    provider_user = None

		return field

	def provider_user(self, provider):
		return self.user.social_auth.get(provider=provider)


