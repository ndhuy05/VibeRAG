import re
import os
from typing import Optional
from gtts import gTTS


class TextToAudioService:
    
    def __init__(self, output_dir: str = "audio_output"):
        self.output_dir = output_dir
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
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
        voice_name: str = "Achernar",  # Kept for backward compatibility, not used
        language_code: str = "en-US",
        prompt: Optional[str] = None  # Kept for backward compatibility, not used
    ) -> str:
        """
        Generate audio from text using gTTS (Google Text-to-Speech).
        
        Args:
            text: The text to convert to speech
            filename: Output filename (optional)
            voice_name: Kept for backward compatibility, not used with gTTS
            language_code: Language code (e.g., 'en-US', 'vi', 'en', 'es')
            prompt: Kept for backward compatibility, not used with gTTS
            
        Returns:
            Path to the generated audio file
        """
        processed_text = self.preprocess_text_for_speech(text)
        
        if filename is None:
            import time
            filename = f"response_{int(time.time())}"
        
        # gTTS outputs mp3 by default, but we'll convert the extension
        if not filename.endswith('.mp3'):
            filename += '.mp3'
        
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            # Convert language code from 'en-US' format to 'en' format for gTTS
            lang = language_code.split('-')[0] if '-' in language_code else language_code
            
            print(f"[TTS] Generating audio for text: {processed_text[:100]}...")
            print(f"[TTS] Using language: {lang}")
            
            # Generate speech using gTTS
            tts = gTTS(text=processed_text, lang=lang, slow=False)
            tts.save(output_path)
            
            print(f"[TTS] Successfully created audio file: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"[TTS Error] Failed to generate audio: {str(e)}")
            raise Exception(f"Failed to generate audio: {str(e)}")



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
