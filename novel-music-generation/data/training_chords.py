import numpy as np
"""
    Training chords key:values are chord:label
    Labels are as follows:
    {1 : “Anxiety”, 2 : “Depression”, 
    3 : “Exuberance”, 4 : “Contentment”}
"""
training_chords_X = np.array(
    [
        "C G Am F",
        "Am Dm Fm C",
        "Em Bm G Em",
        "F G Am Bm",
        "Em C D Bm C A Bm G",
        "A E F#m D A E",
        "Bm A G F#",
        "F#m E D7 E",
        "F7 E7 Ebm7 D7",
        "C Dm F#dim G7",
        "G Cm Fm7 Eb",
        "C Dm Am Fm",
        "Fm Db Ab Eb",
        "Am G F Dm",
        "G Bb C G",
        "Bm E7 G F#m",
        "D A Bm G",
        "Bm7 E7 A7",
        "E B C#m A",
        "Dm7 G7 Cmaj7 Fmaj7",
        "Am7 Em7 G",
        "C G A D",
        "Eb Bb Cm Bb",
        "G C E D",
        "G A C D",
        "G A Cmaj7 B",
        "Cm Ab G",
        "Bm G D A",
        "Dmaj7 A F#m Amaj7",
        "Eb Bbm Bbm Fm7",
        "Bb Gm C Eb",
        "G F Gsus4 C",
        "D#m7 C#sus4 D#m G#m7",
        "Eb Ab Bbm Ab",
        "C#m C#m F#m7 C#m7",
        "A E C E",
        "G#m C#m A F#m",
        "Gb Ab7 Gbmaj7 Ab",
        "E Bsus2 B E",
        "C Bb F C", 
        "F#m Bm Bm Em", 
        "F#m G#m F#m G#m",
        "F F Gm C7",
        "Em F Dm C",
        "Fm Dbmaj7 Db Bbm",
        "F#m Bm7 Gmaj7 D", 
        "C# G# D# G#",
        "D A Bm G"
    ]
)

training_chords_y = np.array(
    [
        4,
        2,
        2,
        1,
        1,
        2,
        2,
        1,
        1,
        1,
        2,
        2,
        4,
        2,
        3,
        4,
        4,
        4,
        3,
        4,
        3,
        4,
        3,
        2,
        2,
        4,
        1,
        4,
        4,
        4,
        3,
        3,
        2,
        4,
        2,
        3,
        1,
        4,
        3,
        4, 
        2, 
        1,
        4,
        2,
        1,
        2,
        4,
        1
    ]
)

#print(training_chords_X.size) == 47
#print(training_chords_y.size) == 47



