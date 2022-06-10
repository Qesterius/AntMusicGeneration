import mido
from random import randint, random, choices


class Note:
    # wysokosc dzwieku
    # dlugosc dzwieku nw jak robimy jesazce z taktowaniem -> to takie co jest 4/4 na przyklad

    def __init__(self, time, note, velocity):
        self.time = time
        self.note = note
        self.velocity = velocity

    def create_message(self):
        msg = mido.Message('note_on', channel=0, note=self.note, velocity=64, time=0)
        return msg

    def __gt__(self, other):
        return self.note >= other.note


class Graph:

    def initialize_pheromones(self, route):
        route = list(map(lambda x: x[1], route))
        # print(max(route))
        time = 10
        pheromones = [[0 for _ in range(max(route)+1)] for _ in range(max(route)+1)]
        ants = []
        for idx, move in enumerate(route):
            if idx != 0:
                pheromones[route[idx-1]][move] += self.pheromone_increase
        return pheromones

    def __init__(self, notes, ants, pheromone_increase, pheromone_decrease, ants_starting_route):
        self.notes = {note.note: note for note in notes}
        self.ants = ants
        self.last_moves = []
        self.pheromone_increase = pheromone_increase
        self.pheromone_decrease = pheromone_decrease
        self.music = []

        self.pheromones = self.initialize_pheromones(ants_starting_route)
        # print(len(self.pheromones))

    # nodes
    # adjencymatrix
    def move_ants(self):
        n = len(self.notes)
        last_moves = []
        for idx, ant in enumerate(self.ants):
            _sum = 0
            weights = [0 for _ in range(max(self.notes.keys()) + 1)]
            for key in self.notes:
                _sum += self.pheromones[ant][key] / (abs(key - ant) + 1)

            for key in self.notes:
                weights[key] = self.pheromones[ant][key] / (abs(key - ant) + 1) / _sum
            move = choices([i for i in range(max(self.notes.keys())+1)], weights=weights)
            move = move[0]
            # adding moves
            self.music.append((self.notes[move].note, self.notes[move].time))
            self.ants[idx] = move
            self.last_moves.append((ant, move))

        for move_from, move_to in self.last_moves:
            self.pheromones[move_from][move_to] += self.pheromone_increase

        for i in range(n):
            for j in range(n):
                self.pheromones[i][j] *= self.pheromones[i][j] * (1 - self.pheromone_decrease)


    def create_music(self, scale, bpm, metryka, length):
        # scale to moze byc rownie dobrze tutaj maska po prostu jakie wierzcholki bedziemy uzywac (ostatecznie chcemy, zeby wierzcholkow bylo przynajmniej z jakis 2 utworow o roznych skalach)
        # bpm to w sumie wyjebane, bo to kwestia czy wszystko bedzie szybciej czy wolniej, mozna ustawic jako stale nawet
        # metryke mozemy ustalic 4/4 bo jest podstawowwe, ale w sumie trzeba do tego przysiasc https://pl.wikipedia.org/wiki/Takt_(muzyka) / https://pl.wikipedia.org/wiki/Metrum_(muzyka)

        il_jedn_metr_na_takt, jednostka_metryczna = metryka  # to oznacza tyle, ze na jeden takt w utworze przypada ilestam cwiercnut/szesnastek itd.
        for i in range(length):
            self.move_ants()
        return self.music
