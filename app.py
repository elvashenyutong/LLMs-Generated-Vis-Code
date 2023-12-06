import streamlit as st
import pandas as pd

import os, sys
import json

data_folder_path = './final'
llms = ['gpt-3.5-turbo-1106', 'llama-2-coder-7b', 'starcoder', 'deepseek-coder-1.3b-instruct']
libs = ['matplotlib', 'seaborn', 'plotly', 'ggplot']

data = dict()
for llm in llms:
  with open(os.path.join(data_folder_path, llm, f'{llm}_{llm}_result.json'), 'r') as fr:
    results = json.load(fr)
  questions = results['visualizations']
  for q in questions:
    q_num = q['index']
    if q_num not in data:
      data[q_num] = {
          'question': q['question'],
          'instruction': q['visualization'],
          'rationale': q['rationale']
      }
    data[q_num][llm] = q['charts']

st.set_page_config(
    page_title="5544",
    page_icon="📊",
    layout="wide",
)

st.title('The LLMs are on Fire in Interpreting Data​')
st.write('Please select the Question and Visualization Library of the chart.')

q_options = [data[q_num]['question'] for q_num in data]
q_option = st.selectbox('Question', q_options)
q_num = q_options.index(q_option)

lib = st.selectbox('Visualization Library', libs)

instruction = data[q_num]['instruction']

st.header('LLMs Generated Code')
st.subheader(f'Instruction: {instruction}')
llm_tabs = st.tabs(llms)

for i, llm_tab in enumerate(llm_tabs):
    # print(q_num, llm, lib)
    llm = llms[i]
    llm_output = data[q_num][llm][lib]
    # image, script = llm_tab.columns(2)
    if len(llm_output) == 0:
       llm_tab.image('./Image_not_available.png')
    else:
        for output in llm_output:
            image, script = llm_tab.columns(2)
            with image:
                st.subheader("Generated Chart")
                image_path = os.path.join(data_folder_path, llm, output['image'])
                st.image(image_path)

            with script:
                st.subheader("Script Display")
                saved_code = output['code']
                st.code(saved_code, language='python')