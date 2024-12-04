import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}
history = []

def response(prompt):
    history.append(prompt)
    data = {
        "model": "TransformersPrime",
        "prompt": "\n".join(history),
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = json.loads(response.text)
        return result.get('response', 'No response field found')
    return f"Error: {response.text}"

def clear_history():
    global history
    history = []
    return "History cleared!"

with gr.Blocks() as interface:
    with gr.Row():
        prompt_input = gr.Textbox(label="Enter your Prompt", lines=4, placeholder="Type here...")
        clear_button = gr.Button("Clear History", variant="secondary")
    
    response_output = gr.Textbox(label="Response", interactive=False)
    
    submit_button = gr.Button("Submit")
    
    submit_button.click(response, inputs=prompt_input, outputs=response_output)
    clear_button.click(clear_history, inputs=None, outputs=response_output)

interface.launch(share=True)
