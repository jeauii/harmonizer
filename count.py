import glob
import xml.etree.ElementTree as ET

sd = {}
fb = {}
sec = {}
emb = {}
sus = {}
alt = {}
length = [0] * 32

for arg in glob.glob('xml/*.xml'):
    tree = ET.parse(arg)
    root = tree.getroot()

    for segment in root.iter('segment'):
        notes = segment.find('.//notes')
        chords = segment.find('.//chords')

        count = 0
        for chord in chords.iter('chord'):
            if chord.findtext('sd') not in sd:
                sd[chord.findtext('sd')] = 0
            sd[chord.findtext('sd')] += 1

            if chord.findtext('fb') not in fb:
                fb[chord.findtext('fb')] = 0
            fb[chord.findtext('fb')] += 1

            if chord.findtext('sec') not in sec:
                sec[chord.findtext('sec')] = 0
            sec[chord.findtext('sec')] += 1

            if chord.findtext('emb') not in emb:
                emb[chord.findtext('emb')] = 0
            emb[chord.findtext('emb')] += 1

            if chord.findtext('sus') not in sus:
                sus[chord.findtext('sus')] = 0
            sus[chord.findtext('sus')] += 1

            if chord.findtext('alternate') not in alt:
                alt[chord.findtext('alternate')] = 0
            alt[chord.findtext('alternate')] += 1

            count += 1
        
        length[count] += 1

print(sd)
print(fb)
print(sec)
print(emb)
print(sus)
print(alt)
print(length)
