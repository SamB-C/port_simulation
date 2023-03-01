from typing import Union
from dataclasses import dataclass


class InvalidSizeException(Exception):
    def __init__(self, invalidSize):
        message = f'{invalidSize}m is not a valid size for a shipping container'
        super().__init__(message)


class ConatinerSizeConflict(Exception):
    def __init__(self, incorrectSize: float, correctSize: float):
        message = f'{incorrectSize}m doesn\'t match the size {correctSize}m'
        super().__init__(message)


class ContainerStackTooTall(Exception):
    def __init__(self):
        super().__init__(
            'Container stack can\'t add any more containers as it is already at max height')


class InvalidContainerSizeExpression(Exception):
    def __init__(self, invalidExpression):
        super().__init__(
            f'{invalidExpression} is not a valid express to generate a container. Choose from [\'long\', \'short\']')


class ContainerStackEmpty(Exception):
    def __init__(self):
        super().__init__('Container cannot be removed as container stack is empty')


@dataclass
class ContainerSize:
    lengths = [2.59, 6.06]

    def __init__(self, length):
        if not isinstance(length, float) and (not isinstance(length, int) or isinstance(length, bool)):
            raise TypeError
        else:
            if length not in ContainerSize.lengths:
                raise InvalidSizeException(length)
        self.length: Union(float, int) = length


class Container:
    def __init__(self, length: float, contents: any):
        self.container_size: ContainerSize = ContainerSize(length)
        self.contents: any = contents

    def __repr__(self):
        return f'Container -> length: {self.container_size.length}, contents: {self.contents}'


def create_container(content, size='long'):
    if not isinstance(size, str):
        raise TypeError
    if size == 'long':
        return Container(ContainerSize.lengths[1], content)
    elif size == 'short':
        return Container(ContainerSize.lengths[0], content)
    else:
        raise InvalidContainerSizeExpression(size)


class ContainerStack:
    def __init__(self, length: float, max_height=10):
        self.top: Union(Container, None) = None
        self.container_size: ContainerSize = ContainerSize(length)
        self.containers = [None]
        self.max_height = max_height

    def add_conatiner(self, container: Container) -> None:
        if len(self.containers) == self.max_height + 1:
            raise ContainerStackTooTall()
        if container.container_size.length != self.container_size.length:
            raise ConatinerSizeConflict(
                container.container_size.length, self.container_size.length)
        self.containers.append(container)
        self.top = container

    def remove_container(self) -> Container:
        if self.top == None:
            raise ContainerStackEmpty()
        else:
            return self.containers.pop()
