import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import re
import subprocess
import json

# Run the createjson.py script when the main script is executed
subprocess.run(["python", "createjson.py"])

# Run the language.py script and capture the output
result = subprocess.run(["python", "language.py"], capture_output=True, text=True)

# Parse the JSON output from language.py
if result.returncode == 0:
    language_settings = json.loads(result.stdout.strip())
else:
    language_settings = {"save_text": "Save", "open_text": "Open"}

def apply_text_styles(text_widget):
    """Apply text styles to the text in the text widget."""
    text_widget.tag_remove("bold", "1.0", tk.END)
    text_widget.tag_remove("italic", "1.0", tk.END)
    text_widget.tag_remove("underline", "1.0", tk.END)
    text_widget.tag_remove("strikethrough", "1.0", tk.END)
    text_widget.tag_remove("hide", "1.0", tk.END)

    # Patterns for finding styled text
    patterns = [
        (r"\*\*\*(.*?)\*\*\*", "bold_italic"),  # ***text*** -> Bold + Italic
        (r"\*\*(.*?)\*\*", "bold"),  # **text** -> Bold
        (r"\*(.*?)\*", "italic"),  # *text* -> Italic
        (r"_(.*?)_", "underline"),  # _text_ -> Underline
        (r"~(.*?)~", "strikethrough"),  # ~text~ -> Strikethrough

        # Combined styles
        (r"\*\*_(.*?)_\*\*", "underline_bold"),  # **_text_** -> Bold + Underline
        (r"\*_(.*?)_\*", "underline_italic"),  # *_text_* -> Italic + Underline
        (r"\*\*~(.*?)~\*\*", "strikethrough_bold"),  # **~text~** -> Bold + Strikethrough
        (r"\*~(.*?)~\*", "strikethrough_italic"),  # *~text~* -> Italic + Strikethrough
        (r"\*\*\*_(.*?)_\*\*\*", "underline_bold_italic"),  # ***_text_*** -> Bold + Italic + Underline
        (r"\*\*\*~(.*?)~\*\*\*", "bold_italic_strikethrough")  # ***~text~*** -> Bold + Italic + Strikethrough
    ]

    for pattern, tag in patterns:
        for match in re.finditer(pattern, text_widget.get("1.0", tk.END), re.DOTALL):
            start_idx = f"1.0 + {match.start()} chars"
            end_idx = f"1.0 + {match.end()} chars"
            text_widget.tag_add(tag, start_idx, end_idx)

            # Apply the hide tag to the asterisks/underscores/tilde
            for pos in range(match.start(), match.end()):
                char = text_widget.get(f"1.0 + {pos} chars", f"1.0 + {pos + 1} chars")
                if char in "*_~":
                    text_widget.tag_add("hide", f"1.0 + {pos} chars", f"1.0 + {pos + 1} chars")

    text_widget.tag_config("bold", font="Helvetica 18 bold")
    text_widget.tag_config("italic", font="Helvetica 18 italic")
    text_widget.tag_config("underline", font="Helvetica 18 underline")
    text_widget.tag_config("strikethrough", font="Helvetica 18", overstrike=1)
    text_widget.tag_config("bold_italic", font="Helvetica 18 bold italic")
    text_widget.tag_config("underline_bold", font="Helvetica 18 bold underline")
    text_widget.tag_config("underline_italic", font="Helvetica 18 italic underline")
    text_widget.tag_config("strikethrough_bold", font="Helvetica 18 bold", overstrike=1)
    text_widget.tag_config("strikethrough_italic", font="Helvetica 18 italic", overstrike=1)
    text_widget.tag_config("underline_bold_italic", font="Helvetica 18 bold italic underline")
    text_widget.tag_config("bold_italic_strikethrough", font="Helvetica 18 bold italic", overstrike=1)
    text_widget.tag_config("hide", elide=True)

def open_file(window, text_edit):
    filepath = askopenfilename(filetypes=[("Markdown Files", "*.md")])
    if not filepath:
        return
    with open(filepath, "r") as f:
        content = f.read()
    text_edit.delete(1.0, tk.END)
    text_edit.insert(tk.END, content)
    apply_text_styles(text_edit)
    window.title(f"Open File: {filepath}")

def save_file(window, text_edit):
    filepath = asksaveasfilename(filetypes=[("Markdown Files", "*.md")])
    if not filepath:
        return
    with open(filepath, "w") as f:
        content = text_edit.get(1.0, tk.END)
        f.write(content)
    window.title(f"Save File: {filepath}")

def main():
    window = tk.Tk()
    window.title("Femboy Text Editor")

    # Load the icon image
    icon = tk.PhotoImage(file="icon.png")
    window.iconphoto(False, icon)

    # A4 size in pixels (approximately) for a typical screen resolution (96 DPI)
    a4_width = 794
    a4_height = 1123
    window.geometry(f"{a4_width}x{a4_height}")

    text_edit = tk.Text(window, font="Helvetica 18")
    text_edit.grid(row=0, column=1, sticky="nsew")

    frame = tk.Frame(window, relief=tk.RAISED, bd=2)

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12))
    style.map('Custom.TButton',
              foreground=[('!active', 'white'), ('pressed', 'white'), ('active', 'white')],
              background=[('!active', '#00008B'), ('pressed', '#00008B'), ('active', '#00008B')])

    # Use language settings from language.py
    save_button = ttk.Button(frame, text=language_settings["save_text"], command=lambda: save_file(window, text_edit), style='Custom.TButton')
    open_button = ttk.Button(frame, text=language_settings["open_text"], command=lambda: open_file(window, text_edit), style='Custom.TButton')

    save_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    open_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    frame.grid(row=0, column=0, sticky="ns")

    # Make the text field expand to fit the window
    window.rowconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)

    window.bind("<Control-s>", lambda x: save_file(window, text_edit))
    window.bind("<Control-o>", lambda x: open_file(window, text_edit))

    text_edit.bind("<KeyRelease>", lambda event: apply_text_styles(text_edit))

    window.mainloop()

main()
