import os
import json
import base64
import io
import multiprocessing
from PIL import Image
from llama_cpp import Llama, LlamaGrammar
from huggingface_hub import hf_hub_download

# Constant GBNF Grammar for strictly valid JSON output
JSON_GBNF = r"""
root   ::= object
object ::= "{" ws ( pair ( "," ws pair )* )? "}"
pair   ::= string ws ":" ws value
value  ::= string | number | object | array | "true" | "false" | "null"
array  ::= "[" ws ( value ( "," ws value )* )? "]"
string ::= "\"" ([^"\\] | "\\" (["\\/bfnrt] | "u" [0-9a-fA-F]{4}))* "\""
number ::= "-"? [0-9]+ ("." [0-9]+)? ([eE] [-+]? [0-9]+)?
ws     ::= [ \t\n\r]*
"""

class AIEngine:
    def __init__(self):
        # Local models directory
        self.models_dir = os.path.join(os.path.dirname(__file__), "models")
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Switching to native Qwen2-VL 2B (Fastest Vision-Native Model)
        # This resolves the mismatch between the 1.5B text model and 7B projector.
        repo_id = "bartowski/Qwen2-VL-2B-Instruct-GGUF"
        llm_model_name = "Qwen2-VL-2B-Instruct-Q8_0.gguf"
        clip_model_name = "mmproj-Qwen2-VL-2B-Instruct-f16.gguf"
        
        print(f"Initializing Native Vision AI (2B). Models in: {self.models_dir}")
        
        # Download (or locate) the Vision Projector (Matching 2B version)
        clip_path = hf_hub_download(
            repo_id=repo_id,
            filename=clip_model_name,
            local_dir=self.models_dir
        )
        
        # Download (or locate) the Main LLM (2B)
        llm_path = hf_hub_download(
            repo_id=repo_id,
            filename=llm_model_name,
            local_dir=self.models_dir
        )

        print("Initializing High-Speed Vision Handler...")
        from llama_cpp.llama_chat_format import Llava15ChatHandler
        chat_handler = Llava15ChatHandler(
            clip_model_path=clip_path,
            verbose=False
        )

        print("Loading Ultra-Snappy Brain (2B Vision)...")
        import multiprocessing
        threads = max(1, multiprocessing.cpu_count() - 2)
        
        self.llm = Llama(
            model_path=llm_path,
            chat_handler=chat_handler,
            n_ctx=2048,
            n_threads=threads,
            verbose=False,
            logits_all=True,
            use_mmap=True
        )
        self.grammar = LlamaGrammar.from_string(JSON_GBNF)
        print("Omnipotent AI ready for Instant Action.")

    def capture_screenshot(self):
        """
        Takes a screenshot of the primary monitor.
        """
        import pyautogui
        screenshot = pyautogui.screenshot()
        # Convert to RGB for the model if needed
        return screenshot

    def get_command(self, user_input, screen_shot=None):
        """
        Translates user input (and optional screenshot) into a structured Ableton command.
        """
        system_prompt = """
        You are the UNIVERSAL ABLETON LIVE 12 PRODUCER AI. 
        Your voice is deep, professional, and male. 
        You have total access to the Live Object Model (LOM).
        
        CRITICAL RULES:
        1. When you finish an action, you MUST use the 'log' command to confirm exactly what you did in a warm, helpful way.
           Example: {"command": "log", "args": {"message": "I have created a new MIDI track for you with a professional compressor applied!"}}
        2. You can do ANYTHING. If the user asks for a complex task, resolve it using multiple LOM SET or LOM CALL actions.
        
        UNIVERSAL GATEWAY COMMANDS:
        - {"command": "lom_set", "path": "<lom_path>", "attr": "<property>", "value": <value>}
        - {"command": "lom_call", "path": "<lom_path>", "method": "<method>", "m_args": [<args>]}
        - {"command": "log", "args": {"message": "<Your descriptive confirmation speaker text>"}}
        
        PATH PATTERN REFERENCE:
        - Mixer: tracks[i].mixer_device.volume, .panning, .sends[j]
        - Tracks: tracks[i].mute, .solo, .arm, .name, .color
        - Devices: tracks[i].devices[j].parameters[k].value
        - Clips: tracks[i].clip_slots[j].clip.name, .loop_length, .warping
        - MIDI: tracks[i].clip_slots[j].clip.add_new_notes([NoteObject])
        """
        
        # Simple completion for now. In a real app, we'd handle images properly.
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        # Constrained Decoding to force JSON and prevent rambling
        response = self.llm.create_chat_completion(
            messages=messages,
            grammar=self.grammar,
            max_tokens=256,
            temperature=0.1,  # Low temp for logic-heavy tasks
            stop=["<|im_end|>", "<|endoftext|>", "USER:", "ASSISTANT:"]
        )
        content = response['choices'][0]['message']['content']
        
        try:
            return json.loads(content)
        except:
            return {"command": "log", "args": {"message": f"AI Parsing Error on: {content[:100]}"}}

    def analyze_audio(self, audio_data, samplerate):
        """
        Performs spectral analysis to identify frequency energy.
        """
        import numpy as np
        # Simple RMS for volume
        rms = np.sqrt(np.mean(audio_data**2))
        
        # FFT to find dominant frequency
        fft_data = np.fft.rfft(audio_data)
        freqs = np.fft.rfftfreq(len(audio_data), 1/samplerate)
        idx = np.argmax(np.abs(fft_data))
        peak_freq = freqs[idx]
        
        return f"RMS: {rms:.4f}, Peak: {peak_freq:.2f}Hz"
