import mido
from random import randint, random


class Note:
    # wysokosc dzwieku
    # dlugosc dzwieku nw jak robimy jesazce z taktowaniem -> to takie co jest 4/4 na przyklad

    def __init__(self, time, note):
        self.time = time
        self.note = note

    def create_message(self):
        msg = mido.Message('note_on', channel=0, note=self.note, velocity=64, time=0)
        return msg

    def __gt__(self, other):
        return self.note >= other.note


class Graph:

    def __init__(self, notes, ants_num, pheromones):
        self.notes = notes
        self.ants = [randint(min(notes), max(notes) + 1) for _ in range(ants_num)]
        self.pheromones = pheromones

    # nodes
    # adjencymatrix
    def move_ants(self):
        for ant in self.ants:
            n = len(self.notes)
            prob = random()
            _sum = 0
            for i in range(n):
                _sum += self.pheromones[ant][i] * 1/abs(self.notes[i].note - self.notes[ant].note)
            for i in range(n):
                if prob < self.pheromones[ant][i]/_sum:
                    self.ants[ant] = i

    def create_music(self, scale, bpm, metryka):
        # scale to moze byc rownie dobrze tutaj maska po prostu jakie wierzcholki bedziemy uzywac (ostatecznie chcemy, zeby wierzcholkow bylo przynajmniej z jakis 2 utworow o roznych skalach)
        # bpm to w sumie wyjebane, bo to kwestia czy wszystko bedzie szybciej czy wolniej, mozna ustawic jako stale nawet
        # metryke mozemy ustalic 4/4 bo jest podstawowwe, ale w sumie trzeba do tego przysiasc https://pl.wikipedia.org/wiki/Takt_(muzyka) / https://pl.wikipedia.org/wiki/Metrum_(muzyka)

        il_jedn_metr_na_takt, jednostka_metryczna = metryka  # to oznacza tyle, ze na jeden takt w utworze przypada ilestam cwiercnut/szesnastek itd.
