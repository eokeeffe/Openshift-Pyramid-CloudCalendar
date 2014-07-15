import datetime
import sqlalchemy as sa
import transaction
from sqlalchemy import (
    Table,
    Column,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    DateTime,
    Boolean,
    ForeignKey,
    exc,
    event as e
)

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
)

from pyramid.security import authenticated_userid

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

permissions = Table('permissions',Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"),nullable=False),
    Column("event_id", Integer, ForeignKey("events.id"),nullable=False)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def by_name(cls, name):
        return DBSession.query(User).filter(User.name == name).first()

    @classmethod
    def by_id(cls, id):
        return DBSession.query(User).filter(User.id == id).first()
    
    def verify_password(self, password):
        return self.password == password

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    
    @classmethod
    def all(cls):
        return DBSession.query(Entry).order_by(sa.desc(Entry.created))
    
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Entry).filter(Entry.id == id).first()
    
    @property
    def slug(self):
        return urlify(self.title)
    
    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)
    
    @classmethod
    def get_paginator(cls, request, page=1):
        page_url = PageURL_WebOb(request)
        return Page(Entry.all(), page, url=page_url, items_per_page=5)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    # event details
    title = Column(Unicode(255), unique=False, nullable=False)
    description = Column(UnicodeText, default=u'')
    start = Column(DateTime, nullable=False)
    end = Column(DateTime)
    allDay = Column(Boolean)
    url = Column(UnicodeText, default=u'')
    # who can view the event
    creator = Column(Integer, ForeignKey('users.id'), nullable=False)
    # event object details
    users = relationship("User",
                    secondary=permissions,
                    backref="events")
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    
    @classmethod
    def all(cls):
        return DBSession.query(Event).filter().all()

    @classmethod
    def by_id(cls, id):
        return DBSession.query(Event).filter(Event.id == id).first()

    @classmethod
    def by_creator(cls, creator):
        return DBSession.query(Event).filter(Event.creator == creator).first()

    @classmethod
    def latest(cls, creator):
        return DBSession.query(Event).group_by(Event.edited).all()

    @classmethod
    def by_title(cls, title):
        return DBSession.query(Event).filter(Event.title == title).first()

    @classmethod
    def getAll_user(cls, creator):
        return DBSession.query(Event).filter(Event.creator == creator).all()

    @classmethod
    def by_start(cls, start):
        return DBSession.query(Event).filter(Event.start == start).first()

    @classmethod
    def by_end(cls, date):
        return DBSession.query(Event).filter(Event.end == end).first()

    @classmethod
    def has_permission(self, user_id):
        '''Check out whether a user has a permission or not.'''
        permission = Event.query.filter_by(by_creator=user_id).first()
        # if the permission does not exist or was not given to the user
        if not permission or not permission in self.users:
            return False
        return True

    @classmethod
    def grant_permission(self, user_id):
        '''Grant a permission to a user.'''
        permission = User.query.filter_by(user_id=user_id).first()
        if permission and permission in self.users:
            return
        if not permission:
            permission = Permission()
            permission.name = name
            db.session.add(permission)
            db.session.commit()
        self.users.append(permission)

    @classmethod
    def revoke_permission(self, name):
        '''Revoke a given permission for a user.'''
        permission = User.query.filter_by(name=name).first()
        if not permission or not permission in self.users:
            return
        self.users.remove(permission)

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    #Base.metadata.drop_all()#clear the database
    Base.metadata.create_all(engine)#create the tables
    admin = User(name=u'admin', password=u'admin')
    try:
        with transaction.manager:
            DBSession.add(admin)
            print 'Admin Created'
    except exc.SQLAlchemyError:
        print 'Admin couldnt be created'
    except exc.IntegrityError:
        print 'Admin exists'