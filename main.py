#TODO: obtain midi Sentino Midas and maybe some others
#TODO: MIDI library
#mido https://mido.readthedocs.io/en/latest/message_types.html
import mido
#TODO: MIDI instruments/samples
#z teoria muzyki too jakos wspolgra, ale nw czy bedzie warto ogarniac https://pythonlang.dev/repo/rainbow-dreamer-musicpy/
#TODO: graph of midi events
#TODO: ant traversing implementation
#TODO: playing music
#TODO: saving music


#1) mido trzeba zaladowac ta biblioteka plik midi (np ten co jest na gicie) i zobaczyc jak on tam wyglada
# w sensie jak te kolejne zdzarzenia midi wystepuja i czy tam sie gdzies ustawia jaki instrument gra
# poza sama osia czasu jakby, czy jak

#2) jakos na podstawie tego uzupelnic nasza klase nutek i nastepnie Grafu muzyki
#3) zagrac na naszym grafie sentino
 #3.2) ogarnac co to jest za wyrazenie w tamtej pracy ktorym mrowka decyduje gdzie pojsc krawedziami
#4) ustawic przy tym zagraniu poczatkowe wartosci na krawedziach (?)
# jakos tak zrozumialem z tej pracy ale nie jestem pewny

#5) puscic mruweczki po grafie, zeby cos naklikaly i pozapisywaly do pliku midi
#6) odtworzyc plik wynikowy uzywajac playmidi

sentino  = mido.MidiFile('midi/sentino.mid')
for i, track in enumerate(sentino.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)