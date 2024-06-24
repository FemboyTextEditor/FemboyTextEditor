import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import re


def apply_text_styles(text_widget):
    """Apply text styles to the text in the text widget."""
    text_widget.tag_remove("bold", "1.0", tk.END)
    text_widget.tag_remove("italic", "1.0", tk.END)
    text_widget.tag_remove("bold_italic", "1.0", tk.END)
    text_widget.tag_remove("hide", "1.0", tk.END)

    # Patterns for finding styled text
    patterns = [
        (r"\*\*\*(.*?)\*\*\*", "bold_italic"),
        (r"\*(.*?)\*", "bold"),
        (r"\*\*(.*?)\*\*", "italic"),
    ]

    for pattern, tag in patterns:
        for match in re.finditer(pattern, text_widget.get("1.0", tk.END), re.DOTALL):
            start_idx = f"1.0 + {match.start()} chars"
            end_idx = f"1.0 + {match.end()} chars"
            text_widget.tag_add(tag, start_idx, end_idx)

            # Apply the hide tag to the asterisks
            for asterisk_pos in range(match.start(), match.end()):
                if text_widget.get(f"1.0 + {asterisk_pos} chars", f"1.0 + {asterisk_pos + 1} chars") == '*':
                    text_widget.tag_add("hide", f"1.0 + {asterisk_pos} chars", f"1.0 + {asterisk_pos + 1} chars")

    text_widget.tag_config("bold", font="Helvetica 18 bold")
    text_widget.tag_config("italic", font="Helvetica 18 italic")
    text_widget.tag_config("bold_italic", font="Helvetica 18 bold italic")
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

    save_button = ttk.Button(frame, text="Save", command=lambda: save_file(window, text_edit), style='Custom.TButton')
    open_button = ttk.Button(frame, text="Open", command=lambda: open_file(window, text_edit), style='Custom.TButton')

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
