from typing import List, Union
from state import State
from path import Path
from .interfaces import AbstractContext

class Context(AbstractContext):
    def __init__(self):
        self.__states: List[State] = []
        self.__paths: List[Path] = []

    @property
    def states(self):
        """状態のリストを返す
        """
        return self.__states

    @property
    def paths(self):
        """経路のリストを返す
        """
        return self.__paths

    def get_states(self, name: str):
        """名前を指定して、状態のリストを返す
        """
        return list(filter(lambda s: s.name == name, self.__states))

    def get_state(self, name: str):
        """名前を指定して、状態を返却する
        重複した名前の状態がある場合とき、最初の1件を返却する。
        該当する名前の状態がなかった場合は、`None`を返す。
        """
        status = self.get_states(name)
        if len(status) > 0:
            return status[0]
        return None

    def get_paths(self, from_state_name: str, to_state_name: str):
        """2点間の経路を取得する"""
        return list(filter(lambda r: r.from_state.name == from_state_name \
                                    and r.to_state.name == to_state_name, self.__paths))

    def create_state(self, name: str):
        cs = State(self, name)

        self.__states.append(cs)
        return cs

    def create_path(self, from_state: State, to_state: State):
        path = Path(self, from_state, to_state)
        self.__paths.append(path)
        return path

    def get_paths_from(self, name: str):
        return list(filter(lambda r: r.from_state.name == name, self.__paths))

    def get_states_from(self, name: str):
        return list(map(lambda r: r.to_state, self.get_paths_from(name)))

    def get_paths_to(self, name: str):
        return list(filter(lambda r: r.to_state.name == name, self.__paths))

    def get_states_to(self, name: str):
        return list(map(lambda r: r.from_state, self.get_paths_to(name)))
