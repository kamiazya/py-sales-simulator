from .interfaces import AbstractPath, AbstractState, AbstractContext

class Path(AbstractPath):
    """経路"""
    def __init__(self, ctx: AbstractContext, from_state: AbstractState, to_state: AbstractState):
        self._from_state = from_state
        self._to_state = to_state

    def from_state(self):
        return self._from_state

    def to_state(self):
        return self._to_state
