from django.apps import AppConfig


class IncidentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'incidents'

    def ready(self):
    	import incidents.db_fetch
    	import incidents.db_insert
    	import incidents.security
        # import incidents.utils
