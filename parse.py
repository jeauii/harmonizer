import sys
import numpy as np
import xml.etree.ElementTree as ET

INPUT_LEN = 32
VOCAB_PATH = 'vocab/chords.txt'

SCALE_NOTES = [0, 2, 4, 5, 7, 9, 11]
SCALE_QUALITY = ['', 'm', 'm', '', '', 'm', 'dim']
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def parse_note(node):
    if node.findtext('isRest') == '1':
        return None

    deg = node.findtext('scale_degree')

    note = SCALE_NOTES[int(deg[0]) - 1]
    if deg[1:] == 's':
        note = (note + 1) % 12
    elif deg[1:] == 'f':
        note = (note - 1) % 12
    
    return note

def parse_chord(node):
    if node.findtext('isRest') == '1':
        return None
    
    sd = node.findtext('sd')
    fb = node.findtext('fb')
    sec = node.findtext('sec')
    sus = node.findtext('sus')
    #emb = node.findtext('emb')

    root = SCALE_NOTES[int(sd) - 1]

    quality = SCALE_QUALITY[int(sd) - 1]
    if sus == 'sus2':
        quality = 'sus2'
    elif sus == 'sus4':
        quality = 'sus4'

    bass = root
    extension = ''
    if fb == '6':
        bass = SCALE_NOTES[(int(sd) + 1) % 7]
    elif fb == '64':
        bass = SCALE_NOTES[(int(sd) + 3) % 7]
    elif fb == '7':
        extension = '7'
    elif fb == '65':
        bass = SCALE_NOTES[(int(sd) + 1) % 7]
        extension = '7'
    elif fb == '43':
        bass = SCALE_NOTES[(int(sd) + 3) % 7]
        extension = '7'
    elif fb == '42':
        bass = SCALE_NOTES[(int(sd) + 5) % 7]
        extension = '7'
    elif fb == '9':
        extension = '9'
    elif fb == '11':
        extension = '11'
    elif fb == '13':
        extension = '13'
    
    if sec:
        root = (root + SCALE_NOTES[int(sec) - 1]) % 12
        bass = (bass + SCALE_NOTES[int(sec) - 1]) % 12

    return NOTE_NAMES[root] + quality + extension + '/' + NOTE_NAMES[bass]

def parse(notes_node, chords_node, vocab):
    notes, chords = [], []

    if notes_node is not None:
        iter = notes_node.iter('note')
    note_node = next(iter, None) if notes_node else None
    note = None
    for chord_node in chords_node.iter('chord'):
        chord = parse_chord(chord_node)
        
        chord_start = float(chord_node.findtext('start_beat_abs'))
        chord_length = float(chord_node.findtext('chord_duration'))

        group = []
        if note is not None and note_start + note_length > chord_start:
            group.append((note, note_start + note_length - chord_start))
        while note_node is not None and \
            float(note_node.findtext('start_beat_abs')) < chord_start + chord_length:
            note = parse_note(note_node)

            note_start = float(note_node.findtext('start_beat_abs'))
            note_length = float(note_node.findtext('note_length'))
            
            if note is not None:
                group.append((note, min(note_length, chord_start + chord_length - note_start)))

            note_node = next(iter, None)

        if chord in vocab:
            index = vocab.index(chord)
        else:
            index = len(vocab)
            vocab.append(chord)
        
        notes.append(group)
        chords.append(index)

    return notes, chords

def main():
    x, y, z = [], [], []
    vocab = [None]

    for arg in sys.argv[2:]:
        tree = ET.parse(arg)
        root = tree.getroot()

        for segment_node in root.iter('segment'):
            notes_node = segment_node.find('.//notes')
            chords_node = segment_node.find('.//chords')
            notes, chords = parse(notes_node, chords_node, vocab)

            for i, group in enumerate(notes):
                duration = np.zeros(12)
                sequence = np.zeros(INPUT_LEN)
                for note, note_length in group:
                    if note is not None:
                        duration[note] += note_length
                sequence[:i] = chords[:i]
                x.append(duration)
                y.append(sequence)
                z.append(chords[i])
    
    np.savetxt(VOCAB_PATH, vocab, fmt='%s')

    np.savez_compressed(sys.argv[1], x=x, y=y, z=z)

if __name__ == '__main__':
    main()
