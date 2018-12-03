import os
class Keys:
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    AWS_REGION = os.environ.get('AWS_REGION')
    consumer_key = os.environ.get('consumer_key')
    consumer_secret = os.environ.get('consumer_secret')
    access_token_key = os.environ.get('access_token_key')
    access_token_secret = os.environ.get('access_token_secret')