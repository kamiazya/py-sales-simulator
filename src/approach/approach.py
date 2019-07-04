from typing import Optional, List, Union

class State(object):
    def __init__(self, ctx: 'Context', name: str, unknown:bool=False, negative:int=0, positive:int=0):
        self.__ctx = ctx
        self.name: str = name
        self.unknown = unknown
        self.negative = negative
        self.positive = positive
        self.point = self.positive - self.negative
        self._fixed: bool = False

    @property
    def fixed(self):
        return self._fixed

    @property
    def is_first(self):
        return len(self.get_prev_states()) == 0

    @property
    def is_last(self):
        return len(self.get_next_states()) == 0

    @property
    def is_standalone(self):
        return self.is_last and self.is_first

    @property
    def is_negative(self):
        return self.negative > 0

    @property
    def is_positive(self):
        return self.positive > 0

    def __get_fixed_path_rate(self):
        if self.is_last:
            return 1.

        rate = 0.
        for path in self.__ctx.get_path_from(self.name):
            if path._probability is not None:
                rate += path._probability
        return rate


    def get_next_states(self):
        return self.__ctx.get_path_from(self.name)

    def get_prev_states(self):
        return self.__ctx.get_path_to(self.name)

    def fix(self):
        fixed = self.__get_fixed_path_rate()
        if self.is_last:
            self.__ctx.create_path(self, self,
                                                 probability=1)
        elif fixed < 1.:
            unknown_probability_paths = list(filter(lambda r: r._probability is None, self.__ctx.get_path_from(self.name)))
            if len(unknown_probability_paths) != 0:
                path_probability = (1. - fixed) / (1.0 * len(unknown_probability_paths))
                for path in unknown_probability_paths:
                    path._probability = path_probability
            else:
                if self.is_last == False:
                    unknown_state = self.__ctx.create_state('{}からの未知'.format(self.name), unknown=True)
                    self.__ctx.create_path(self, unknown_state,
                                                 probability=(1. - fixed))
                else:
                    self.__ctx.create_path(self, self,
                                                 probability=(1. - fixed))

        self._fixed = True

    def will_be(self, state: Union[str, 'State'],
                note: Optional[str]=None,
                probability:Optional[float]=None):


        if type(state) == str:
            next_state = self.__ctx.get_state(state)
            self.__ctx.create_path(self, next_state,
                                        note=note, probability=probability)
        else:
            # State
            self.__ctx.create_path(self, state,
                                        note=note, probability=probability)

class Context(object):
    def __init__(self):
        self.__states: List[State] = []
        self.__paths: List[State] = []
        self._fixed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def fix(self):
        for state in self.__states:
            state.fix()
        self._fixed = True

    def get_states(self, name: str):
        return list(filter(lambda s: s.name == name, self.__states))

    def get_state(self, name: str):
        status = self.get_states(name)
        if len(status) > 0:
            return status[0]
        return None

    def get_paths(self, from_state_name: str, to_state_name: str):
        return list(filter(lambda r: r.from_state.name == from_state_name \
                                                        and r.to_state.name == to_state_name,
                                    self.__paths))

    def create_state(self, name: str, unknown=False, negative: int = 0, positive: int = 0):
        cs = State(self, name,
                       unknown=unknown,
                       negative=negative,
                       positive=positive)

        self.__states.append(cs)
        return cs

    def create_path(self, from_state: State, to_state: State,
                note: Optional[str]=None,
                probability:Optional[float]=None):

        path = Path(self, from_state, to_state,
                                            note=note, probability=probability)
        self.__paths.append(path)
        return path

    def get_path_from(self, name: str):
        return list(filter(lambda r: r.from_state.name == name,
            self.__paths))

    def get_path_to(self, name: str):
        return list(filter(lambda r: r.to_state.name == name,
            self.__paths))

    @property
    def _states(self):
        return self.__states

    @property
    def paths(self):
        return self.__paths


class Path(object):
    def __init__(self, ctx: Context, from_state: State, to_state: State,
                note: Optional[str]=None,
                probability:Optional[float]=None):
        self.from_state = from_state
        self.to_state = to_state
        self.note = note
        self._probability = probability

    @property
    def probability(self):
        return self._probability
