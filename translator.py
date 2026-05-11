"""
English to Kannada Translator Module
"""

from deep_translator import GoogleTranslator


class EnglishToKannadaTranslator:
    """Translates English text to Kannada using Google Translate API"""
    
    def __init__(self):
        """Initialize the translator"""
        self.translator = GoogleTranslator(source='en', target='kn')
    
    def translate(self, text):
        """
        Translate English text to Kannada
        
        Args:
            text (str): English text to translate
            
        Returns:
            str: Translated Kannada text
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
        Translate English text from a file to Kannada and save to output file
        
        Args:
            input_file (str): Path to input file with English text
            output_file (str): Path to output file for Kannada text
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
