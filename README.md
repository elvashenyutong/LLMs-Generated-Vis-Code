# LLMs-Generated-Vis-Code
This repository contains code and data utilized for automatic data visualization using Large Language Models (LLMs) such as gpt-3.5-turbo-1106, llama-2-coder-7b, starcoder, and deepseek-coder-1.3b-instruct.

## Introduction
The objective of this project is to assess the capability of LLMs in generating visualizations from provided datasets. We evaluate their performance in adhering to instructions, generating diverse visualizations, and effectively developing code and chart images using various visualization libraries.

## Usage
- ### Setup Environment:
Ensure Python environment with required packages. Our code was tested with python version of 3.10.13.
If you want to play with all the functions (including inference LLMs), please install all dependencies by `pip install -r requirements.txt`.
Otherwise, you can simply install Streamlit to view our generated results: `pip install streamlit`.
- ### Inference LLMs (for visualization code generation):
You can decide whether to use the chatGPT API or the local models downloaded from huggingface at line 16 in [inference_LLM.py](https://github.com/elvashenyutong/LLMs-Generated-Vis-Code/blob/main/inference_LLMs.py).
If using chatGPT API, please make sure you have exported the 'OPENAI_API_KEY' to the environment variable.
If using huggingface models, please replace the value with your huggingface 'User Access Tokens' at line 12 in [inference_LLM.py](https://github.com/elvashenyutong/LLMs-Generated-Vis-Code/blob/main/inference_LLMs.py), and decide which model to use at line 54 to 57.
Then execute it by `python inference_LLMs.py`.
- ### Run Streamlit App:
Execute the Streamlit app: `streamlit run app.py`.
- ### Interact with Streamlit UI:
https://llms-generated-vis-code-3r8paqrspbzpoykzhke9cn.streamlit.app/
 - Choose the question and visualization library using the dropdowns provided.
 - View generated chart images and corresponding code snippets for each Language Model.

## Files Description
- [app.py](https://github.com/elvashenyutong/LLMs-Generated-Vis-Code/blob/main/app.py): Streamlit app for visualizing the results.
- [inference_LLM.py](https://github.com/elvashenyutong/LLMs-Generated-Vis-Code/blob/main/inference_LLMs.py): This involves summarizing a dataset and generating script pieces for data visualization.

## How to Run
- Clone the repository: `git clone https://github.com/elvashenyutong/LLMs-Generated-Vis-Code`
- Navigate to the directory: cd LLMs-Generated-Vis-Code
- Or download the package of the code
- Install dependencies: `pip install streamlit` or `pip install -r requirements.txt` for full test
- Run LLMs inference: `python inference_LLMs.py`
- Run the Streamlit app: `python -m streamlit run app.py`
- After executing the Streamlit app, it will create a local website
- OR you can simply access this [URL](https://llms-generated-vis-code-3r8paqrspbzpoykzhke9cn.streamlit.app/) to view what we have achieved.


## Dependencies
Python 3.10+
Streamlit
Other dependencies are listed in [requirements.txt](https://github.com/elvashenyutong/LLMs-Generated-Vis-Code/blob/main/requirements.py)

## Acknowledgments
The project utilized data and models from various sources, acknowledging their contributions.
