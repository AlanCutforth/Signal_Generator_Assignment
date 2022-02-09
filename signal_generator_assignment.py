##############################################################################
# This piece of code simulates a physical laboratory signal generator as per
# the assignment.
##############################################################################

import matplotlib.pyplot as plt
import matplotlib.widgets as ws
import numpy as np
from scipy import signal
import random as rnd_no

# Default conditions
tmax = 1
a = 1
f = 1
stop = False
smple_pts = 100
phase = 0
wavetype = 'Sine'
window_width = tmax
window_start = 0
noise = 0
smple_pts_intrans = smple_pts

# Checks to see which radio button is selected, and generates the corresponding signal
def signalg(s_a, s_f, s_t, p, s_n=0):    
    if wavetype == 'Sine':
        signal_output = s_a*np.sin(2*np.pi*s_f*s_t + p)
    elif wavetype == 'Sawtooth':
        signal_output = s_a*signal.sawtooth(2*np.pi*s_f*s_t + p)
    else:
        signal_output = s_a*signal.square(2*np.pi*s_f*s_t + p)
       
    # Adds the noise values to the signal, providing a noise array is passed into this function
    if s_n != 0:
        for i in range(0, len(signal_output)):
            signal_output[i] += s_n[i]
       
    return signal_output

# Generates an array of random numbers that will be applied to the signal as noise,
# multiplied by the noise intensity which will be between 0 and 1
def gen_noise_array(n):
    noise_arr = []
    
    for i in range(0, len(t)):
        noise_arr.append(rnd_no.uniform(-1,1)*n)
        
    return noise_arr

# Changes frequency using slider
def sliderCallback_f(val):
    global f
    f = val
    update_signal()

# Changes timespan using slider
def sliderCallback_t(val):
    global tmax
    tmax = val
    reset_time()

# Changes the number of sample points using slider
def sliderCallback_s(val):
    global smple_pts
    smple_pts = int(val)
    reset_time()
   
# Resets the time linspace with new values for either or both of tmax and sample points
def reset_time():
    global t
    t_n = np.linspace(0, tmax, smple_pts)
    t = t_n
    update_signal()

# Changes the phase using slider    
def sliderCallback_p(val):
    global phase
    phase = val
    update_signal()
   
# Changes the noise intensity using slider
def sliderCallback_n(val):
    global noise
    global rseed
    noise = gen_noise_array(val)
    update_signal()
    
# Changes the width of the window using slider
def sliderCallback_w(val):
    global window_width
    window_width = val*(tmax - window_start)
    update_signal()
   
# Changes the starting position of the window using slider
def sliderCallback_lw(val):
    global window_start
    window_start = val*tmax
    update_signal()
       
# Changes the waveform type using the radio buttons
def wavefunc_type(label):
    global wavetype
    wavetype = label
    update_signal()

# Redraws the graphs with new parameters
def update_signal():
    global window_start
    global window_width
    
    # Redefines axes
    ax.set_xlim([0, tmax])
    axf.set_xlim([0, smple_pts/(2*tmax)])
   
    plotsignal = signalg(a, f, t, phase, noise)
   
    # Updates data for the two plots, and then for the two window lines
    axesHandle.set_data(t, plotsignal)
    f_tran = fourier_transform(plotsignal)
    axesHandle_f.set_data(k_transform(), f_tran)
   
    axesHandle_lw.set_data([window_start, window_start], [-2, 2])
    axesHandle_w.set_data([window_start+window_width, window_start+window_width], [-2, 2])
   
    windowlabel.set_text('Window from ' + str(np.round_(window_start, 2)) + ' to ' + str(np.round_(window_start+window_width, 2)) + '.')
   
    ax.draw()
    axf.draw()

# Returns the fourier transformed signal
def fourier_transform(plotsignal=signalg(a, f, np.linspace(window_start, window_start+window_width, smple_pts), phase)):
    window_sig = []
    global smple_pts_intrans
   
    # Takes the signal elements from inside the winidow and applies the fourier transform to them
    for i in range(0, len(plotsignal)):
        if t[i] >= window_start and t[i] <= window_start + window_width:
            window_sig.append(plotsignal[i])
    smple_pts_intrans = len(window_sig)
    fourier_t = np.fft.fft(window_sig)

    return fourier_t*np.conj(fourier_t)/smple_pts_intrans

# Returns the k-space x-axis data for the fourier plot
def k_transform():
    return np.linspace(window_start, smple_pts_intrans/(2*(window_start+window_width)), smple_pts_intrans)

# Closes the program using the close button
def closeCallback(event):
    global stop
    stop = True

# Sets up axes for graph and widgets, inputs initial conditions and plots the
# initial graphs
fig, (ax, axf) = plt.subplots(1, 2, figsize=(14,5))
plt.subplots_adjust(left=0.2, right=0.7, bottom=0.4)

t = np.linspace(0, tmax, smple_pts)
axesHandle, = ax.plot(t, signalg(a, f, t, phase), lw=2, color='red')
ax.set_xlim([0, tmax])
ax.set_ylabel('Frequency')
ax.set_xlabel('Time')
ax.set_title('Waveform')

axesHandle_f, = axf.plot(k_transform(), fourier_transform())
axf.set_ylabel('Fourier Transform')
axf.set_xlabel('Frequency')
axf.set_title('Fast Fourier Transformed Waveform')

axesHandle_lw, = ax.plot([0, 0],[-1, 1])
axesHandle_w, = ax.plot([tmax, tmax],[-1, 1])

slider_fax = plt.axes([0.2, 0.06, 0.6, 0.03])
sliderHandle_f = ws.Slider(slider_fax, 'Frequency', 1, 300.0, valinit=1.0)

slider_tax = plt.axes([0.2, 0.11, 0.6, 0.03])
sliderHandle_t = ws.Slider(slider_tax, 'Time', 1, 300.0, valinit=1.0)

slider_sax = plt.axes([0.2, 0.16, 0.6, 0.03])
sliderHandle_s = ws.Slider(slider_sax, 'Number of Points', 2, 300.0, valinit=100.0, valfmt='%0.0f')

slider_pax = plt.axes([0.2, 0.21, 0.6, 0.03])
sliderHandle_p = ws.Slider(slider_pax, 'Phase', 0, 2*np.pi, valinit=0.0)

slider_lwax = plt.axes([0.02, 0.3, 0.03, 0.6])
sliderHandle_lw = ws.Slider(slider_lwax, 'Window Start', 0, 1, valinit=0.0, orientation='vertical')

slider_wwax = plt.axes([0.1, 0.3, 0.03, 0.6])
sliderHandle_w = ws.Slider(slider_wwax, 'Window Width', 0, 1, valinit=1.0, orientation='vertical')

slider_nax = plt.axes([0.2, 0.01, 0.6, 0.03])
sliderHandle_n = ws.Slider(slider_nax, 'Noise', 0, 1, valinit=0.0)

rax = plt.axes([0.75, 0.4, 0.2, 0.3])
radioHandle = ws.RadioButtons(rax, ('Sine', 'Square', 'Sawtooth'))

btn_ax = plt.axes([0.8, 0.75, 0.1, 0.1])
buttonHandle = ws.Button(btn_ax, 'Close')

windowlabel = plt.text(-7.7, -5.2, 'Window from ' + str(window_start) + ' to ' + str(window_start+window_width) + '.')

while stop == False:
    # Activates callbacks for ui elements
    sliderHandle_f.on_changed(sliderCallback_f)
    sliderHandle_t.on_changed(sliderCallback_t)
    sliderHandle_s.on_changed(sliderCallback_s)
    sliderHandle_p.on_changed(sliderCallback_p)
    sliderHandle_w.on_changed(sliderCallback_w)
    sliderHandle_lw.on_changed(sliderCallback_lw)
    sliderHandle_n.on_changed(sliderCallback_n)
    radioHandle.on_clicked(wavefunc_type)
    buttonHandle.on_clicked(closeCallback)
    plt.pause(1)
    if stop == True:
        print("Stopping...")
   
plt.close('all')