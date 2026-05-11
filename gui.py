"""
English to Kannada Translator - GUI Version using Tkinter
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from translator import EnglishToKannadaTranslator


class TranslatorGUI:
    """GUI for English to Kannada Translator"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("English to Kannada Translator")
        self.root.geometry("800x600")
        self.translator = EnglishToKannadaTranslator()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root,
            text="English to Kannada Translator",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
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
        output_label = tk.Label(self.root, text="Kannada Translation:", font=("Arial", 10, "bold"))
        output_label.pack(anchor="w", padx=10)
        
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
        
        output_file = filedialog.asksaveasfilename(
            title="Save Kannada translation as",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            defaultextension=".txt"
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
