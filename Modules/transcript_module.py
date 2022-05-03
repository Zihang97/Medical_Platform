import deepspeech
import wave
import numpy as np

model_file_path = 'deepspeech/deepspeech-0.9.3-models.pbmm'
# file1 = '../static/file_buffer/2830-3980-0043.wav'

def translator(filename, model_file_path=model_file_path):
    model = deepspeech.Model(model_file_path)
    with wave.open(filename, 'r') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    text = model.stt(data16)

    return text
