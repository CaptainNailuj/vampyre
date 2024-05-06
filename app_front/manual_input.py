import streamlit as st
from itertools import chain
import pandas as pd
import json
import os

def get_classification(trait):
    classification_list = [classification for classification in dict_trait_lists if trait in dict_trait_lists[classification]]
    return classification_list[0] if classification_list else 'weird'


def get_index(trait):
    classification = get_classification(trait)
    idx = dict_trait_lists.get(classification, [trait]).index(trait)
    return idx



path_levels = "../util_files/level_trais.json"
path_base_attributes = "../util_files/base_attributes.json"
path_base_abilities = "../util_files/base_abilities.json"


dict_levels = json.load(open(path_levels))

dict_attributes = json.load(open(path_base_attributes))
attributes = list(chain.from_iterable([list(dict_attributes[key].keys()) for key in dict_attributes]))

dict_abilities = json.load(open(path_base_abilities))
abilities = list(chain.from_iterable([list(dict_abilities[key].keys()) for key in dict_abilities]))

other_traits = ['willpower', 'blood pool']
dict_trait_lists = {'ability': abilities, 'attribute': attributes, 'other': other_traits} 



st.sidebar.image("../util_files/Images/vampire_theme_image.jpeg", use_column_width=True)
st.sidebar.title("Darkness Brooder:\nFill information manually")

level_name = st.sidebar.selectbox('Level Name', dict_levels.keys(), index=0)
trait_list = list(set(dict_levels[level_name]))

st.write(trait_list)
buttons = ['']*len(trait_list)
for i, trait in enumerate(trait_list):
    # if i != 0:
    #     continue
    classification = get_classification(trait)
    idx = get_index(trait)
    
    action = st.sidebar.selectbox(f'Action for trait {i}', ['keep', 'modify', 'delete'], index=0)
    if action=='modify':
        trait_list[i] = st.sidebar.selectbox(f'{classification} {i}', abilities + attributes + other_traits)    
    elif action=='delete':
        del trait_list[i]
    
st.write(trait_list)