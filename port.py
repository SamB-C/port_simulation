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


class Crane:
    """Base class for all cranes - to do with coupling and decoupling"""
    pass


class AutomaticStackingCrane(Crane):
    """Moving crane that moves containers that are currently being unloaded or loaded onto the ContainerShip"""
    pass


class AutomaticStackingCraneManagementMatrix:
    """The area of stacks looked after by 2 AutomaticStackingCranes"""
    pass


class Cassettes:
    """Hold containers whilst they are being moved by TransLifters"""
    pass


class TrainLoadingCrane(Crane):
    """Load and unload FrieghtTrains"""
    pass


class TransLifters:
    """Just move cassettes"""
    pass


class StraddleCarriers:
    """Move containers between AutomaticStackingCraneManagementMatrix and BoatLoadingCrane"""
    pass


class BoatLoadingCrane(Crane):
    """Load and unload ships"""
    pass


class FreightTrain:
    """Moves containers in and out of the port"""
    pass


class RailwayTerminals:
    """Where FreightTrains stay to be loaded"""
    pass


class Berth:
    """Where ContainerShips dock to be loaded"""
    pass


class ConatainerShip:
    """Ships that transport continers"""
    pass


class Tugboats:
    """2 tugboats are required to be free for a ship to dock"""


"""
specific stacks for temperature controlled cargo

some containers come by rail - moved by translifters on stands called cassettes
    specialised cranes move containers from rails to cassettes.
    translifters move cassettes to the AutomaticStackingCrane

straddle-carriers carry boxes to stacks
"""
