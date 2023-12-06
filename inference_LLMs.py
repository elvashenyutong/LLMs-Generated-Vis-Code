from lida import Manager, TextGenerationConfig , llm  
from dotenv import load_dotenv
import os
import json
import openai
import base64
from PIL import Image
from io import BytesIO
from huggingface_hub import login


login("hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")  # Please replace the value with you huggingface 'User Access Tokens'.
                                                # Visit https://huggingface.co/docs/hub/security-tokens for tails.
load_dotenv()

using_chatgpt = True  # You can decide whether to use the chatGPT API or the local models download from huggingface.
                       # If using chatGPT API, please make sure you have exported the 'OPENAI_API_KEY' to the environment variable.

def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

def save_image(base64_str, save_path):
    img = base64_to_image(base64_str)
    img.save(save_path)
    print(f"Image saved at {save_path}")

if using_chatgpt == True:
    openai.api_key = os.getenv('OPENAI_API_KEY')
    lm = 'gpt-3.5-turbo-1106'
    code_lm = 'gpt-3.5-turbo-1106'
    text_gen = llm("openai")
else:
    ## too small, not able to generate proper results in this work.
    # lm = 'meta-llama/Llama-2-7b-chat-hf'  # too small
    # lm = 'meta-llama/Llama-2-7b-hf'  # too small

    ## OOM
    # lm = 'codellama/CodeLlama-13b-Python-hf'  # OOM
    # lm = 'TheBloke/CodeLlama-13B-Python-fp16'  # OOM
    # lm = 'deepseek-ai/deepseek-coder-6.7b-instruct'  # OOM
    # lm = 'codellama/CodeLlama-7b-Instruct-hf'  # OOM
    # lm = 'meta-llama/Llama-2-70b-chat-hf'  # OOM
    # lm = 'togethercomputer/Llama-2-7B-32K-Instruct'  # OOM
    # lm = 'codellama/CodeLlama-7b-Python-hf'  # OOM

    ## other bugs
    # lm = 'microsoft/codebert-base'  # bug

    ## works
    ## You can decide which language model to use. The three models below were used in our demo.
    lm = 'deepseek-ai/deepseek-coder-1.3b-instruct'  # works
    # lm = 'bigcode/starcoder'  # some work
    # lm = 'mrm8488/llama-2-coder-7b'  # probably works
    
    code_lm = lm
    text_gen = llm(provider="hf", model=lm, device_map="auto")

lida = Manager(text_gen = text_gen) 

print("Model Loaded Successfully!")


textgen_config = TextGenerationConfig(n=1, temperature=0.5, model=lm, use_cache=True)
try:
    summary = lida.summarize("netflix_titles.csv", summary_method="llm", textgen_config=textgen_config)
except:
    summary = lida.summarize("netflix_titles.csv", summary_method="default", textgen_config=textgen_config)


visual_libraries = ['matplotlib', 'seaborn', 'plotly', 'ggplot']


persona = 'An experienced film critic who recommends movies based on current trends.'
persona_goals = [
    {
        "question": "Which countries produce the most content available on Netflix?",
        "visualization": "bar chart of top 10 countries",
        "rationale": "By visualizing the top 10 countries that produce content available on Netflix, the film critic can identify the countries with the most content and recommend movies based on the current trends in production.",
        "index": 0
    },
    {
        "question": 'What is the distribution of ratings for shows and movies on Netflix?',
        "visualization": 'bar chart of rating',
        "rationale": 'By visualizing the distribution of ratings, we can gain insights into the audience preferences and the types of content available on Netflix.',
        "index": 1
    },
    {
        "question": "What is the distribution of release years for the movies and TV shows on Netflix?",
        "visualization": "line chart of release_year",
        "rationale": "This countplot will show the distribution of release years for the movies and TV shows on Netflix, enabling the film critic to identify trends in release years and recommend movies based on the current trends.",
        "index": 2
    },
    {
        "question": 'What is the relationship between genres and release year?',
        "visualization": 'scatter chart of top 10 listed_in genres and release_year',
        "rationale": 'This visualization will show the correlations between genres and release year of movies and TV shows available on Netflix. It will help the film critic identify which genres in which years are more popular',
        "index": 3
    },
    {
        "question": "What is the relationship between director and genres of movies and TV shows on Netflix?",
        "visualization": "heatmap of directors and the listed_in genres, the colormap is decided by the counts of genres",
        "rationale": "This heatmap will show the correlations between directors and genres of movies and TV shows available on Netflix., aiding the film critic identifying genre trends.",
        "index": 4
    },
]

print("Start generating resuilts...")

results_path = os.path.join('./final', f"{lm.split('/')[-1]}")
os.makedirs(results_path, exist_ok=True)

results = {
    'lm': lm,
    'code_lm': code_lm,
    'summary': summary,
    'visualizations': []
}

for goal_num, goal in enumerate(persona_goals):
    try:
        output_dict = {
            'index': goal.index,
            'question': goal.question,
            'visualization': goal.visualization,
            'rationale': goal.rationale,
            'charts': {}
        }
    except:
        output_dict = {
            'index': goal['index'],
            'question': goal['question'],
            'visualization': goal['visualization'],
            'rationale': goal['rationale'],
            'charts': {}
        }
    textgen_config = TextGenerationConfig(n=3, temperature=0.6, model=code_lm, use_cache=True)
    for library in visual_libraries:
        charts = lida.visualize(summary=summary, goal=goal, textgen_config=textgen_config, library=library)  
        lm_output = []
        for i, chart in enumerate(charts):
            image_base64 = chart.raster
            img_f = os.path.join(results_path, f"{lm.split('/')[-1]}_persona_goal{goal_num}_{library}_{i}.png")
            save_image(image_base64, img_f)

            lm_output.append({
                'status': chart.status,  # True if successful
                'code': chart.code,  # code used to generate the visualization
                'library': chart.library,  # library used to generate the visualization
                'error': chart.error,  # error message if status is False
                'image': img_f
            })
        output_dict['charts'][library] = lm_output

    results['visualizations'].append(output_dict)

with open(os.path.join(results_path, f"{lm.split('/')[-1]}_{code_lm.split('/')[-1]}_result.json"), 'w') as fw:
    json.dump(results, fw, ensure_ascii=False, indent=4)

print("Done!")
