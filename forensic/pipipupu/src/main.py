import numpy as np
from scipy.io import wavfile

row_frequencies = [697, 770, 852, 941]
col_frequencies = [1209, 1336, 1477, 1633]

keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

sample_rate = 44100
tone_duration = 0.3
pause_duration = 0.1
amplitude = 0.3


def generate_dtmf_tone(key, duration=tone_duration):
    for i, row in enumerate(keys):
        if key in row:
            row_idx = i
            col_idx = row.index(key)
            break

    row_freq = row_frequencies[row_idx]
    col_freq = col_frequencies[col_idx]
    print(key, row_freq, col_freq)

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    tone = amplitude * (np.sin(2 * np.pi * row_freq * t) + np.sin(2 * np.pi * col_freq * t))

    return tone


def generate_dtmf_sequence(sequence):
    result = np.array([])

    for key in sequence:
        tone = generate_dtmf_tone(key)

        result = np.append(result, tone)

        pause = np.zeros(int(sample_rate * pause_duration))
        result = np.append(result, pause)

    return result


def save_to_wav(audio_data, filename="pipipupu.wav"):
    audio_data = np.clip(audio_data, -1, 1)

    audio_data_int16 = (audio_data * 32767).astype(np.int16)

    wavfile.write(filename, sample_rate, audio_data_int16)

    return filename


if __name__ == "__main__":
    phone_number = "880055536361905"

    dtmf_sequence = generate_dtmf_sequence(phone_number)

    output_file = save_to_wav(dtmf_sequence)
