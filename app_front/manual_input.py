import streamlit as st
from itertools import chain
import pandas as pd
import json
import os
from datetime import datetime

def get_classification(trait):
    classification_list = [classification for classification in dict_trait_lists if trait in dict_trait_lists[classification]]
    return classification_list[0] if classification_list else 'weird'


def get_index(trait):
    classification = get_classification(trait)
    idx = dict_trait_lists.get(classification, [trait]).index(trait)
    return idx


if st.button('Reset Session State'):
    st.session_state.clear()
    st.experimental_rerun()  


path_levels = "/home/julian/Documents/Projects/vampyre/util_files/level_trais.json"
path_base_attributes = "/home/julian/Documents/Projects/vampyre/util_files/base_attributes.json"
path_base_abilities = "/home/julian/Documents/Projects/vampyre/util_files/base_abilities.json"
path_complete_levels = "/home/julian/Documents/Projects/vampyre/util_files/complete_level_traits.json"
path_save_complete_levels = "/home/julian/Documents/Projects/vampyre/util_files/level_traits/complete_level_traits_{}.json"


dict_levels = json.load(open(path_levels))

if 'dict_complete_levels' not in st.session_state:
    st.session_state['dict_complete_levels'] = json.load(open(path_complete_levels))


dict_attributes = json.load(open(path_base_attributes))
attributes = list(chain.from_iterable([list(dict_attributes[key].keys()) for key in dict_attributes]))
dict_abilities = json.load(open(path_base_abilities))
abilities = list(chain.from_iterable([list(dict_abilities[key].keys()) for key in dict_abilities]))



other_traits = ['willpower', 'blood pool']
dict_trait_lists = {'ability': abilities, 'attribute': attributes, 'other': other_traits} 
complete_traits_list = abilities + attributes + other_traits

st.sidebar.image("/home/julian/Documents/Projects/vampyre/util_files//Images/vampire_theme_image.jpeg", use_column_width=True)
st.sidebar.title("Darkness Brooder:\nFill information manually")

level_name = st.sidebar.selectbox('Level Name', dict_levels.keys(), index=0)
current_trait_list = list(set(dict_levels[level_name]))

st.write(current_trait_list)
traits_num = len(current_trait_list)
if not current_trait_list:
    extinction_list = complete_traits_list.copy()
    traits_num = int(st.sidebar.text_input(f"There are no traits related to {level_name}. How many field do you wish to insert?", 
                                           value=0))
    current_trait_list = ['None']*traits_num
else:
    traits_num = int(st.sidebar.text_input(f"Current numbers of traits for {level_name}.", 
                                           value=traits_num))
    current_trait_list = current_trait_list + [complete_traits_list[0]]*(traits_num - len(current_trait_list))

for i in range(traits_num):
    idx = get_index(current_trait_list[i])
    current_trait_list[i] = st.sidebar.selectbox(f"Pick {i+1} trait", complete_traits_list, index=idx)


new_level_traits = {level_name: current_trait_list}
st.write(f"New element")
st.write(new_level_traits)

modify = st.sidebar.button("Modify")
save = st.sidebar.button("Save")

if modify:
    st.session_state.dict_complete_levels.update(new_level_traits)

if save:
    today = datetime.now().strftime("%Y%m%d_%H-%M")
    path_saving_levels = path_save_complete_levels.format('')
    json.dump(st.session_state.dict_complete_levels, open(path_saving_levels, 'w'))