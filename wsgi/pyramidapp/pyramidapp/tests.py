import unittest
import transaction

from pyramid import testing

from pyramidapp.models import DBSession

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from pyramidapp.models import (
            Base,
            User,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            admin = User(name=u'admin', password=u'admin')
            DBSession.add(admin)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from pyramidapp.views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'pyramid_blogr')