# This file is an adaptation/modification of the improv_rnn_generate.py
# code.

import threading
import ast
import os
import time
import mido
import subprocess
import csv
import random
import numpy as np
from timidity import Parser, play_notes
import threading
import pandas as pd
import fluidsynth
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#import pygame
#import pygame.midi
from mido import Message, MetaMessage, MidiFile, MidiTrack

# Initialize Firebase
cred = credentials.Certificate('ismug-1-music gen service key.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'Sensor Data').document(u'Vitals')

chords = pd.read_csv('data/Chords1234.csv').to_numpy()
labels = pd.read_csv('data/Chord_Labels1234.csv').to_numpy()
user_weights = np.ones(chords.shape[0])

current_emotion = None
curr_chord_progression = None
def get_emotion():
    """
    Grabs emotion from human state detection model
    :return int from 1 to 4:
    """
    try:
        global current_emotion
        global curr_chord_progression
        while True:
            response = doc_ref.get()
            current_emotion = None
            if response.exists:
                current_emotion = response.to_dict()['quadrant']
            curr_chord_progression = get_chord_progression()
            time.sleep(30)  # poll every 30 seconds
    except Exception as e:
        print('Error connecting to the API')



def get_chord_progression():
    """
    Grabs random chord progression given a emotion state
    :param emotion int from 1 to 4:
    :return list representation a chord progression:
    """
    global current_emotion
    global chords
    global labels
    return random.choice(chords[labels == current_emotion])



def improv_rnn_call(chord_pro):
    global current_emotion
    if current_emotion is None:
        return
    files = os.listdir(f'/home/pi/iSMuG/improv_outputs/quadrant_{current_emotion}')
    if len(files) < 18:
        config = "'chord_pitches_improv'"
        chord_pro = chord_pro * 4
        terminal_call = ['improv_rnn_generate', f'--config={config}',
                         f'--bundle_file=/home/pi/iSMuG/novel-music-generation/chord_pitches_improv.mag',
                         f'--output_dir=/home/pi/iSMuG/improv_outputs', f'--num_outputs=3',
                         f'--backing_chords={chord_pro}', f'--steps_per_chord=16', f'--render_chords']
        subprocess.run(terminal_call)
    else:
        return

def get_rand_improv_midi():
    """
    Gets a random output from improv_rnn and split to grab only the melody portion
    :return python midi object:
    """
    path = "/home/pi/iSMuG/improv_outputs/"
    files = os.listdir(path)
    midi_track = random.choice(files)
    full_path = path + midi_track
    file_name = midi_track.split('.')[0]
    melody, chords = split_tracks(full_path, file_name)
    return melody, chords

def split_tracks(file_path, file_name):
    improvrnn_output_midi = mido.MidiFile(file_path)
    tracks = []
    names = []
    for i, track in enumerate(improvrnn_output_midi.tracks):
        if i == 0:
            continue
        track_name = "/home/pi/iSMuG/split_outputs/" + file_name + '_track_' + str(i)
        output_track = mido.MidiFile()
        output_track.tracks.append(track)
        output_track.save(track_name + '.mid')
        tracks.append(track_name + '.mid')
        names.append(track_name + '.mid')

    return names[0], names[1]
    
    #only track_1 and track_2 will be relevant, ignore track_0

def performance_rnn_call(melody):
    """
    Given an emotion state and melody midi primer file, call performance_rnn
    :param melody python midi object:
    :return None:
    """
    config = "'performance_with_dynamics_and_modulo_encoding'"
    bundle_file = "/home/pi/iSMuG/performance_with_dynamics_and_modulo_encoding.mag"
    terminal_call = ['performance_rnn_generate', f'--config={config}', f'--bundle_file={bundle_file}',
                     f'--output_dir=/home/pi/iSMuG/performance_outputs', f'--num_outputs=3', f'--primer_midi={melody}']
    subprocess.run(terminal_call)

def recombine_midi():
    """
    Grabs performance rnn output and chord only midi, combine them together
    :return python midi object:
    """
    original_backing_chords = MidiFile('orig.mid', clip=True) #TODO: replace with actual file name/location
    performance_melody = MidiFile('perf.mid', clip=True) #TODO: replace with actual file name/location
    merged_mid = MidiFile(type=1)
    merged_mid.ticks_per_beat = (original_backing_chords.ticks_per_beat + performance_melody.ticks_per_beat) // 2
    melody = MidiTrack()
    chords = MidiTrack()
    chords = original_backing_chords.tracks[0].copy()
    melody = performance_melody.tracks[0].copy()
    merged_mid.tracks.append(chords)
    merged_mid.tracks.append(melody)
    merged_mid.save('full_output.mid') #TODO: replace with actual file name/location


def audio_playback_loop():
    global current_emotion
    if current_emotion is None:
        return
    path = f"/home/pi/iSMuG/improv_outputs/quadrant_{current_emotion}"
    os.chdir('/home/pi/iSMuG/novel-music-generation')
    while True:
        files = os.listdir(path)
        midi_track = random.choice(files)
        if (len(files) == 0):
            continue
        else:
            full_path = path + midi_track
            terminal_call = ['fluidsynth', '-a', 'alsa', '-n', '-i', 'YDP-GrandPiano-20160804.sf2', f'{full_path}']
            subprocess.run(terminal_call)
            os.remove(full_path)


def play_better_audio_than_arushi_2():
    terminal_call = ['fluidsynth', '-a', 'alsa', '-n', '-i', 'YDP-GrandPiano-20160804.sf2', '2022-10-30_011505_03.mid']
    os.chdir('/home/pi/iSMuG/novel-music-generation')
    subprocess.run(terminal_call)

def music_gen_loop():
    global curr_chord_progression
    while True:
        if curr_chord_progression is None:
            continue
        else:
            improv_rnn_call(curr_chord_progression)



def main():
    get_emotion_thread = threading.Thread(target=get_emotion)
    get_emotion_thread.start()

    music_gen_thread = threading.Thread(target=music_gen_loop)
    music_gen_thread.start()

    music_play_back_thread = threading.Thread(target=audio_playback_loop)
    music_play_back_thread.start()




if __name__ == "__main__":
    main()