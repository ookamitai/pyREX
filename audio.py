import numpy as np
import math

def apply_fadeout(audio, sr, duration):
    # convert to audio indices (samples)
    audio = np.array(audio)
    length = int(duration/1000*sr)
    end = audio.shape[0]
    start = end - length

    # compute fade out curve
    # linear fade
    fade_curve = np.linspace(1.0, 0.0, length)

    # apply the curve
    audio[start:end] = audio[start:end] * fade_curve
    audio = np.ndarray.tolist(audio)
    return audio

def apply_fadein(audio, sr, duration):
    # convert to audio indices (samples)
    audio = np.array(audio)
    length = int(duration/1000*sr)
    start = 0
    end = length

    # compute fade out curve
    # linear fade
    fade_curve = np.linspace(0.0, 1.0, length)

    # apply the curve
    audio[start:end] = audio[start:end] * fade_curve
    audio = np.ndarray.tolist(audio)
    return audio

def normalize(sig, rms_level=0):
    """
    Normalize the signal given a certain technique (peak or rms).
    Args:
        - infile    (str) : input filename/path.
        - rms_level (int) : rms level in dB.
    """
    # read input file

    # linear rms level and scaling factor
    r = 10**(rms_level / 10.0)
    a = np.sqrt( (len(sig) * r**2) / np.sum(sig**2) )

    # normalize
    y = sig * a

    return y
