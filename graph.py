

class Nutka:
    #wysokosc dzwieku
    #dlugosc dzwieku nw jak robimy jesazce z taktowaniem -> to takie co jest 4/4 na przyklad


    def __init__(self):


class Graph:
    #nodes
    #adjencymatrix

    def createMusic(self, scale, bpm, metryka ):
        #scale to moze byc rownie dobrze tutaj maska po prostu jakie wierzcholki bedziemy uzywac (ostatecznie chcemy, zeby wierzcholkow bylo przynajmniej z jakis 2 utworow o roznych skalach)
        #bpm to w sumie wyjebane, bo to kwestia czy wszystko bedzie szybciej czy wolniej, mozna ustawic jako stale nawet
        #metryke mozemy ustalic 4/4 bo jest podstawowwe, ale w sumie trzeba do tego przysiasc https://pl.wikipedia.org/wiki/Takt_(muzyka) / https://pl.wikipedia.org/wiki/Metrum_(muzyka)

        il_jedn_metr_na_takt,jednostka_metryczna = metryka # to oznacza tyle, ze na jeden takt w utworze przypada ilestam cwiercnut/szesnastek itd.