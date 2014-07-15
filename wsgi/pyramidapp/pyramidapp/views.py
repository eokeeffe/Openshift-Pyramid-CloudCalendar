from pyramidapp.forms import *
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget, authenticated_userid
from pyramid.view import view_config
from pyramidapp.permissions import *
from sqlalchemy.exc import DBAPIError
from sqlalchemy import exc
import transaction,json

from pyramidapp.models import *
from pyramidapp.widgets import *

import tw2.core as twc
from datetime import date, datetime, timedelta

@view_config(route_name='home', renderer="pyramidapp:templates/index.mak")
def index_page(request):
    return {}

@view_config(route_name='search',
    renderer="pyramidapp:templates/search.mak")
def search(request):
    form = FindEvent(request.POST)
    username = authenticated_userid(request)

    if request.method == 'POST' and form.validate():
        user = User.by_name(username)
        events = Event.all()
        for event in events:
            if user.id == event.creator or user in event.users:
                if event.title == form.title.data:
                    request.session.flash(u'Title:\t%s'%(event.title))
                    request.session.flash(u'Description:\t%s'%(event.description))
                    request.session.flash(u'Start:\t%s'%(event.start))
                    request.session.flash(u'End:\t%s'%(event.end))
                    request.session.flash(u'AllDay:\t%s'%(event.allDay))
                    request.session.flash(u'URL:\t%s'%(event.url))
        return {'form':form, 'action':request.matchdict.get('action')}
    return {'form':form, 'action':request.matchdict.get('action')}

@view_config(route_name='remove')
def remove(request):
    title = request.POST.get('t', None)
    desc = request.POST.get('d', None)
    durl = request.POST.get('du', None)
    start = request.POST.get('s', None)
    end = request.POST.get('e', None)

    username = authenticated_userid(request)
    user = User.by_name(username)
    events = Event.all()
    found = False
    for e in events:
        if e.title == title and user.id == e.creator:
            with transaction.manager:
                DBSession.delete(e)
            found = True
    if found:
        request.session.flash(u'%s Event Removed'%title)
    else:
        request.session.flash(u'%s Event Does not Belong to You'%title)
    return HTTPFound(location=request.route_url('home'))

@view_config(route_name='edit_event',
    renderer="pyramidapp:templates/edit_event.mak")
def edit_event(request):
    id = int(request.matchdict.get('id', -1))
    username = authenticated_userid(request)
    user = User.by_name(username)
    event_id = None
    creator = 0
    if request.method == 'GET':
        #print 'Event ID:',id
        event = Event.by_id(id)
        event_id = event.id
        creator = event.creator
        if event.creator != user.id:
            request.session.flash(u'You do not have priviledges to edit %s'%event.title)
            return HTTPFound(location=request.route_url('home'))
        #print '--------------------------'
        #print "Event to be updated:",event
        #print '--------------------------'
        if not event:
            return HTTPNotFound()
    else:
        event = Event()
    form = EditEvent(request.POST, event)
    check = event

    if request.method == 'POST' and form.validate():
        #print '--------------'
        #print "POST"
        #print '--------------'
        form.populate_obj(event)
        old = Event.by_id(id)
        event.id = old.id
        event.users = old.users
        event.creator = old.creator
        del old
        # event.start = form.start.data
        # event.end = form.end.data
        # event.allDay = form.allDay.data
        # event.description = form.description.data
        # event.title = form.title.data

        #print "\nPre commit"
        with transaction.manager:
            DBSession.merge(event)
        #print "Commited\n"

        request.session.flash(u'%s Event Updated'%form.title.data)
        return HTTPFound(location=request.route_url('home'))
    else:
        #print '--------------'
        #print "GET"
        #print '--------------'
        return {'form':form, 
        'id': request.matchdict.get('id'),
        'action':request.matchdict.get('action')}

@view_config(route_name='edit')
def edit(request):
    key = request.POST['id']
    event = Event.by_id(int(key))
    #print "Found and Updating Event",event.id
    return HTTPFound(
        location=request.route_url('edit_event',id=key)
    )

@view_config(route_name='dates', renderer="json")
def dates(request):
    username = authenticated_userid(request)
    user = User.by_name(username)
    events = Event.all()
    cevents = []
    for event in events:
        #print '----------------------'
        #print event.title
        #print event.description
        #print event.start
        #print event.end
        #print event.allDay
        #print event.url
        #print '----------------------'
        if user.id == event.creator or user in event.users:
            #print 'allowed users'
            #for u in event.users:print u.name
            #print 'end users'
            e = {
                'title': event.title,
                'description' : event.description,
                'start': event.start.ctime(),
                'end': event.end.ctime(),
                'url' : event.url,
                'allDay': event.allDay,
                'id':event.id
            }
            cevents.append(e)
    return cevents

@view_config(route_name='blog', renderer="pyramidapp:templates/view_blog.mak")
def blog_view(request):
    id = int(request.matchdict.get('id', -1))
    entry = Entry.by_id(id)
    if not entry:
        return HTTPNotFound()
    return {'entry':entry}

@view_config(route_name='blog_action', match_param="action=create",
             renderer="pyramidapp:templates/edit_blog.mak",
             permission='create')
def blog_create(request):
    entry = Entry()
    form = BlogCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return {'form':form, 'action':request.matchdict.get('action')}

@view_config(route_name='register',
             renderer="pyramidapp:templates/create_user.mak")
def user_create(request):
    user = User()
    form = CreateUser(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(user)
        DBSession.add(user)
        request.session.flash(u'User account created')
        return HTTPFound(location=request.route_url('home'))
    return {'form':form, 'action':request.matchdict.get('action')}

@view_config(route_name='create_event',
             renderer="pyramidapp:templates/create_event.mak")
def create_event(request):
    event = Event()
    form = CreateEvent(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(event)

        username = authenticated_userid(request)
        user = User.by_name(username)

        dates = Event.getAll_user(user.id)
        users = []
        print '--------------'
        print '\tDate'
        for date in dates:  
            print date.title
            for u in date.users:
                if not u in users:
                    users.append(u)
        print '--------------'

        print '----------------'
        print user.name
        for p in users:
            print p
            print p.name
        print '----------------'

        title_exists = Event.by_start(form.title.data)
        start_exists = Event.by_start(form.start.data)

        if title_exists and start_exists:
            request.session.flash(u'Event exists already')
            return HTTPFound(location=request.route_url('home'))

        event.start = form.start.data
        event.end = form.end.data
        event.allDay = form.allDay.data
        event.creator  = user.id
        event.description = form.description.data

        with transaction.manager:
            DBSession.add(event)

        update_sharing(user,event,users)

        request.session.flash(u'%s Event created'%form.title.data)
        return HTTPFound(location=request.route_url('home'))
    return {'form':form, 'action':request.matchdict.get('action')}

def update_sharing(user,event,users):
    found_event = Event.getAll_user(user.id)
    print '***************'
    print '#Events',len(found_event)
    print '#Users',len(users)
    for fe in found_event:
        for user in users:
            try:
                if not user in fe.users:
                    fe.users.append(user)
            except:
                pass
    print '***************'


@view_config(route_name='sharing', renderer="pyramidapp:templates/sharing.mak")
def sharing_page(request):
    return {}

@view_config(route_name='share_calendar',
             renderer="pyramidapp:templates/share_calendar.mak")
def share_calendar(request):
    form = AllowUser(request.POST)
    username = authenticated_userid(request)
    sharing_user = User.by_name(username)

    if request.method == 'POST' and form.validate():
        dates = Event.getAll_user(sharing_user.id)
        user = User.by_name(form.name.data)
        for date in dates:
            if not (user in date.users):
                date.users.append(user)
        request.session.flash(u'%s shared calendar with %s'%(username,user.name))
        return HTTPFound(location=request.route_url('home'))
    return {'form':form, 'action':request.matchdict.get('action')}

@view_config(route_name='revoke_calendar',
             renderer="pyramidapp:templates/revoke_calendar.mak")
def revoke_calendar(request):
    form = RevokeUser(request.POST)
    username = authenticated_userid(request)
    sharing_user = User.by_name(username)

    if request.method == 'POST' and form.validate():
        dates = Event.getAll_user(sharing_user.id)
        user = User.by_name(form.name.data)
        for date in dates:
            if user in date.users:
                date.users.remove(user)
        request.session.flash(u'%s revoked calendar for %s'%(username,user.name))
        return HTTPFound(location=request.route_url('home'))
    return {'form':form, 'action':request.matchdict.get('action')}

@view_config(route_name='blog_action', match_param="action=edit",
             renderer="pyramidapp:templates/edit_blog.mak",
             permission='edit')
def blog_update(request):
    id = int(request.params.get('id', -1))
    entry = Entry.by_id(id)
    if not entry:
        return HTTPNotFound()
    form = BlogUpdateForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        return HTTPFound(location=request.route_url('blog', id=entry.id,
                                                    slug=entry.slug))
    return {'form':form, 'action':request.matchdict.get('action')}

@view_config(route_name='auth', match_param="action=in", renderer="string",
             request_method="POST")
@view_config(route_name='auth', match_param="action=out", renderer="string")
def sign_in_out(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username != None:
        user = User.by_name(username)
        if not user:
            request.session.flash(u'user does not exist')
        if user and user.verify_password(password):
            headers = remember(request, user.name)
        else:
            request.session.flash(u'User/Password not recognized')
            headers = forget(request)
    else:
        request.session.flash(u'Username is empty')
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)