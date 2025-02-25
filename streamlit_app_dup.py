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
st.set_page_config(layout="wide")

root_folder = "Visualization_DAPI"

marker_set = os.listdir(root_folder)
# col3.title("DAPI Segmented Image")
# col4.title("DAPI Raw Image")

mset = st.selectbox("Select marker set", marker_set)


image_path_list = []
actual_path_list = []
all_image_path_list = []
for msett in marker_set:
    list_of_image_folders = os.listdir(root_folder  + "/" + msett)
    for img_folder in list_of_image_folders[:20]:
        fullpath = root_folder  + "/" + msett + "/" + img_folder
        all_image_path_list.append(fullpath + '/actualImage.png')
        if mset == msett:
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
        col3, col4 = st.columns([1, 2])
        col3.header("Dapi segmented image")
        col4.header("Dapi raw image")
        target_image_path = image_path_list[num_page]
        col3.image(actual_path_list[num_page])
        with col4:
            new_labels = detection(image_path=target_image_path, 
                                bboxes=st.session_state['result_dict'][target_image_path]['bboxes'], 
                                labels=st.session_state['result_dict'][target_image_path]['labels'], 
                                label_list=label_list, use_space=True, key=target_image_path)
            if new_labels is not None:
                st.session_state['result_dict'][target_image_path]['bboxes'] = [v['bbox'] for v in new_labels]
                st.session_state['result_dict'][target_image_path]['labels'] = [v['label_id'] for v in new_labels]


            with open("result_dict.json", "r") as outfile: 
                result_dict_exist = json.load(outfile)
            
            if not json.dumps(result_dict_exist) == json.dumps(st.session_state['result_dict']):
                # Convert and write JSON object to file
                with open("result_dict.json", "w") as outfile: 
                    json.dump(st.session_state['result_dict'], outfile)

    
    # st.json(st.session_state['result_dict'])