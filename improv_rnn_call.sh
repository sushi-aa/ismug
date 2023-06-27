cd '/Users/raja/AA/UC Irvine/FALL 2022/EECS159A/magenta/magenta/models/improv_rnn'

improv_rnn_generate \
    --config='chord_pitches_improv' \
    --bundle_file='/Users/raja/AA/UC Irvine/FALL 2022/EECS159A/magenta/magenta/models/improv_rnn/chord_pitches_improv.mag' \
    --output_dir=/tmp/improv_rnn/generated \
    --num_outputs=3 \
    --primer_melody="[60]" \
    --backing_chords="C G Am F C G Am F" \
    --render_chords
