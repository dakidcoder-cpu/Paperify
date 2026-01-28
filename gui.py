import threading
import tkinter as tk
from tkinter import scrolledtext
from main import run_query


def run_and_display(query, btn, out_widget):
    btn.config(state="disabled")
    out_widget.config(state="normal")
    out_widget.delete("1.0", tk.END)
    out_widget.insert(tk.END, "Thinking...\n")
    out_widget.update()
    try:
        resp = run_query(query)
    except Exception as e:
        resp = f"Error: {e}"
    out_widget.delete("1.0", tk.END)
    out_widget.insert(tk.END, resp)
    out_widget.config(state="disabled")
    btn.config(state="normal")


def on_submit(entry, btn, out_widget):
    q = entry.get().strip()
    if not q:
        return
    t = threading.Thread(target=run_and_display, args=(q, btn, out_widget), daemon=True)
    t.start()


root = tk.Tk()
root.title("Paperify Research")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

entry = tk.Entry(frame, width=80)
entry.pack(fill="x", pady=(0,8))
entry.focus()

output = scrolledtext.ScrolledText(frame, height=20, state="disabled", wrap="word")
output.pack(fill="both", expand=True)

submit_btn = tk.Button(frame, text="Ask", width=10, command=lambda: on_submit(entry, submit_btn, output))
submit_btn.pack(pady=(8,0))

root.mainloop()
