import tkinter as tk
from tkinter import ttk

class ChatApp(tk.Tk):
    def __init__(self, logic=None, flow=[]):
        super().__init__()
        self.title("ChatBot GUI")
        self.configure(bg="#f0f0f0")
        self.logic = logic
        self.flow = flow

        self.user_response = tk.StringVar()
        self._build_widgets()
        self._on_send_clicked = lambda: None

    def _build_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.chat_frame = ttk.Frame(self)
        self.chat_frame.grid(row=0, column=0, sticky="nsew")
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.chat_canvas = tk.Canvas(self.chat_frame, bg="#f0f0f0", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.chat_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(
                scrollregion=self.chat_canvas.bbox("all")
            )
        )

        self.canvas_window = self.chat_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.chat_canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.chat_canvas.bind("<Configure>", self._resize_canvas)

        self.input_frame = ttk.Frame(self)
        self.input_frame.grid(row=1, column=0, sticky="ew")
        self.input_frame.columnconfigure(0, weight=1)

        self.user_input = ttk.Entry(self.input_frame, textvariable=self.user_response, font=("Helvetica", 14), show="")
        self.user_input.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.user_input.bind("<Return>", lambda e: self._on_send_clicked())

        self.send_button = ttk.Button(self.input_frame, text="Send", command=lambda: self._on_send_clicked())
        self.send_button.grid(row=0, column=1, padx=5, pady=5)

    def _resize_canvas(self, event):
        canvas_width = event.width
        self.chat_canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _add_message(self, text, sender="user"):
        bubble = ttk.Label(
            self.scrollable_frame,
            text=text,
            background="#cce5ff" if sender == "user" else "#e6e6e6",
            anchor="w" if sender == "bot" else "e",
            justify="left",
            wraplength=300,
            padding=8,
            relief="ridge"
        )
        bubble.pack(anchor="e" if sender == "user" else "w", pady=2, padx=10, fill="none")

        self.after(100, lambda: self.chat_canvas.yview_moveto(1.0))

    def _add_bot_message(self, text):
        self._add_message(text, sender="bot")

    def ask_user(self, question: str):
        self._add_bot_message(question)
        self.response_var = tk.StringVar()

        def on_response(event=None):
            user_text = self.user_input.get().strip()
            if user_text:
                self._add_message(user_text, sender="user")
                self.user_input.delete(0, tk.END)
                self.response_var.set(user_text)

        self.user_input.bind("<Return>", on_response)
        self._on_send_clicked = on_response

        self.wait_variable(self.response_var)
        return self.response_var.get()

    def reset_chat(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def ask_password(self, prompt: str):
        self._add_bot_message(prompt)

        self.password_var = tk.StringVar()

        def on_password_submit(event=None):
            password_text = self.user_input.get()
            if password_text:
                self.user_input.delete(0, tk.END)
                self.password_var.set(password_text)

        self.user_input.configure(show="*")
        self.user_input.bind("<Return>", on_password_submit)
        self._on_send_clicked = on_password_submit

        self.wait_variable(self.password_var)
        password = self.password_var.get()

        self.user_input.configure(show="")  # Reset input visibility
        self.user_response.set("")
        return password
