
## TO DO:

☐ Adjust post-processing of the model (so that is easier to process for TTS)

☐ Video Generation ? (Find something that would work) => Lightweight and portable

☐ Update and modify requirements.txt



# Faster Speech To Speech:

[![Demo Video](https://github.com/harvestingmoon/S2S/blob/master/demo.MOV)]

## A very fast way to get S2S models

### How? just abuse APIs (while they are still free)

## Important: Currently it is still in development, overtime I would increase its feature capabilities and modifications :) <If my school hours permits ?>


A super fast and quick way to implement a speech to speech model using:

### 1. Groq

### 2. Google TTS Service

If you wish to just call Google TTS API just run

```python s2s.py --gtts  ```



### 3. Coqui TTS (Locally Run & Modifiable!) [Default]


## Simple Pipeline:

### Person Talking ===> Groq Whisper ===> Groq Llama-70b-8192 ===> Google TTS Services


## Modifications:



## How To Use:

1. Ensure you install the requirements via 

    ``` pip install requirements.txt ```
2. Remember to sign up for Groq Playground and create an API_KEY

3. Run the script 

    ```python s2s.py ``` 

### It goes by a simple CLI interface

Just run ```python s2s.py ``` followed by the following args commands you can try:


``` --output file_to_path ``` : To set path for audio

``` --gtts ```: Enables Google TTS Service, else fallsback to Coqui TTS

``` --temperature (insert int) ```: controls creativity of the model

``` --audio (audio_name) ```: Sets name of your microphone 

``` --model (model_name) ```: Set model name (Default is llama3-70b-8192)


## Requirements:

### 1. Cuda 12.4 
### 2. Groq Account
### 3. Accepting Coqui TTS UAT



## Acknowledgements:

### 1. Groq (For providing superfast inference)
### 2. Coqui (For providing the open source weights)