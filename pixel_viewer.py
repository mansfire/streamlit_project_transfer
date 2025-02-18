import sys
import numpy as np
$ conda activate pixelexplorer
$ pip install matplotlib
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# decide what matplotlib backend to use depending on system


import os.path
import os
import tifffile as tif
import pandas as pd
from skimage.segmentation import find_boundaries
from skimage.measure import label
import random
import pickle
from sklearn.mixture import GaussianMixture
from scipy.stats import norm
import datetime
import time
import streamlit as st


# read in the data location
assert len(sys.argv) == 2, "Please pass data location as the only argument."
data_dir = sys.argv[1]
assert os.path.exists(data_dir), f"Directory {data_dir} does not exist."
assert os.path.exists(os.path.join(data_dir, "slides")), "Please organize data as: data_folder/slides"
assert os.path.exists(os.path.join(data_dir, "channel_names.csv")), "Please include a file called `channel_names.csv` in data folder."

# open the files
slides = {}
for f in sorted(os.listdir(os.path.join(data_dir, "slides"))):
    name = f.split(".")[0]
    slides[name] = tif.TiffFile(os.path.join(data_dir, "slides", f))
    print(f"Opened {name} has shape {slides[name].series[0].shape}")
    # slides[f.split(".")[0]] = zarr.open(tif.imread(os.path.join(data_dir, "slides", f), aszarr=True))
slides_key_list = list(slides.keys())
# open channel names
channel_names = list(pd.read_csv(os.path.join(data_dir, "channel_names.csv"))["marker_name"])
print("Using channel names: ", channel_names)
# assert len(channel_names) == slides[slides_key_list[0]].series[0].shape[0], f"Channel names length {len(channel_names)} doesnt match slide shape {slides[slides_key_list[0]].series[0].shape[0]}"

# initialize session state

if 'cur_samples' not in st.session_state:
    st.session_state.cur_samples = []
if 'plot_x_range' not in st.session_state:
    st.session_state.plot_x_range = [0, 2**16]
if 'use_log_y' not in st.session_state:
    st.session_state.use_log_y = False
if 'use_density' not in st.session_state:
    st.session_state.use_density = False
if 'threshold_value' not in st.session_state:
    st.session_state.threshold_value = None
if 'above_threshold' not in st.session_state:
    st.session_state.above_threshold = True
if 'cur_data' not in st.session_state:
    st.session_state.cur_data = None
if 'gmm_data' not in st.session_state:
    st.session_state.gmm_data = None
if 'num_bins' not in st.session_state:
    st.session_state.num_bins = 50
if 'transform' not in st.session_state:
    st.session_state.transform = ""

#define functionality 
def select_all_samples():
    st.session_state.cur_samples = slides_key_list

def deselect_all_samples():
    st.session_state.cur_samples = []
    

# Placeholder for plot and plot variable
subsample = 1
lower_threshold = 0
higher_threshold = 10000
plot_placeholder = st.empty()

st.image(image="logo_small.png", caption="Predx Logo",clamp=False, channels="RGB", output_format="auto")
  
st.write("")
#sg.Text("", size=(10,6))
# Inject the custom CSS
button_css = """
<style>
    .stButton > button {
        font-size: 24px;
        padding: 15px 32px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        margin: 5px;
    }
</style>
"""

st.markdown(button_css, unsafe_allow_html=True)

# Threshold value
st.session_state.threshold_value_input = st.number_input("Threshold Value", value=st.session_state.threshold_value or 0.0, on_change=update_threshold)

# Sample list
cur_samples = st.multiselect("Sample List", slides_key_list, default=st.session_state.cur_samples, on_change=update_samples, key='cur_samples')




       
st.button(label='Select All', on_click=select_all_samples)
st.button(label='Deselect All', on_click=deselect_all_samples)
#sg.Text("", size=(10, 1), font=("Arial Bold", 16)),
#sg.Button("Select All", key="-SELECT-ALL-"),
#sg.Button("Deselect All", key="-DESELECT-ALL-"),




