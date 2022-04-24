'''
Apps
'''

from django.apps import AppConfig


class UserConfig(AppConfig):
    ''' UserConfig '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
