"""
Multi-Language English Translator - GUI Version using Tkinter
Supports: Telugu, Tamil, Hindi, Malayalam, and Kannada
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
from translator import MultiLanguageTranslator


class TranslatorGUI:
    """GUI for Multi-Language Translator"""
    
    SUPPORTED_LANGUAGES = {
        'Kannada': 'kannada',
        'Telugu': 'telugu',
        'Tamil': 'tamil',
        'Hindi': 'hindi',
        'Malayalam': 'malayalam',
    }
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("Multi-Language Translator")
        self.root.geometry("900x700")
        self.selected_language = 'kannada'
        self.translator = MultiLanguageTranslator('kannada')
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root,
            text="Multi-Language English Translator",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Language selector frame
        lang_frame = tk.Frame(self.root)
        lang_frame.pack(pady=10)
        
        lang_label = tk.Label(lang_frame, text="Select Target Language:", font=("Arial", 10, "bold"))
        lang_label.pack(side=tk.LEFT, padx=5)
        
        self.language_var = tk.StringVar(value="Kannada")
        language_menu = ttk.Combobox(
            lang_frame,
            textvariable=self.language_var,
            values=list(self.SUPPORTED_LANGUAGES.keys()),
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        language_menu.pack(side=tk.LEFT, padx=5)
        language_menu.bind("<<ComboboxSelected>>", self.on_language_change)
        
        # Input section
        input_label = tk.Label(self.root, text="English Text:", font=("Arial", 10, "bold"))
        input_label.pack(anchor="w", padx=10)
        
        self.input_text = scrolledtext.ScrolledText(
            self.root,
            height=10,
            width=90,
            font=("Arial", 10)
        )
        self.input_text.pack(padx=10, pady=5)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        translate_btn = tk.Button(
            button_frame,
            text="Translate",
            command=self.translate_text,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20
        )
        translate_btn.grid(row=0, column=0, padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_text,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20
        )
        clear_btn.grid(row=0, column=1, padx=5)
        
        file_btn = tk.Button(
            button_frame,
            text="Translate File",
            command=self.translate_file,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20
        )
        file_btn.grid(row=0, column=2, padx=5)
        
        # Output section
        self.output_label = tk.Label(self.root, text="Kannada Translation:", font=("Arial", 10, "bold"))
        self.output_label.pack(anchor="w", padx=10)
        
        self.output_text = scrolledtext.ScrolledText(
            self.root,
            height=10,
            width=90,
            font=("Arial", 10)
        )
        self.output_text.pack(padx=10, pady=5)
        
        # Copy button
        copy_btn = tk.Button(
            self.root,
            text="Copy Translation",
            command=self.copy_translation,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold")
        )
        copy_btn.pack(pady=5)
    
    def on_language_change(self, event=None):
        """Handle language selection change"""
        selected_name = self.language_var.get()
        self.selected_language = self.SUPPORTED_LANGUAGES[selected_name]
        self.translator = MultiLanguageTranslator(self.selected_language)
        self.output_label.config(text=f"{selected_name} Translation:")
        self.clear_text()
    
    def translate_text(self):
        """Translate the input text"""
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter English text to translate.")
            return
        
        try:
            result = self.translator.translate(text)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Error", f"Translation failed: {str(e)}")
    
    def clear_text(self):
        """Clear both input and output text"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
    
    def copy_translation(self):
        """Copy the translation to clipboard"""
        text = self.output_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "No translation to copy.")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Success", "Translation copied to clipboard!")
    
    def translate_file(self):
        """Translate text from a file"""
        input_file = filedialog.askopenfilename(
            title="Select English text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not input_file:
            return
        
        lang_name = self.language_var.get().lower()
        output_file = filedialog.asksaveasfilename(
            title=f"Save {lang_name} translation as",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            defaultextension=".txt",
            initialfile=f"{lang_name}_translation.txt"
        )
        
        if not output_file:
            return
        
        try:
            self.translator.translate_file(input_file, output_file)
            messagebox.showinfo("Success", f"Translation saved to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"File translation failed: {str(e)}")


def main():
    """Main function"""
    root = tk.Tk()
    gui = TranslatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
