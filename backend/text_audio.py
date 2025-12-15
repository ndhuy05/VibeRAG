import re
import os
import wave
from typing import Optional
from google import genai
from google.genai import types
import config


class TextToAudioService:
    
    def __init__(self, api_key: str = None, output_dir: str = "audio_output"):
        self.api_key = api_key or config.GEMINI_API_KEY
        self.output_dir = output_dir
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self.client = None
        
    def preprocess_text_for_speech(self, text: str) -> str:
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        text = re.sub(r'`(.+?)`', r'\1', text)
        
        text = re.sub(r'https?://([^\s]+)', r'\1', text)
        
        abbreviations = {
            r'\bDr\.': 'Doctor',
            r'\bMr\.': 'Mister',
            r'\bMrs\.': 'Missus',
            r'\bMs\.': 'Miss',
            r'\be\.g\.': 'for example',
            r'\bi\.e\.': 'that is',
            r'\betc\.': 'et cetera',
            r'\bvs\.': 'versus',
            r'\bmin\.': 'minutes',
            r'\bhr\.': 'hour',
            r'\bhrs\.': 'hours',
            r'\btsp\.': 'teaspoon',
            r'\btbsp\.': 'tablespoon',
            r'\bcup\.': 'cup',
            r'\blb\.': 'pound',
            r'\boz\.': 'ounce',
            r'\bno\.': 'number',
        }
        
        for abbr, expansion in abbreviations.items():
            text = re.sub(abbr, expansion, text, flags=re.IGNORECASE)
        
        text = re.sub(r'\b1/2\b', 'half', text)
        text = re.sub(r'\b1/4\b', 'quarter', text)
        text = re.sub(r'\b3/4\b', 'three quarters', text)
        text = re.sub(r'\b1/3\b', 'one third', text)
        text = re.sub(r'\b2/3\b', 'two thirds', text)
        
        text = re.sub(r',([^\s])', r', \1', text)
        text = re.sub(r'\.([A-Z])', r'. \1', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def generate_audio(
        self, 
        text: str, 
        filename: Optional[str] = None,
        voice_name: str = "Achernar",
        language_code: str = "en-US",
        prompt: Optional[str] = None
    ) -> str:
        processed_text = self.preprocess_text_for_speech(text)
        
        if filename is None:
            import time
            filename = f"response_{int(time.time())}"
        
        if not filename.endswith('.wav'):
            filename += '.wav'
        
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=self.api_key)
            
            print(f"[TTS] Generating audio for text: {processed_text[:100]}...")
            print(f"[TTS] Using voice: {voice_name}")
            
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=processed_text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice_name,
                            )
                        )
                    ),
                )
            )
            
            audio_data = response.candidates[0].content.parts[0].inline_data.data
            
            self._save_wav_file(output_path, audio_data)
            
            print(f"[TTS] Successfully created audio file: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"[TTS Error] Failed to generate audio: {str(e)}")
            raise Exception(f"Failed to generate audio: {str(e)}")
    
    def _save_wav_file(self, filepath: str, pcm_data: bytes, channels: int = 1, 
                       rate: int = 24000, sample_width: int = 2):
        with wave.open(filepath, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm_data)



def text_to_audio(
    text: str,
    output_filename: Optional[str] = None,
    voice_name: str = "Achernar",
    language_code: str = "en-US"
) -> str:
    service = TextToAudioService()
    return service.generate_audio(
        text=text,
        filename=output_filename,
        voice_name=voice_name,
        language_code=language_code
    )