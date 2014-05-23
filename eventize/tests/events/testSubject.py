from .. import TestCase, Mock
from eventize.events import Subject
from eventize.descriptors import Handler


class SubjectTest(TestCase):
    descriptor_subject = Subject(Handler)

    def test_it_binds_subject_handlers_to_owner_class(self):

        class MockHandler(Handler):
            bind = Mock()

        class FakeSubject(object):
            handler = MockHandler()

        self.descriptor_subject(FakeSubject)

        MockHandler.bind.assert_called_once_with(FakeSubject)

    def test_it_add_parent_handlers_defaults(self):
        expected1 = lambda event: null
        expected2 = lambda event: null
        class SubjectParent(object):
            handler = Handler(expected1)

        class FakeSubject(SubjectParent):
            handler = Handler(expected2)

        self.descriptor_subject(FakeSubject)

        self.assertEqual([expected1, expected2], list(FakeSubject.handler))

    def test_when_subject_has_parent_it_keeps_its_type(self):
        class ChildHandler(Handler):
            pass
        class SubjectParent(object):
            handler = Handler()

        class FakeSubject(SubjectParent):
            handler = ChildHandler()

        self.descriptor_subject(FakeSubject)

        self.assertTrue(isinstance(FakeSubject.handler, ChildHandler))

    def test_it_can_be_used_as_a_decorator(self):
        expected1 = lambda event: null
        expected2 = lambda event: null

        @self.descriptor_subject
        class SubjectParent(object):
            handler = Handler(expected1)

        @self.descriptor_subject
        class FakeSubject(SubjectParent):
            handler = Handler(expected2)

        self.assertEqual([expected1, expected2], list(FakeSubject.handler))


    def test_it_inherits_from_all_its_parents(self):
        expected1 = lambda event: null
        expected2 = lambda event: null
        class SubjectParent1(object):
            handler = Handler(expected1)
        class SubjectParent2(object):
            handler = Handler(expected2)

        class FakeSubject(SubjectParent1, SubjectParent2):
            handler = Handler()

        self.descriptor_subject(FakeSubject)

        self.assertEqual([expected1, expected2], list(FakeSubject.handler))



