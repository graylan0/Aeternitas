import json
import torch
import time
import threading
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, Y, RIGHT, END
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from llama_cpp import Llama

stop_loop = False

# Llama Model
llm = Llama(model_path="C:\\Users\\Shadow\\ggml-vicuna-7b-4bit\\ggml-vicuna-7b-4bit-rev1.bin")

def llama_generate(prompt, max_tokens=200):
    output = llm(prompt, max_tokens=max_tokens)
    return output['choices'][0]['text']  # return the text of the completion


# GPT-Neo Model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-125m').to(device)
tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-125m')

tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model.config.pad_token_id = tokenizer.pad_token_id

def generate_chunks(prompt, chunk_size=1500):
    words = prompt.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def gpt3_generate(model, tokenizer, chunk, max_length=2000, time_limit=50.0):
    start_time = time.time()

    inputs = tokenizer.encode(chunk, return_tensors='pt', truncation=True, max_length=512).to(device)
    attention_mask = inputs.ne(tokenizer.pad_token_id).float().to(device)
    outputs = model.generate(inputs, max_length=max_length, do_sample=True, max_time=time_limit, attention_mask=attention_mask)

    response = tokenizer.decode(outputs[0])
    end_time = time.time()

    return response, end_time - start_time

with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

loop_count = settings['loop_count']

with open('trideque.json', 'r') as trideque_file:
    trideque = json.load(trideque_file)

def send_chunks_intercommunication(trideque_point, loop_count=-1):
    global stop_loop
    repetition = 0

    if 0 <= trideque_point < len(trideque):
        while (loop_count == -1 or repetition < loop_count) and not stop_loop:
            response = ""
            for topic in trideque[trideque_point]:
                for model_name in ['llama', 'gpt-neo']:
                    if model_name == 'llama':
                        response = llama_generate(topic)
                    else:
                        chunks = generate_chunks(response)  # make sure to pass a string to generate_chunks()
                        for chunk in chunks:  # process chunks sequentially
                            response, _ = gpt3_generate(model, tokenizer, chunk)

                output_text.insert(END, f"{topic}: {response}\n")
            repetition += 1
    else:
        output_text.insert(END, "Invalid trideque point. Please enter a valid index.\n")

def on_generate_click():
    trideque_point = int(trideque_point_input.get())
    threading.Thread(target=send_chunks_intercommunication, args=(trideque_point, loop_count)).start()

# GUI setup
root = Tk()
root.title("TheMatrix")
root.geometry("954x800")

root.config(background='black')
Label(root, text="Point:", fg="green", bg="black", font=("Courier", 14)).grid(row=2, column=0, sticky="W")

trideque_point_input = Entry(root, width=10)
trideque_point_input.grid(row=3, column=0)

Label(root, text="Enter input:", fg="green", bg="black", font=("Courier", 14)).grid(row=0, column=0, sticky="W")

input_text = Entry(root, width=100)
input_text.grid(row=1, column=0)

Button(root, text="Generate", command=on_generate_click, bg="green", fg="black", font=("Courier", 14)).grid(row=1, column=1)

output_text = Text(root, wrap="word", width=80, height=20, bg="#0a0a0a", fg="#00ff00", font=("Courier", 14))
output_text.grid(row=2, column=0, columnspan=6, padx=10, pady=10)

scrollbar = Scrollbar(root, command=output_text.yview)
scrollbar.grid(row=2, column=6, sticky="ns")
output_text.config(yscrollcommand=scrollbar.set)

root.mainloop()