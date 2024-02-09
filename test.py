import numpy as np
import pyaudio
import tensorflow as tf
import tensorflow_hub as hub
import time
import csv
import os
import json
from datetime import datetime

model = hub.load('https://tfhub.dev/google/yamnet/1')
class_map_path = model.class_map_path().numpy()
class_names = [row['display_name'] for row in csv.DictReader(open(class_map_path))]

def classify_audio(audio_data):
    # Converte i dati audio in float32 che YAMNet si aspetta
    audio_data = audio_data / 32768.0
    # Esegue la classificazione con YAMNet
    scores, embeddings, spectrogram = model(audio_data)
    # Calcola le percentuali
    mean_scores = np.mean(scores, axis=0)
    top5 = np.argsort(mean_scores)[::-1][:5]
    os.system('cls')
    print("5 Classi più probabili:")
    dict_top5 = {}
    for i in top5:
        print(f"{class_names[i]}: {mean_scores[i] * 100:.2f}%")
        dict_top5 [f"{class_names[i]}"] = f"{mean_scores[i] * 100:.2f}%"
    salva(dict_top5)

def salva(dati):
    if(not os.path.exists("test.json")):
        pattern ={
            "rilevazioni": [
            ]
        }
        with open("test.json", 'w') as file:
            json.dump(pattern, file, indent=4)
    with open('test.json', 'r') as file:
        data = json.load(file)
    item = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "valori": dati
    }
    ora = {datetime.now().strftime("%Y-%m-%d") :[
        ]
    }
    if(not any(datetime.now().strftime("%Y-%m-%d") in giorno for giorno in data['rilevazioni'])):
        data["rilevazioni"].append(ora)
    for giorno in data["rilevazioni"]:
        if datetime.now().strftime("%Y-%m-%d") in giorno:
            giorno[datetime.now().strftime("%Y-%m-%d")].append(item)
            break
    with open('test.json', 'w') as file:
        json.dump(data, file, indent=4)

def callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    classify_audio(audio_data)
    return (None, pyaudio.paContinue)

p = pyaudio.PyAudio()
n = 5
# Apri lo stream audio
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=int(16000*n), stream_callback=callback)

print("Inizio cattura e classificazione audio.")
stream.start_stream()

try:
    while stream.is_active():
        time.sleep(0.1)
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Finito.")
