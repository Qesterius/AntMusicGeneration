# TODO: obtain midi Sentino Midas and maybe some others
# TODO: MIDI library
# mido https://mido.readthedocs.io/en/latest/message_types.html
import mido
from queue import PriorityQueue

# TODO: MIDI instruments/samples
# z teoria muzyki too jakos wspolgra, ale nw czy bedzie warto ogarniac https://pythonlang.dev/repo/rainbow-dreamer-musicpy/
# TODO: graph of midi events
# TODO: ant traversing implementation
# TODO: playing music
# TODO: saving music


# 1) mido trzeba zaladowac ta biblioteka plik midi (np ten co jest na gicie) i zobaczyc jak on tam wyglada
# w sensie jak te kolejne zdzarzenia midi wystepuja i czy tam sie gdzies ustawia jaki instrument gra
# poza sama osia czasu jakby, czy jak

# 2) jakos na podstawie tego uzupelnic nasza klase nutek i nastepnie Grafu muzyki
# 3) zagrac na naszym grafie sentino
# 3.2) ogarnac co to jest za wyrazenie w tamtej pracy ktorym mrowka decyduje gdzie pojsc krawedziami
# 4) ustawic przy tym zagraniu poczatkowe wartosci na krawedziach (?)
# jakos tak zrozumialem z tej pracy ale nie jestem pewny

# 5) puscic mruweczki po grafie, zeby cos naklikaly i pozapisywaly do pliku midi
# 6) odtworzyc plik wynikowy uzywajac playmidi

from graph import Graph
import random

sentino = mido.MidiFile('midi/sentino.mid')
out = mido.MidiFile()
print("ticks", sentino.ticks_per_beat)


def printTrack(track):
    for msg in track:
        print(msg)


def process(track):
    notes_non_dup = []
    velocity_arr = []
    timeline = []
    route = []
    cur_time = 0
    for i, msg in enumerate(track):
        cur_time += msg.time
        if msg.type == 'note_on':
            note = msg.note
            time = 0
            j = i + 1
            while track[j].type != 'note_off' or track[j].note != note:
                # if(note == 68):
                # print(track[j].note)
                time += track[j].time
                j += 1
            # print()
            time += track[j].time
            index = 0
            if (note, time) in notes_non_dup:
                index = notes_non_dup.index((note, time))

            else:
                index = len(notes_non_dup)
                notes_non_dup.append((note, time))
                velocity_arr.append(msg.velocity)
            timeline.append((cur_time, index))
            route.append((cur_time, note))

    return notes_non_dup, velocity_arr, timeline, route


from graph import Note


def createNotes(keys, velocity_arr):
    Notes = []
    for i, key in enumerate(keys):
        note, time = key
        Notes.append(Note(time, note, velocity_arr[i]))

    return Notes


def create_notes_without_time(keys, velocity_arr):
    Notes = []
    keys = map(lambda x: x[0], keys)
    keys = list(set(keys))
    # print(keys)
    for i, key in enumerate(keys):
        note = key
        Notes.append(Note(4, note, velocity_arr[i]))
    return Notes


def recreateMidifromGraphPath(path, keys):
    file = mido.MidiFile()
    file.ticks_per_beat = sentino.ticks_per_beat
    outTrack = mido.MidiTrack()
    file.tracks.append(outTrack)
    queue = PriorityQueue()
    for p in path:
        queue.put((p[0], p[1], 1))

    last_time = 0
    while not queue.empty():
        top = queue.get()
        action = 'note_on' if top[2] == 1 else 'note_off'
        timeline_time = top[0]
        note_ind = top[1]
        # print(note_ind)
        if action == 'note_on':
            queue.put((timeline_time + keys[note_ind].time, top[1], 0))

        outTrack.append(mido.Message(action, note=keys[note_ind].note, velocity=keys[note_ind].velocity,
                                     time=timeline_time - last_time))
        last_time = timeline_time

    # printTrack(outTrack)

    print("ticks", file.ticks_per_beat)
    global out
    out = file
    file.save("midi/out.mid")


notess, velocity_arrr, timeli, route = process(sentino.tracks[0])
# print("notes:", notess)
# print("timeli:", timeli)
# print("route", route)
not_without_time = create_notes_without_time(notess, velocity_arrr)
ants_num = 5
ants = random.choices(list(map(lambda x: x[0], notess)), k=ants_num)
print(ants)

notess = createNotes(notess, velocity_arrr)

graph = Graph(notes=not_without_time, ants=ants, pheromone_increase=1, pheromone_decrease=0.01,
              ants_starting_route=route)
music = graph.create_music(scale=10, bpm=190, metryka=(1, 1), length=1000)
print(music)

recreateMidifromGraphPath(timeli, notess)

import sys

original_stdout = sys.stdout  # Save a reference to the original standard output

with open('LOG.txt', 'w') as f:
    sys.stdout = f  # Change the standard output to the file we created.
    printTrack(sentino.tracks[0])
    print(" ")
    printTrack(out.tracks[0])

    sys.stdout = original_stdout  # Reset the standard output to its original value
