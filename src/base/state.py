from .interfaces import AbstractState, AbstractContext

class State(AbstractState):
    """状態
    """
    def __init__(self, ctx: AbstractContext, name: str):
        self.__ctx = ctx
        self.name: str = name

    @property
    def is_first(self):
        """始点かどうか。始点であれば`True`を返す。
        """
        return len(self.prev_states) == 0

    @property
    def is_last(self):
        """終点かどうか。終点であれば`True`を返す。
        """
        return len(self.next_states) == 0

    @property
    def is_isolated(self):
        """独立かどうか。独立であれば`True`を返す。
        """
        return self.is_last and self.is_first

    @property
    def next_states(self):
        return self.__ctx.get_states_from(self.name)

    @property
    def prev_states(self):
        return self.__ctx.get_states_to(self.name)
