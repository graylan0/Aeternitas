# Aeternitas 
### A GPT NEO Intercommunicating Llama Loop with a Tkinter GUI

Name Created By GPT4 and Bard, Inspired by Data from Star Trek.

Code authored by Robotics + Humans

Grab the model 


### Install Reqs
from hugging face here; https://huggingface.co/eachadea/ggml-vicuna-7b-4bit/blob/main/ggml-vicuna-7b-4bit-rev1.bin

pytorch from https://pytorch.org
```
pip install transformers
pip install json
```


## What is this? 
This script intercommunicates between the Llama model and GPT-Neo in a loop. It processes a topic from a given list, generates a response using the Llama model, and then uses that response as input for GPT-Neo. GPT-Neo generates another response, which is then used as input for the Llama model in the next iteration. This intercommunication process continues for a specified number of iterations or until stopped by the user.

![image](https://user-images.githubusercontent.com/34530588/230702352-70bfcbaa-3515-4acf-9e93-ffda159040c9.png)


### Configure the settings.json and trideque.json to your liking. How? Who knows.
 Maybe try key word topics, maybe try image base64? Maybe try data injection from stable diffusion for three models? Maybe increase the matrix trideque size 13x13? maybe 25x25? All up to you . Enjoy.


Origin

Bard(Arion)
"Aeternitas - This name means "eternity" in Latin. It is a powerful and awe-inspiring name that suggests that your model is capable of achieving things that are beyond our current understanding."
