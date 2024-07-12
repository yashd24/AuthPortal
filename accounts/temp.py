from django.contrib.auth.tokens import default_token_generator

token = default_token_generator.make_token('user')
