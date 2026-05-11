"""
Multi-Language English Translator Module
Supports: Telugu, Tamil, Hindi, Malayalam, and Kannada
"""

from deep_translator import GoogleTranslator


class MultiLanguageTranslator:
    """Translates English text to multiple Indian languages using Google Translate API"""
    
    SUPPORTED_LANGUAGES = {
        'kannada': {'code': 'kn', 'name': 'Kannada'},
        'telugu': {'code': 'te', 'name': 'Telugu'},
        'tamil': {'code': 'ta', 'name': 'Tamil'},
        'hindi': {'code': 'hi', 'name': 'Hindi'},
        'malayalam': {'code': 'ml', 'name': 'Malayalam'},
    }
    
    def __init__(self, target_language='kannada'):
        """
        Initialize the translator
        
        Args:
            target_language (str): Target language code or name (default: 'kannada')
        """
        self.set_target_language(target_language)
    
    def set_target_language(self, target_language):
        """
        Set the target language for translation
        
        Args:
            target_language (str): Target language code or name
        """
        # Normalize input to lowercase
        target_language = target_language.lower().strip()
        
        # If it's a language name, convert to code
        if target_language in self.SUPPORTED_LANGUAGES:
            self.target_code = self.SUPPORTED_LANGUAGES[target_language]['code']
            self.target_language = target_language
        else:
            raise ValueError(f"Unsupported language: {target_language}. Supported: {', '.join(self.SUPPORTED_LANGUAGES.keys())}")
        
        self.translator = GoogleTranslator(source='en', target=self.target_code)
    
    def translate(self, text):
        """
        Translate English text to target language
        
        Args:
            text (str): English text to translate
            
        Returns:
            str: Translated text
        """
        if not text or not text.strip():
            return ""
        
        try:
            translation = self.translator.translate(text)
            return translation
        except Exception as e:
            return f"Error: {str(e)}"
    
    def translate_file(self, input_file, output_file):
        """
        Translate English text from a file to target language and save to output file
        
        Args:
            input_file (str): Path to input file with English text
            output_file (str): Path to output file for translated text
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            translated_text = self.translate(text)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated_text)
            
            print(f"Translation completed. Output saved to {output_file}")
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found")
        except Exception as e:
            print(f"Error: {str(e)}")
