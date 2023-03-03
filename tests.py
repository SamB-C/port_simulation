import unittest
from port import Container, InvalidSizeException, ContainerStack, ConatinerSizeConflict, ContainerStackTooTall, create_container, InvalidContainerSizeExpression, ContainerStackEmpty


class TestContainerFactory(unittest.TestCase):
    @unittest.expectedFailure
    def test_deafult_size_expressions(self):
        with self.assertRaises(Exception):
            create_container('')

    @unittest.expectedFailure
    def test_short_size_expressions(self):
        with self.assertRaises(Exception):
            create_container('', 'short')

    def test_contents(self):
        container = create_container('')
        self.assertEqual(container.contents, '')

    def test_invalid_size_expression(self):
        with self.assertRaises(InvalidContainerSizeExpression):
            create_container('', 'hi')

    def test_erroneous_size_expression(self):
        with self.assertRaises(TypeError):
            create_container('', True)


class TestContainer(unittest.TestCase):

    @unittest.expectedFailure
    def test_size_two_point_five_nine(self):
        with self.assertRaises(InvalidSizeException):
            Container(2.59, '')

    def test_contents(self):
        with self.subTest():
            container = Container(2.59, '')
            expected = ''
            actual = container.contents
            self.assertEqual(expected, actual)
        with self.subTest():
            container = Container(2.59, [1, 2, 3])
            expected = [1, 2, 3]
            actual = container.contents
            self.assertListEqual(expected, actual)

    @unittest.expectedFailure
    def test_size_six_point_zero_six(self):
        with self.assertRaises(InvalidSizeException):
            Container(6.06, '')

    def test_size_invalid(self):
        with self.assertRaises(InvalidSizeException):
            Container(1, '')

    def test_size_as_string(self):
        with self.assertRaises(TypeError):
            Container('1', '')

    def test_size_as_boolean(self):
        with self.assertRaises(TypeError):
            Container(True, '')

    @unittest.expectedFailure
    def test_size_as_int(self):
        with self.assertRaises(TypeError):
            Container(10, '')

    def test_get_is_short(self):
        container = create_container('', 'short')
        self.assertTrue(container.is_short)

    def test_get_is_short_false(self):
        container = create_container('')
        self.assertFalse(container.is_short)


class TestContainerStack(unittest.TestCase):

    @unittest.expectedFailure
    def test_size_two_point_five_nine(self):
        with self.assertRaises(InvalidSizeException):
            ContainerStack(2.59)

    @unittest.expectedFailure
    def test_size_six_point_zero_six(self):
        with self.assertRaises(InvalidSizeException):
            ContainerStack(6.06)

    def test_size_invalid(self):
        with self.assertRaises(InvalidSizeException):
            ContainerStack(1)

    def test_size_as_string(self):
        with self.assertRaises(TypeError):
            ContainerStack('1')

    def test_size_as_boolean(self):
        with self.assertRaises(TypeError):
            ContainerStack(True)

    @unittest.expectedFailure
    def test_size_as_int(self):
        with self.assertRaises(TypeError):
            ContainerStack(10)

    def test_add_invalid_sized_container(self):
        with self.assertRaises(ConatinerSizeConflict):
            containerStack = ContainerStack(2.59)
            container = Container(6.06, '')
            containerStack.add_conatiner(container)

    def test_add_valid_container(self):
        containerStack = ContainerStack(2.59)
        container = Container(2.59, '')
        containerStack.add_conatiner(container)
        self.assertListEqual(containerStack.containers, [None, container])

    def test_add_too_many_containers(self):
        containerStack = ContainerStack(2.59, 2)
        containerStack.add_conatiner(Container(2.59, ''))
        containerStack.add_conatiner(Container(2.59, ''))
        with self.assertRaises(ContainerStackTooTall):
            containerStack.add_conatiner(Container(2.59, ''))

    def test_remove_from_empty_stack(self):
        containerStack = ContainerStack(2.59)
        with self.assertRaises(ContainerStackEmpty):
            containerStack.remove_container()


unittest.main()
