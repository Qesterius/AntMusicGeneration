import mido
from random import randint, random, choices


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

    def __init__(self, notes, ants_num, pheromones, pheromone_increase, pheromone_decrease):
        self.notes = notes
        self.ants = [randint(min(notes), max(notes) + 1) for _ in range(ants_num)]
        self.pheromones = pheromones
        self.last_moves = []
        self.pheromone_increase = pheromone_increase
        self.pheromone_decrease = pheromone_decrease

    # nodes
    # adjencymatrix
    def move_ants(self):
        n = len(self.notes)

        for ant in self.ants:
            _sum = 0
            weights = [0 for _ in range(n)]

            for i in range(n):
                _sum += self.pheromones[ant][i] * 1/abs(self.notes[i].note - self.notes[ant].note)

            for i in range(n):
                weights[i] = self.pheromones[ant][i]/_sum
            move = choices([1 for i in range(n)], weights=weights)
            self.ants[ant] = move
            self.last_moves.append((ant, move))

        for move_from, move_to in self.last_moves:
            self.pheromones[move_from][move_to] += self.pheromone_increase

        for i in range(n):
            for j in range(n):
                self.pheromones[i][j] *= self.pheromones[i][j]*(1-self.pheromone_decrease)



    def create_music(self, scale, bpm, metryka):
        # scale to moze byc rownie dobrze tutaj maska po prostu jakie wierzcholki bedziemy uzywac (ostatecznie chcemy, zeby wierzcholkow bylo przynajmniej z jakis 2 utworow o roznych skalach)
        # bpm to w sumie wyjebane, bo to kwestia czy wszystko bedzie szybciej czy wolniej, mozna ustawic jako stale nawet
        # metryke mozemy ustalic 4/4 bo jest podstawowwe, ale w sumie trzeba do tego przysiasc https://pl.wikipedia.org/wiki/Takt_(muzyka) / https://pl.wikipedia.org/wiki/Metrum_(muzyka)

        il_jedn_metr_na_takt, jednostka_metryczna = metryka  # to oznacza tyle, ze na jeden takt w utworze przypada ilestam cwiercnut/szesnastek itd.
