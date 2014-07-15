import os
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramidapp.security import EntryFactory
from pyramidapp.models import *

#Evan O'Keeffe

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    # OpenShift Database Connecction Settings
    if os.environ.get('OPENSHIFT_DB_URL'):
        settings['sqlalchemy.url'] = \
                '%(OPENSHIFT_DB_URL)s%(OPENSHIFT_APP_NAME)s' % os.environ
    #initialize the Database
    engine = engine_from_config(settings, 'sqlalchemy.')
    # connect to the Database
    initialize_sql(engine)

    authentication_policy = AuthTktAuthenticationPolicy('correcthorsestaplebattery')
    authorization_policy = ACLAuthorizationPolicy()
    my_session_factory = UnencryptedCookieSessionFactoryConfig('correcthorsestaplebattery')

    config = Configurator(settings=settings,
                session_factory = my_session_factory,
                authentication_policy=authentication_policy,
                authorization_policy=authorization_policy)

    #include other add-ons
    config.include('pyramid_mako')

    #inlcuding the css,javascript files
    config.add_static_view('static', 'pyramidapp:static', cache_max_age=3600)
    config.add_static_view('lib', 'pyramidapp:static/lib', cache_max_age=3600)
    config.add_static_view('datetimepicker', 'pyramidapp:static/datetimepicker', cache_max_age=3600)
    config.add_static_view('fullcalendar', 'pyramidapp:static/fullcalendar', cache_max_age=3600)
    #configuring the url paths
    config.add_route('home', '/')
    config.add_route('dates', '/dates')
    config.add_route('remove', '/remove')
    config.add_route('edit', '/edit')
    config.add_route('search', '/search')
    config.add_route('edit_event', '/edit_event/{id:\d+}')
    config.add_route('register','/register')
    # Share Routes
    config.add_route('sharing','/sharing')
    config.add_route('share_calendar','/share_calendar')
    config.add_route('revoke_calendar','/revoke_calendar')
    # Event Routes
    config.add_route('create_event','/addEvent')

    #used for authentication
    config.add_route('auth', '/sign/{action}')

    #no longer used when project is finished these will be removed
    config.add_route('blog', '/blog/{id:\d+}/{slug}')
    config.add_route('blog_action', '/blog/{action}',
                     factory='pyramidapp.security.EntryFactory')

    #scan for any extra pieces to be added
    config.scan()
    return config.make_wsgi_app()