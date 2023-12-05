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

# q_num = 0
# llm = 'gpt-3.5-turbo-1106'
# lib = 'matplotlib'

# print(data[q_num]['question'])
# print(data[q_num]['instruction'])
# print(data[q_num][llm][lib])

# sys.exit()

st.set_page_config(
    page_title="5544",
    page_icon="📊",
    layout="wide",
)

st.title('The LLMs are on Fire in Interpreting Data​')
st.write('Please select the Question and Visualization Library of the chart.')
#Question
q_options = [data[q_num]['question'] for q_num in data]
q_option = st.selectbox('Question', q_options)
q_num = q_options.index(q_option)


#Visualization Library
lib = st.selectbox('Visualization Library', libs)


# tab1, tab2, tab3, tab4 = st.tabs(llms)

# tab1.subheader("Figure 1")
# image, script = tab1.columns(2)
# with image:
#    st.subheader("Generated Chart")
# #   selected_chart_resource = chart_resource.get(chart_type, '')
# # if selected_chart_resource:
# #     st.image(selected_chart_resource, caption=f'{chart_type.capitalize()} Chart')
# # else:
# #     st.write("Please select a chart type")
#    st.image("https://static.streamlit.io/examples/cat.jpg")

# with script:
#    st.subheader("Script Display")
#    file_path = 'main.py'  # Replace with your file path
#    with open(file_path, 'r') as file:
#     saved_code = file.read()
#     st.code(saved_code, language='python')

# tab2.subheader("Figure 1")
# tab2.write(data)


# tab3.subheader("Figure 1")
# tab3.write(data)

# tab4.subheader("Figure 1")
# tab4.write(data)

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