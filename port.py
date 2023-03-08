import asyncio


COUPLING_TIME_MILLISECONDS = 100
DECOUPLING_TIME_MILLISECONDS = 100


class InvalidSizeException(Exception):
    def __init__(self, invalidSize):
        message = f'{invalidSize}m is not a valid size for a shipping container'
        super().__init__(message)


class ConatinerSizeConflict(Exception):
    def __init__(self):
        message = f'Can\'t stack container size 6.06m on one container sized 2.59m'
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


class LayerHalfFull(Exception):
    """When trying to remove a pair of short containers, but there is only one short container to remove"""

    def __init__(self):
        super().__init__('There is only one container on this layer.')


class PairExpected(Exception):
    """When trying to remove a pair of short containers, but the layer is just a long container"""

    def __init__(self):
        super().__init__('The top layer is 1 long container when expecting 2 short containers.')


class LayerExpected(Exception):
    """Raised when a layer is expected as an input, but a list is not recieved"""

    def __init__(self):
        super().__init__('A layer of containers was expected but a list was not given. Check if the argument passed in is a Container instead of a list of containers.')


class ContainerSize:
    lengths = [2.59, 6.06]

    def __init__(self, length):
        if not isinstance(length, float) and (not isinstance(length, int) or isinstance(length, bool)):
            raise TypeError
        else:
            if length not in ContainerSize.lengths:
                raise InvalidSizeException(length)
        self.length: float = length


class Container:
    id = 1

    def __init__(self, length: float, contents: any):
        self.container_size: ContainerSize = ContainerSize(length)
        self.contents: any = contents
        self.is_short = self.container_size.length == ContainerSize.lengths[0]
        self.id = Container.id
        Container.id += 1

    def __repr__(self):
        return f'Container id: {self.id}'


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
    def __init__(self, max_height=10):
        self.layers = [[None]]
        self.top: list[Container] = self.layers[0]
        self.max_height = max_height

    @property
    def stack_full(self) -> bool:
        if len(self.layers) == self.max_height + 1 and self.top_layer_full:
            return True
        return False

    @property
    def max_height_reached(self) -> bool:
        return len(self.layers) == self.max_height + 1

    @property
    def top_layer_full(self) -> bool:
        top: list[Container] = self.top
        if top[0] == None:
            return True
        one_container_in_top = len(top) == 1
        top_layer_consists_of_short_containers = top[0].is_short
        return not (one_container_in_top and top_layer_consists_of_short_containers)

    @property
    def is_empty(self):
        if self.top == [None]:
            return True
        return False

    def add_container(self, layer: list[Container]) -> None:
        if not type(layer) == list:
            raise LayerExpected()
        if self.stack_full:
            raise ContainerStackTooTall()
        if (not self.top_layer_full) and (not layer[0].is_short):
            raise ConatinerSizeConflict()
        elif (not self.top_layer_full) and layer[0].is_short:
            self.top.append(*layer)
        else:
            self.layers.append(layer)
            self.top = self.layers[-1]

    def remove_container(self, remove_pair=False) -> list[Container]:
        if self.is_empty:
            raise ContainerStackEmpty()
        elif remove_pair:
            if not self.top_layer_full:
                raise LayerHalfFull()
            elif len(self.top) == 1:
                raise PairExpected()
        elif not remove_pair:
            if self.top[0].is_short and len(self.top) != 1:
                removed_value = self.top.pop()
                return [removed_value]
        to_remove = self.layers.pop()
        self.top = self.layers[-1]
        return to_remove


class Crane:
    """Base class for all cranes - to do with coupling and decoupling"""

    def __init__(self, lift_time=100, lower_time=100):
        self.coupled_container = [None]
        self.lift_time = lift_time
        self.lower_time = lower_time

    async def couple(self):
        await asyncio.sleep(COUPLING_TIME_MILLISECONDS / 1000)

    async def decouple(self):
        await asyncio.sleep(DECOUPLING_TIME_MILLISECONDS / 1000)

    async def lift(self):
        await asyncio.sleep(self.lift_time / 1000)

    async def lower(self):
        await asyncio.sleep(self.lower_time / 1000)


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
