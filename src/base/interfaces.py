from typing import List
from abc import abstractproperty, ABCMeta

class AbstractState(metaclass=ABCMeta):
    """状態
    """

    @abstractproperty
    def is_first(self):
        """始点かどうか。始点であれば`True`を返す。
        """
        pass

    @abstractproperty
    def is_last(self):
        """終点かどうか。終点であれば`True`を返す。
        """
        pass

    @abstractproperty
    def is_isolated(self):
        """孤立かどうか。孤立であれば`True`を返す。
        """
        pass

    @abstractproperty
    def next_states(self):
        """次の状態のリストを返す"""
        pass

    @abstractproperty
    def prev_states(self):
        """前の状態のリストを返す"""
        pass

class AbstractPath(metaclass=ABCMeta):

    @abstractproperty
    def from_state(self):
        """経路の始点状態を返す"""
        pass

    @abstractproperty
    def to_state(self):
        """経路の終点状態を返す"""
        pass

class AbstractContext(metaclass=ABCMeta):

    @abstractproperty
    def states(self):
        """状態の一覧を取得する"""
        pass

    @abstractproperty
    def paths(self):
        """経路の一覧を取得する"""
        pass
