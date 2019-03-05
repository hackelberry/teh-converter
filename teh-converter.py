#!/usr/bin/env python
# coding: utf-8

from mido import MidiFile
import operator


def get_notes(filename):
    mid = MidiFile(filename)

    tempo = 500000

    notes = []

    for i, track in enumerate(mid.tracks):
        #print('Track {}: {}'.format(i, track.name))
        
        dt = 0
        
        for msg in track:
            dt += msg.time
            
            if msg.type == 'set_tempo':
                tempo = msg.tempo
                
            if msg.type == 'note_on':
                notes.append((msg.note, dt * tempo / (96 * 1000)))


    notes = list(set(notes))
    notes.sort(key=operator.itemgetter(1))

    return notes


def convert(note, strategy):
    # uses the playable midi notes between 52 and 76 (E3 and E5)
    # and ignores everything else
    if strategy == 'basic-high':
        if note == 52:
            return 0
        if note == 57:
            return 1
        if note == 62:
            return 2
        if note == 67:
            return 3
        if note == 71:
            return 4
        if note == 76:
            return 5
        
    # assumes midi notes 0-5 correspond to strings 0-5
    # and ignores everything else
    elif strategy == 'basic':
        if note == 0:
            return 0
        if note == 1:
            return 1
        if note == 2:
            return 2
        if note == 3:
            return 3
        if note == 4:
            return 4
        if note == 5:
            return 5
        
    # transposes all playable notes to the playable octave and ignores everything else.
    # does not use the high E (6th) string
    elif strategy == 'ignore':
        if note % 12 == 4:
            return 0
        if note % 12 == 9:
            return 1
        if note % 12 == 2:
            return 2
        if note % 12 == 7:
            return 3
        if note % 12 == 11:
            return 4
        
    # uses a reasonably close playable note, probably sounds like garbage.
    # does not use the high E (6th) string
    elif strategy == 'closest':
        if note % 12 in [4, 5, 6]:
            return 0
        if note % 12 in [9, 10]:
            return 1
        if note % 12 in [2, 3]:
            return 2
        if note % 12 in [7, 8]:
            return 3
        if note % 12 in [11, 0, 1]:
            return 4

    else:
        return None


def process(notes, strategy, output):
    notes = [notes[i] for i in range(len(notes)) if convert(notes[i][0], strategy) is not None]

    with open(output, 'w') as outfile:
        outfile.write('// This file was generated automatically using teh-converter.py\n\n')

        outfile.write('struct Hit {\n')
        outfile.write('    uint16_t string;\n')
        outfile.write('    uint16_t time;\n')
        outfile.write('};\n\n')

        outfile.write('#define HIT_COUNT ' + str(len(notes)) + '\n')
        outfile.write('struct Hit hits[HIT_COUNT];\n\n')

        outfile.write('void set_notes() {\n')
        for i in range(len(notes)):
            outfile.write('    hits[' + str(i) + '].string = ' + str(convert(notes[i][0], strategy)) + ';\n')
            outfile.write('    hits[' + str(i) + '].time = ' + str(int((notes[i][1]))) + ';\n\n')
        outfile.write('}')


import argparse

parser = argparse.ArgumentParser(description='Converts midi files to our format.')
parser.add_argument('input', help='input midi file')
parser.add_argument('output', help='output C source file')
parser.add_argument('-s', '--strategy', help='strategy to use when encountering unplayable notes', default='closest')

args = parser.parse_args()

process(get_notes(args.input), strategy=args.strategy, output=args.output)