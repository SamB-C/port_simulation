import unittest
from port import Container, InvalidSizeException, ContainerStack, ConatinerSizeConflict, ContainerStackTooTall, create_container, InvalidContainerSizeExpression, ContainerStackEmpty


class TestContainerFactory(unittest.TestCase):
    @unittest.expectedFailure
    def test_deafult_size_expressions(self):
        with self.assertRaises(Exception):
            create_container(None)

    @unittest.expectedFailure
    def test_short_size_expressions(self):
        with self.assertRaises(Exception):
            create_container(None, 'short')

    def test_contents(self):
        container = create_container(None)
        self.assertEqual(container.contents, None)

    def test_invalid_size_expression(self):
        with self.assertRaises(InvalidContainerSizeExpression):
            create_container(None, 'hi')

    def test_erroneous_size_expression(self):
        with self.assertRaises(TypeError):
            create_container(None, True)


class TestContainer(unittest.TestCase):

    @unittest.expectedFailure
    def test_size_two_point_five_nine(self):
        with self.assertRaises(InvalidSizeException):
            Container(2.59, None)

    def test_contents(self):
        with self.subTest():
            container = Container(2.59, 'lion')
            expected = 'lion'
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
            Container(6.06, None)

    def test_size_invalid(self):
        with self.assertRaises(InvalidSizeException):
            Container(1, None)

    def test_size_as_string(self):
        with self.assertRaises(TypeError):
            Container('1', None)

    def test_size_as_boolean(self):
        with self.assertRaises(TypeError):
            Container(True, None)

    @unittest.expectedFailure
    def test_size_as_int(self):
        with self.assertRaises(TypeError):
            Container(10, None)

    def test_get_is_short(self):
        container = Container(2.59, None)
        self.assertTrue(container.is_short)

    def test_get_is_short_false(self):
        container = Container(6.06, None)
        self.assertFalse(container.is_short)


class TestContainerStack(unittest.TestCase):

    @unittest.expectedFailure
    def test_size_two_point_five_nine(self):
        with self.assertRaises(InvalidSizeException):
            ContainerStack()

    @unittest.expectedFailure
    def test_size_six_point_zero_six(self):
        with self.assertRaises(InvalidSizeException):
            ContainerStack()

    def test_add_invalid_sized_container(self):
        with self.assertRaises(ConatinerSizeConflict):
            containerStack = ContainerStack()
            containerStack.add_conatiner(create_container(None, 'short'))
            container = Container(6.06, None)
            containerStack.add_conatiner(container)

    def test_add_valid_container(self):
        containerStack = ContainerStack()
        container = Container(2.59, None)
        containerStack.add_conatiner(container)
        self.assertListEqual(containerStack.layers, [[None], [container]])

    def test_add_too_many_containers(self):
        containerStack = ContainerStack(2)
        containerStack.add_conatiner(create_container(None))
        containerStack.add_conatiner(create_container(None))
        with self.assertRaises(ContainerStackTooTall):
            containerStack.add_conatiner(create_container(None))

    def test_add_2_short_1_long(self):
        container_stack = ContainerStack()
        short_containers = [create_container(None, 'short') for i in range(2)]
        for short_container in short_containers:
            container_stack.add_conatiner(short_container)
        long_container = create_container(None)
        container_stack.add_conatiner(long_container)
        self.assertListEqual(container_stack.layers, [
                             [None], short_containers, [long_container]])

    @unittest.skip('Feature not yet implemented')
    def test_remove_from_empty_stack(self):
        containerStack = ContainerStack()
        with self.assertRaises(ContainerStackEmpty):
            containerStack.remove_container()


unittest.main()
