import streamlit as st
from glob import glob
import pandas as pd
import streamlit as st
from streamlit_image_annotation import classification
import os
from pathlib import Path
import streamlit as st
from glob import glob
import pickle 
from streamlit_image_annotation import detection
import json
# st.set_page_config(layout="wide")

root_folder = "Visualization_DAPI_INSPECTION"
root_folder = "Dec29_60X_OME-TIFFs_Visualization_DAPI_INSPECTION"

marker_set = os.listdir(root_folder)
# col3.title("DAPI Segmented Image")
# col4.title("DAPI Raw Image")

indipl = """INDI00002D
INDI00003D
INDI00005D
INDI00006D
INDI00008D
INDI00009D
INDI00010D
INDI00011D
INDI00019D
INDI00012D
INDI00013D
INDI00014D
INDI00015D
INDI00016D
INDI00017D
INDI00018D"""

selectedplate = st.selectbox("Select plate", indipl.split("\n")) # ["INDI00003D", "INDI00004D", "INDI00005D", "INDI00007D"]


# mset = st.selectbox("Select marker set", marker_set)


image_path_list = []
actual_path_list = []
all_image_path_list = []
for msett in marker_set:
    list_of_image_folders = os.listdir(root_folder  + "/" + msett)
    for img_folder in list_of_image_folders: # [:20]:
        fullpath = root_folder  + "/" + msett + "/" + img_folder
        if selectedplate in fullpath:
            all_image_path_list.append(fullpath + '/actualImage.png')
        if selectedplate in fullpath:
            image_path_list.append(fullpath + '/actualImage.png')
            actual_path_list.append(fullpath + '/segmentedImage.png')



if True:
    label_list = ['deer', 'human', 'dog', 'penguin', 'framingo', 'teddy bear']
    label_list = ['FP', 'TP', 'FN', 'TN']
    # image_path_list = glob('image/*.jpg')
    if 'result_dict' not in st.session_state:
        result_dict = {}
        for img in all_image_path_list:
            # result_dict[img] = {'bboxes': [[0,0,100,100],[10,20,50,150]],'labels':[0,3]}
            result_dict[img] = {'bboxes': [],'labels':[]}
        
        if os.path.exists("result_dict.json"):
            with open("result_dict.json", "r") as outfile: 
                result_dict = json.load(outfile)
        else:
            with open("result_dict.json", "w") as outfile: 
                json.dump(result_dict, outfile)



        st.session_state['result_dict'] = result_dict.copy()
        

    num_page = st.slider('page', 0, len(image_path_list)-1, 0, key='slider')
    # for num_page, img_folder in enumerate(list_of_image_folders):
    if True:
        col3, col4 = st.columns([1, 1])
        col4.write("Dapi segmented image")
        col3.write(os.path.basename(Path(actual_path_list[num_page]).parent))
        target_image_path = image_path_list[num_page]
        col4.image(actual_path_list[num_page])
        col3.image(image_path_list[num_page])

    
    # st.json(st.session_state['result_dict'])