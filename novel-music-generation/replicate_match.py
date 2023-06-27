import replicate
import pretty_midi
import matplotlib.pyplot as plt

midi_path = pretty_midi.PrettyMIDI('input.mid') #TODO replace

output = replicate.run(
    "mtg/music-arousal-valence:1064850eeb2853ac69d7ff50c05404e7113ade77e176a6760086354e49c13dee",
    input={"audio": open(midi_path, "rb")}
)
print(output)

expected_quadrant = "" #TODO get expected quadrant from other code
predicted_quadrant = "" 

sampling_rate = 10
hop_size = 1


valence, arousal = rav.predict_valence_arousal(midi_data, sampling_rate=sampling_rate, hop_size=hop_size)
if valence > 0: 
    if arousal > 0:
        predicted_quadrant = 1
    else:
        predicted_quadrant = 4
else:
    if arousal > 0:
        predicted_quadrant = 2
    else:
        predicted_quadrant = 3

#unnecessary but helpful to visualize
fig, ax = plt.subplots()
ax.plot(valence, arousal)
ax.set_xlabel('Valence')
ax.set_ylabel('Arousal')
ax.set_title('Valence-Arousal Plot')
plt.show()

if expected_quadrant == predicted_quadrant:
    return "match"
else: 
    pass #TODO re-run music generation or use diff MIDI input for Replicate model to analyze