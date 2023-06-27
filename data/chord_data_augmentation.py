import numpy as np
import training_chords
import csv


anxiety_bi_grams = None
depression_bi_grams = None
exuberance_bi_grams = None
contentment_bi_grams = None

gen_anx_chords = []
gen_dep_chords = []
gen_exu_chords = []
gen_con_chords = []

PROBABILITY_THRESHOLD = 0.4
LOOK_BACK = -4
WEIGHTS = [6.75, 1.15, .6]  # MAKE SURE THAT THE NUMBER OF WEIGHTS MATCHES |LOOK_BACK| - 3
REPEAT_MULTIPLIER = 0.35



def format_list(list_of_chords):
    """
    Formats a list of generated chords to write into a csv file
    :param list_of_chords:
    :return: list consisting of labeled chords
    """
    formatted_list = np.empty([len(list_of_chords), 2], dtype=object)
    for i, chord_and_label in enumerate(list_of_chords):
        chord = chord_and_label[0]
        label = chord_and_label[1]
        formatted_list[i, 0] = chord
        formatted_list[i, 1] = label

    return formatted_list.tolist()

def generate_bi_grams(chords):
    """
    This function takes the provided data of chords and labels and generates
    the bi grams (edge to edge) transitions for each of the chords.
    Returns a list of all bigrams
    :param chords - numpy.array of chords:
    :return bi_grams_chord_transitions:
    """
    bi_grams_chord_transitions = [(x, i.split()[j + 1]) for i in chords
       for j, x in enumerate(i.split()) if j < len(i.split()) - 1]
    return bi_grams_chord_transitions

def get_chord_bi_grams(bi_grams, chord):
    """
    Get the bi_grams for the current chord
    :param bi_grams: bi_grams of a specific label
    :param chord: current chord
    :return: bi_grams of the given chord
    """
    return [bi_gram for bi_gram in bi_grams if bi_gram[0] == chord]

def compute_probabilities(bi_grams):
    """
    Computes the probabilties for each transistion of a chord given its bi_grams
    :param bi_grams:
    :return: Tuple of list of possible chords and list of probabilities
    """
    occurrences = {item: bi_grams.count(item) for item in bi_grams}
    for ngram in occurrences.keys():
        occurrences[ngram] = occurrences[ngram] / len(bi_grams)
    options = [key[1] for key in occurrences.keys()]
    probabilities = list(occurrences.values())

    return options, probabilities


def softmax(x):
    """
    Computes the softmax of a given probability array x
    :param x:
    :return softmax x:
    """
    e_x = np.exp(x)
    return e_x / e_x.sum()


def eliminate_repeat(generated_chord, options, probabilities):
    """
    Removes any options that could lead to the generated chord having two chords repeated
    back to back
    :param generated_chord:
    :param options:
    :param probabilities:
    :return options, probabilities:
    """
    try:
        last_chord = generated_chord.split()[-1]

        i = options.index(last_chord)

    except ValueError as e:
        return options, probabilities

    options.pop(i)
    probabilities.pop(i)
    return options, probabilities




def reduce_repeats(generated_chord, options, probabilities):
    """
    Reduces probabilities for a chord to be selected if the chord is already
    found in the current generated chord. This is to reduce the likelihood that
    a generated chord is just the same 3 chords repeated over and over
    :param generated_chord:
    :param options:
    :param probabilities:
    :return probabilities:
    """
    global REPEAT_MULTIPLIER
    options, probabilities = eliminate_repeat(generated_chord, options, probabilities)
    for i, chord in enumerate(options):
        if chord in generated_chord:
            probabilities[i] = REPEAT_MULTIPLIER * probabilities[i]
    return options, probabilities



def generate_chord(chord, bi_grams, label, n):
    """
    Generate the chord progression for the given initial chord and the list of bi_grams until chord
    progression is of length n.
    :param chord - list of chords:
    :param bi_grams - list of bigrams:
    :param label - the desired mood to be achieved
    :param n - desired length of chord progression
    :return:
    """
    global PROBABILITY_THRESHOLD
    global LOOK_BACK
    global WEIGHTS
    generated_chord = chord

    for i in range(n):
        prev_chords = generated_chord.split()[-1: LOOK_BACK: -1]
        chord_options = []
        p = []
        for j, chord in enumerate(prev_chords):
            chord_bi_grams = get_chord_bi_grams(bi_grams, chord)
            options, probabilities = compute_probabilities(chord_bi_grams)
            options, probabilities = reduce_repeats(generated_chord, options, probabilities)
            chord_options = chord_options + options

            if len(probabilities) == 1:
                probabilities = list(WEIGHTS[j] * 0.2 / (j + 1) * np.array(probabilities))
                p = p + probabilities
            else:

                p = p + list(WEIGHTS[j] * np.array(probabilities))
        p = softmax(p)
        try:
            predicted_chord = np.random.choice(chord_options, p=p)
            generated_chord = generated_chord + " " + predicted_chord
        except ValueError as e:
            print(f"Error: {e}")
            continue

    return generated_chord, label






def main():
    """
    Main
    :return: Tuple of list of generated chords
    """
    global anxiety_bi_grams
    global depression_bi_grams
    global exuberance_bi_grams
    global contentment_bi_grams

    X = training_chords.training_chords_X
    Y = training_chords.training_chords_y

    anxiety_chords = X[Y == 1]
    depression_chords = X[Y == 2]
    exuberance_chords = X[Y == 3]
    contentment_chords = X[Y == 4]

    anxiety_bi_grams = generate_bi_grams(anxiety_chords)
    depression_bi_grams = generate_bi_grams(depression_chords)
    exuberance_bi_grams = generate_bi_grams(exuberance_chords)
    contentment_bi_grams = generate_bi_grams(contentment_chords)

    for i in range(100):
        n = np.random.randint(4, 8)
        starting_anx_chord = np.random.choice(np.random.choice(anxiety_chords).split()[:2])
        starting_dep_chord = np.random.choice(np.random.choice(depression_chords).split()[:2])
        starting_exu_chord = np.random.choice(np.random.choice(exuberance_chords).split()[:2])
        starting_con_chord = np.random.choice(np.random.choice(contentment_chords).split()[:2])
        gen_anx_chords.append(generate_chord(starting_anx_chord, anxiety_bi_grams, 1, n))
        gen_dep_chords.append(generate_chord(starting_dep_chord, depression_bi_grams, 2, n))
        gen_exu_chords.append(generate_chord(starting_exu_chord, exuberance_bi_grams, 3, n))
        gen_con_chords.append(generate_chord(starting_con_chord, contentment_bi_grams, 4, n))

    return gen_anx_chords, gen_dep_chords, gen_exu_chords, gen_con_chords


def has_pattern(chord):
    """
    Returns True if a pair of chords in the chord progression repeats in that progression
    :param chord:
    :return bool:
    """
    first = 0
    last = 1
    chord_list = list(chord.split(" "))
    while last < len(chord_list):
        chord_pair = chord_list[first:last + 1]
        chord_str = ' '.join(chord_pair)
        sublist = chord_list[last + 1:]
        c = " ".join(sublist)
        if c.find(chord_str) != -1:
            return True
        else:
            first = first + 1
            last = last + 1
    return False

def is_valid_chord_progression(chord_progression):
    """
    Given a chord progression, returns true if the chord does not have more than 3 duplicates of
    a chord or if there is no repeated pair of chords.
    :param chord_progression:
    :return bool:
    """
    map = {}
    chord = chord_progression[0]
    for c in chord.split():
        if c not in map.keys():
            map[c] = 1
        else:
            map[c] = map[c] + 1
        if map[c] >= 3:
            return False

    if has_pattern(chord):
        return False

    return True


def trim_chords(list_of_chords):
    trimmed_list_of_chords = []
    for chord_progression in list_of_chords:
        if is_valid_chord_progression(chord_progression):
            print(f'{chord_progression} is valid')
            trimmed_list_of_chords.append(chord_progression)
        else:
            print(f'{chord_progression} is not valid')
    return trimmed_list_of_chords



if __name__ == "__main__":
    seed = 1234
    np.random.seed(seed)
    #seed = np.random.seed()
    anx, dep, exu, con = main()
    list_of_chords = [*anx, *dep, *exu, *con]
    list_of_chords = format_list(list_of_chords)

    labeled_chords = trim_chords(list_of_chords)
    list_of_chords = [[pair[0]] for pair in labeled_chords]
    list_of_labels = [[pair[1]] for pair in labeled_chords]

    try:
        with open(f'Chords{seed}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile,
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(["Chord"])
            writer.writerows(list_of_chords)
            csvfile.close()
    except Exception as e:
        print(f'Could not write to csv file\nError: {e}')
        pass

    try:
        with open(f'Chord_Labels{seed}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Label"])
            writer.writerows(list_of_labels)
            csvfile.close()
    except Exception as e:
        print(f'Could not write to csv file \nError: {e}')
        pass
