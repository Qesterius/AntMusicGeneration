#TODO: obtain midi Sentino Midas and maybe some others
#TODO: MIDI library
#mido https://mido.readthedocs.io/en/latest/message_types.html
import mido
from queue import PriorityQueue
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

sentino = mido.MidiFile('midi/sentino.mid')
def printTrack(track):
        for msg in track:
            print(msg)

def process(track):
    notes_non_dup = []
    timeline=[]
    cur_time=0
    for i,msg in enumerate(track):
        cur_time+=msg.time
        if msg.type == 'note_on':
            note = msg.note
            time =0
            j=i+1
            while track[j].type != 'note_off' and track[j].note != note:
                time+= track[j].time
                j+=1

            index=0
            if (note,time) in notes_non_dup:
                index = notes_non_dup.index((note,time))

            else:
                index = len(notes_non_dup)
                notes_non_dup.append((note,time))
            timeline.append((cur_time,index))

    return notes_non_dup,timeline
from graph import Note

def createNotes(keys):
    Notes=[]
    for key in keys:
        note,time = key
        Notes.append(Note(time,note))

    return Notes

def recreateMidifromGraphPath(path,keys):
    file = mido.MidiFile()
    outTrack = mido.MidiTrack()
    file.tracks.append(outTrack)
    queue = PriorityQueue()
    for p in path:
        queue.put( (p[0],p[1], 1))

    last_time=0
    while not queue.empty():
        top = queue.get()
        action = 'note_on' if top[2] == 1 else 'note_off'
        timeline_time = top[0]
        note_ind = p[1]
        if action == 'note_on':
            queue.put((timeline_time+keys[note_ind].time,p[1],0))

        outTrack.append(mido.Message(action,note=keys[note_ind].note,velocity=64,time=timeline_time-last_time))
        last_time = timeline_time

    file.save("midi/out.mid")



notess,timeli = process(sentino.tracks[0])
print("notes:",notess)
print("timeli:",timeli)

notess = createNotes(notess)
recreateMidifromGraphPath(timeli,notess)