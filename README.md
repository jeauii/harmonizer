Some XML dumps of songs from hooktheory collected by: https://github.com/Glamdring/computoser

These files are the results of queries like https://www.hooktheory.com/songs/getXmlByPk?pk=7840

Note that not the ID range for songs seems to vary dramatically and there are a large number of IDs that result in 404 or 403 response codes, or are for test data that you'll want to exclude (I don't know how to detect them automatically, but you can see some stuff is named "test" etc).

This repo exists to provide educational value for those interested in musical analysis or machine learning. If you have any questions or concerns please contact me at owencmoore@gmail.com

Some notes on the structure of the XML files:

- Doesn't seem like each file has a very fixed format.
- The key and mode are at the top of each file, and the chords / notes are all relative to those
- Some have a <harmony> tag that contains the chords, some has a <chords> tag.
- Sometimes multiple beats of a certain chord are represented by one <chord> per beat, so to get cleaner chords probably merge these
- Some songs are broken into multiple <segment>s but it's unclear what these correspond to, but based on spot checks it seems generally safe to just merge them

An example chord with notes:

    <chord>
      <!-- sd is the root of the chord (in number of tones relative to the key, e.g. 2 is D for a piece in C) -->
      <sd>2</sd>
      <!-- the figured bass. Seems to use 'symbol most often used' from the top answer here: https://music.stackexchange.com/questions/14866/classical-music-theory-notation-for-chord-inversions-figured-bass -->
      <fb/>
      <!-- if this is set, it means the chord should be the one notated by sd and fb but "of" or "relative to" this one. So 6 here with 7 in sd means a VII chord, but taking VI as root instead of I -->
      <sec/>
      <!-- only ever 'add9' or empty -->
      <emb>add9</emb>
      <!-- sus is one of 'sus2', 'sus4' or 'sus42' -->
      <sus/>
      <!-- no idea!! -->
      <pedal/>
      <!-- no idea!! -->
      <alternate/>
      <!-- borrowed indicates that this chord should follow a different mode. It's not clear to me what the mapping is of value to mode to borrow from (relative? absolute? etc) -->
      <borrowed>1</borrowed>
      <!-- self explanitory, the length of the chord -->
      <chord_duration>0.75</chord_duration>
      <!-- which bar the chord should be placed within -->
      <start_measure>2</start_measure>
      <!-- the point within the bar the chord should be inserted -->
      <start_beat>1.75</start_beat>
      <!-- the absolute timing point within the YouTube recording that this chord goes -->
      <start_beat_abs>4.75</start_beat_abs>
      <!-- a binary value that represents whether this is actually just a rest, I don't think this is used for chords, only for notes, but I could be wrong -->
      <isRest>0</isRest>
    </chord>
