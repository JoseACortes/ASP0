#data
####
data = '../../bigdata/'
#data =  '../../../Data/bigdata/'
drumfolder = data+'drums/'
guitarfolder = data+'guitar/'


import os
import matplotlib.pyplot as plt
import numpy as np

drumfilelist = []
for filename in os.listdir(drumfolder):
    f = os.path.join(drumfolder, filename)
    # checking if it is a file
    if os.path.isfile(f):
        drumfilelist.append(f)
        
guitarfilelist = []
for filename in os.listdir(guitarfolder):
    f = os.path.join(guitarfolder, filename)
    # checking if it is a file
    if os.path.isfile(f):
        guitarfilelist.append(f)


from pydub import AudioSegment

drums = []
for f in drumfilelist:
    drums.append(AudioSegment.from_wav(f))

guitar = []
for f in guitarfilelist:
    guitar.append(AudioSegment.from_wav(f))



from pydub import scipy_effects
from pydub import effects


def showspec(sound):
    plt.figure(figsize = (15,5))
    plt.specgram(sound.get_array_of_samples())
    plt.show()

#data generators

def mixing_generic(a, b):
    a.overlay(b)

def mixing_parameters_generic(a, b, aset, bset):
    return aset[a].overlay(bset[b])

def mixing_parameters_0(a, b):
    return mixing_parameters_generic(a, b, guitar, drums)

def oga(a):
    return guitar[a]

def ogb(b):
    return drums[b]

###
def filter_parameters(audio, l = 0.01, u = 22049.99):
    #(0, 22050)
    return scipy_effects.band_pass_filter(audio, l, u)


###
def compare_generic(de_mix, og_stem):
    return np.abs(np.average(de_mix.overlay(og_stem.invert_phase()).get_array_of_samples()))

def comparison_parameters_0(audio, a):
    return compare_generic(audio, guitar[a])

def correlation_generic(de_mix, og_stem):
    return np.correlate(de_mix.get_array_of_samples(), og_stem.get_array_of_samples())[0]

def correlation_parameters_0(audio, a):
    return correlation_generic(audio, guitar[a])

def sdr_generic(de_mix, og_stem):
    s_ = de_mix.get_array_of_samples()
    s = og_stem.get_array_of_samples()
    return 10*np.log10((np.sum(np.square(s)))/(np.sum(np.square(np.subtract(s,s_)))))

def sdr_parameters_0(audio, a):
    return sdr_generic(audio, guitar[a])
###

###
def scan_opt_sdr_0(a, b, res = 10, disp = False):
    mount = []
    eall = [-10000, -10000]
    _max = [np.exp(0), np.exp(10)]
    r = np.linspace(1, 10, res)
    _r = len(r)
    for _l, l in enumerate(r):
        m = []
        for _ in r[:_l]:
            m.append(np.nan)
        for u in r[_l:]:
            _eval = sdr_parameters_0(filter_parameters(mixing_parameters_0(a, b), np.exp(l), np.exp(u)), a)
            if _eval > np.amax(eall):
                _max = [np.exp(l), np.exp(u)]
            eall.append(_eval)
            m.append(_eval)
        mount.append(m)
    if disp == True:
        plt.figure(figsize = (10, 10))
        plt.imshow(mount)
        plt.colorbar()
        plt.show()
    return np.array(_max)

def optimize_this_sdr_0(outpar, a, b):
    l, u = outpar
    return -sdr_parameters_0(filter_parameters(mixing_parameters_0(a, b), l, u), a)

import scipy.optimize as opt

def optimize_sdr_0(start, args, disp = False):
    start = (start[0], start[1])
    return opt.fmin(optimize_this_sdr_0, start, args = args, disp = disp)

def superoptimize_sdr_0(a, b, res = 10, disp = False):
    return optimize_sdr_0(scan_opt_sdr_0(a, b, disp = disp, res=res), (a, b), disp = disp)