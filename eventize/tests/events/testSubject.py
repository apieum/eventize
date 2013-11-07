from .. import TestCase, Mock
from eventize.events.subject import Subject
from eventize.events.handler import DescriptorHandler


class SubjectTest(TestCase):
    def test_it_binds_subject_handlers_to_owner_class(self):

        class MockHandler(DescriptorHandler):
            bind = Mock()

        class FakeSubject(object):
            handler = MockHandler()

        Subject(FakeSubject)

        MockHandler.bind.assert_called_once_with(FakeSubject)

    def test_it_add_parent_handlers_defaults(self):
        expected1 = Mock()
        expected2 = Mock()
        class SubjectParent(object):
            handler = DescriptorHandler(expected1)

        class FakeSubject(SubjectParent):
            handler = DescriptorHandler(expected2)

        Subject(FakeSubject)

        self.assertEqual([expected1, expected2], list(FakeSubject.handler))

    def test_when_subject_has_parents_it_keeps_its_type(self):
        class ChildHandler(DescriptorHandler):
            pass
        class SubjectParent(object):
            handler = DescriptorHandler()

        class FakeSubject(SubjectParent):
            handler = ChildHandler()

        Subject(FakeSubject)

        self.assertTrue(isinstance(FakeSubject.handler, ChildHandler))

    def test_it_can_be_used_as_a_decorator(self):
        expected1 = Mock()
        expected2 = Mock()

        @Subject
        class SubjectParent(object):
            handler = DescriptorHandler(expected1)

        @Subject
        class FakeSubject(SubjectParent):
            handler = DescriptorHandler(expected2)

        self.assertEqual([expected1, expected2], list(FakeSubject.handler))



