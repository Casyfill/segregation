from random import shuffle
import pandas as pd
from .family import Family


def _permutate(num):
    L = [(i, j) for i in range(num) for j in range(num)]
    shuffle(L)
    return L


class City(object):
    size = None
    matrix = None
    ratio = None
    happy = None
    families = {}
    empty = []
    all_happy = False
    age = 0

    def __init__(self, size, famTypes: dict):

        self.size = size
        # self.matrix = np.ndarray((self.size, self.size), int)
        self.families = {}
        self.empty = []
        self.all_happy = False

        self.populate(famTypes)
        self.age = 0

    def populate(self, famTypes: dict):
        total_pop = sum(famTypes.values())
        space = self.size ** 2

        assert (
            total_pop <= space
        ), f"Overpopulated: {total_pop} families for {space} lots"
        self.ratio = total_pop / space
        self.empty = _permutate(self.size)
        print(f"Density: {self.ratio:.0%}, lots:{len(self.empty)}")

        for tp, num in famTypes.items():
            for _ in range(num):
                pos = self.empty.pop()
                # print(f'Populating: {tp}; {pos}; Empty lots: {len(self.empty)}')
                self.families[pos] = Family(tp=tp, pos=pos)

    def mood_survey(self):
        happy = {"total": 0}

        for f in self.families.values():
            mood = f.check_mood(city=self)
            happy["total"] += mood
            happy[f.tp] = happy.get(f.tp, 0) + mood

        return happy

    def relocate(self):
        assert len(self.empty) > 0, "Nowhere to move!"
        all_happy = True

        for f in self.families.values():
            if not f.check_mood(city=self):
                all_happy = False
                f.relocate(city=self)

        self.happy = self.mood_survey()
        self.all_happy = all_happy

    def get_plottable(self, empty=False):

        df = pd.DataFrame([f.get_dict(city=self) for f in self.families.values()])

        if empty:
            df_empty = pd.DataFrame([{"x": p[0], "y": p[1]} for p in self.empty])
            df = pd.concat([df, df_empty], sort=False)

        return df

    def plot(self):
        self.get_plottable(empty=True).plot.scatter(x="x", y="y")

    def evolve(self, max_age=100):
        stats = {self.age: self.mood_survey()}

        for i in range(max_age):
            if (self.age >= max_age) or (self.all_happy):
                return pd.DataFrame(stats).T

            self.age += 1
            self.relocate()
            stats[self.age] = self.mood_survey()

        return pd.DataFrame(stats).T  # theoretically, should never execute
