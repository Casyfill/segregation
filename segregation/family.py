import pandas as pd
from random import shuffle
from collections import Counter

QUEEN_POS = ((-1, -1), (-1, 0), (-1, 1),
             (0, -1),           (0, 1),
             (1, -1),  (1, 0),  (1, 1))

ROOK_POS = (         (-1, 0),
            (0, -1),           (0, 1),
                     (1, 0))


class noFamily():
    tp = None


# in the future family should be characterised by their tp and behaviour rule
BEHAVIORAL_RULES = {
    'abs_majority_extravert': lambda s, nbs: nbs[s.tp] > sum(nbs.values()) * .5,
    'abs_majority_intraver': lambda s, nbs: nbs[s.tp] > sum([nbs[k] for k in nbs if k is not None]) * .5,
    'majority': lambda s, nbs: ( s.tp == nbs.most_common(1)[0][0]) and (nbs.most_common(2)[0][1] > nbs.most_common(2)[1][1])
}


class Family(object):
    tp = None
    position = None
    behaviour = None

    def __init__(self, tp, pos, behaviour='abs_majority_extravert'):
        self.tp = tp
        self.position = pos

        assert behaviour in BEHAVIORAL_RULES
        self.behaviour = behaviour
        self.description = f'{tp}:{behaviour}'

    def mood_rule(self, nbs):
        return BEHAVIORAL_RULES[self.behaviour](self, nbs=nbs)

    def _neighb_pos(self, nb):
        # absolute neighb position
        return tuple(sum(el) for el in zip(self.position, nb))

    def get_neighbors(self, city):
        return Counter(city.families.get(self._neighb_pos(pos), NF).tp for pos in QUEEN_POS)

    def check_mood(self, city):
        '''return True if happy'''
        nbs = self.get_neighbors(city)
        return self.mood_rule(nbs)

    def relocate(self, city):
        old_pos = self.position

        shuffle(city.empty)
        self.position = city.empty.pop()
        city.empty.append(old_pos)

    def get_dict(self, city=None):
        D = {'x': self.position[0], 'y': self.position[1],
             'tp': self.tp, 'happy': None, 'behaviour': self.behaviour}

        if city:
            D['happy'] = self.check_mood(city)
        return D
