import nd2
import os
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
# package for io
from aicsimageio import AICSImage
from aicsimageio.writers import OmeTiffWriter

# function for core algorithm
from aicssegmentation.core.vessel import filament_2d_wrapper
from aicssegmentation.core.pre_processing_utils import intensity_normalization, image_smoothing_gaussian_3d, edge_preserving_smoothing_3d
from skimage.morphology import remove_small_objects     # function for post-processing (size filter)




list_of_files = list(os.listdir('/Users/dadua2/Projects/DAPISegmentation/cellPaintingAnnotation/VeronicaProjectLimited'))
fl = st.selectbox("Select file", [i for i in list_of_files if 'raw' in i])
fname1 = "/Users/dadua2/Projects/DAPISegmentation/cellPaintingAnnotation/VeronicaProjectLimited" + "/" + fl
# "'/ACS_neurites_norm_Pt-5_CSU-488_20240913_094939_873__WellF11_ChannelCSU 405,CSU 488,CSU 640_Seq0039.png'
 # 'forFaraz/20240913_094939_873__WellC10_ChannelCSU 405,CSU 488,CSU 640_Seq0007_C10_0003_RGB_CSU 488.tif'
# FILE_NAME = 'forFaraz/20240913_094939_873__WellC10_ChannelCSU 405,CSU 488,CSU 640_Seq0007_C10_0003_RGB_CSU 640.tif'

FILE_NAME = fname1
reader = AICSImage(FILE_NAME)
# IMG = my_array[4, 1, :, :] # reader.data[0,0,0,:,:,0]
IMG = plt.imread(fname1)

st.write(IMG.shape)


intensity_scaling_param = [2.5, 7.5]
struct_img = intensity_normalization(IMG, scaling_param=intensity_scaling_param)

# @st.cache_data
def f(name, i, j):
    if os.path.exists(f"{name}_{i}_{j}.png"):
        return f"{name}_{i}_{j}.png"
    else:
        f2_param = [[i, j]]
        # f2_param = [[1, 0.15]]

        bw = filament_2d_wrapper(struct_img, f2_param)
        fig, (ax, ax3) = plt.subplots(1, 2, figsize=(12,16), dpi=72, facecolor='w', edgecolor='k')
        ax.imshow(IMG, cmap=plt.cm.gray)
        # ax2.imshow(struct_img, cmap=plt.cm.gray)
        ax3.imshow(bw, cmap=plt.cm.gray)
        ax.axis('off')
        # ax2.axis('off')
        ax3.axis('off')
        ax.set_title("raw")
        # ax2.set_title("normalized")
        ax3.set_title(f"segmented ({i}, {j})")
        fig.savefig(f"{name}_{i}_{j}.png", bbox_inches='tight')
        return f"{name}_{i}_{j}.png"


        # plt.show()

i = st.slider("Thickness", min_value=1, max_value=25, step=3)
j = st.slider("Cutoff", min_value=0.15, max_value=0.60, step=0.15)
figname = f(fl.split('__Well')[-1].split('_')[0], i, j)
st.pyplot(figname)