#!/usr/bin/env python3
"""
PyCalc - A Python Calculator
Double-click this file to run the calculator offline.
Requires Python 3.6+ (tkinter is included with Python by default)
"""

import tkinter as tk
from tkinter import font as tkfont


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("PyCalc")
        self.root.geometry("380x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a2744")
        
        # State
        self.expression = ""
        self.display_value = "0"
        
        # Fonts
        self.display_font = tkfont.Font(family="Consolas", size=32, weight="bold")
        self.expr_font = tkfont.Font(family="Consolas", size=14)
        self.button_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        
        self._create_ui()
    
    def _create_ui(self):
        # Main container
        container = tk.Frame(self.root, bg="#1e3a5f", padx=20, pady=20)
        container.pack(expand=True, fill="both", padx=15, pady=15)
        
        # Header with Python logo representation
        header = tk.Frame(container, bg="#1e3a5f")
        header.pack(fill="x", pady=(0, 15))
        
        # Python logo circles
        logo_frame = tk.Frame(header, bg="#1e3a5f")
        logo_frame.pack(side="left")
        
        canvas = tk.Canvas(logo_frame, width=40, height=24, bg="#1e3a5f", highlightthickness=0)
        canvas.pack(side="left")
        canvas.create_oval(2, 2, 20, 20, fill="#ffd43b", outline="")
        canvas.create_oval(18, 4, 36, 22, fill="#306998", outline="")
        
        title = tk.Label(header, text="PyCalc", font=("Segoe UI", 18, "bold"), 
                        fg="#ffffff", bg="#1e3a5f")
        title.pack(side="left", padx=(10, 0))
        
        # Display area
        display_frame = tk.Frame(container, bg="#142238", padx=15, pady=15)
        display_frame.pack(fill="x", pady=(0, 15))
        
        # Expression label
        self.expr_label = tk.Label(display_frame, text=">>> ", font=self.expr_font,
                                   fg="#7a8fa6", bg="#142238", anchor="e")
        self.expr_label.pack(fill="x")
        
        # Result label
        self.result_label = tk.Label(display_frame, text="0", font=self.display_font,
                                     fg="#ffffff", bg="#142238", anchor="e")
        self.result_label.pack(fill="x")
        
        # Buttons grid
        buttons_frame = tk.Frame(container, bg="#1e3a5f")
        buttons_frame.pack(expand=True, fill="both")
        
        # Button layout
        buttons = [
            [("C", "muted"), ("()", "muted"), ("%", "muted"), ("÷", "operator")],
            [("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator")],
            [("4", "number"), ("5", "number"), ("6", "number"), ("−", "operator")],
            [("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator")],
            [("±", "muted"), ("0", "number"), (".", "number"), ("=", "equals")],
        ]
        
        # Colors
        colors = {
            "number": {"bg": "#2a4a6e", "fg": "#ffffff", "hover": "#3a5a7e"},
            "operator": {"bg": "#306998", "fg": "#ffffff", "hover": "#4079a8"},
            "muted": {"bg": "#1a3355", "fg": "#a0b0c0", "hover": "#2a4365"},
            "equals": {"bg": "#ffd43b", "fg": "#1a2744", "hover": "#ffe45b"},
        }
        
        for row_idx, row in enumerate(buttons):
            buttons_frame.rowconfigure(row_idx, weight=1)
            for col_idx, (text, btn_type) in enumerate(row):
                buttons_frame.columnconfigure(col_idx, weight=1)
                
                color = colors[btn_type]
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    font=self.button_font,
                    fg=color["fg"],
                    bg=color["bg"],
                    activeforeground=color["fg"],
                    activebackground=color["hover"],
                    border=0,
                    cursor="hand2",
                    command=lambda t=text: self._on_button_click(t)
                )
                btn.grid(row=row_idx, column=col_idx, padx=4, pady=4, sticky="nsew")
                
                # Hover effects
                btn.bind("<Enter>", lambda e, b=btn, c=color: b.configure(bg=c["hover"]))
                btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c["bg"]))
        
        # Add backspace button at bottom
        backspace_frame = tk.Frame(container, bg="#1e3a5f")
        backspace_frame.pack(fill="x", pady=(10, 0))
        
        backspace_btn = tk.Button(
            backspace_frame,
            text="⌫ Backspace",
            font=("Segoe UI", 12),
            fg="#a0b0c0",
            bg="#1a3355",
            activeforeground="#ffffff",
            activebackground="#2a4365",
            border=0,
            cursor="hand2",
            pady=8,
            command=self._backspace
        )
        backspace_btn.pack(fill="x")
        backspace_btn.bind("<Enter>", lambda e: backspace_btn.configure(bg="#2a4365"))
        backspace_btn.bind("<Leave>", lambda e: backspace_btn.configure(bg="#1a3355"))
        
        # Keyboard bindings
        self.root.bind("<Key>", self._on_key_press)
        self.root.bind("<Return>", lambda e: self._calculate())
        self.root.bind("<BackSpace>", lambda e: self._backspace())
        self.root.bind("<Escape>", lambda e: self._clear())
    
    def _on_button_click(self, text):
        if text == "C":
            self._clear()
        elif text == "=":
            self._calculate()
        elif text == "±":
            self._negate()
        elif text == "%":
            self._percentage()
        elif text == "()":
            self._add_parenthesis()
        else:
            self._append(text)
    
    def _on_key_press(self, event):
        key = event.char
        if key in "0123456789.":
            self._append(key)
        elif key in "+-":
            self._append(key)
        elif key == "*":
            self._append("×")
        elif key == "/":
            self._append("÷")
        elif key == "(":
            self._append("(")
        elif key == ")":
            self._append(")")
    
    def _append(self, value):
        # Convert display operators to expression
        if self.expression == "" and value in "×÷+−":
            return
        
        self.expression += value
        self._update_display()
    
    def _clear(self):
        self.expression = ""
        self.display_value = "0"
        self._update_display()
    
    def _backspace(self):
        if self.expression:
            self.expression = self.expression[:-1]
            self._update_display()
    
    def _negate(self):
        if self.display_value and self.display_value != "0":
            if self.display_value.startswith("-"):
                self.display_value = self.display_value[1:]
            else:
                self.display_value = "-" + self.display_value
            self.expression = self.display_value
            self._update_display()
    
    def _percentage(self):
        try:
            result = float(self.display_value) / 100
            self.display_value = self._format_number(result)
            self.expression = self.display_value
            self._update_display()
        except:
            pass
    
    def _add_parenthesis(self):
        open_count = self.expression.count("(")
        close_count = self.expression.count(")")
        
        if open_count == close_count or (self.expression and self.expression[-1] in "×÷+−("):
            self.expression += "("
        else:
            self.expression += ")"
        
        self._update_display()
    
    def _calculate(self):
        if not self.expression:
            return
        
        try:
            # Convert display operators to Python operators
            calc_expr = self.expression.replace("×", "*").replace("÷", "/").replace("−", "-")
            result = eval(calc_expr)
            self.display_value = self._format_number(result)
            self.expression = self.display_value
        except:
            self.display_value = "Error"
            self.expression = ""
        
        self._update_display()
    
    def _format_number(self, num):
        if isinstance(num, float):
            if num == int(num):
                return str(int(num))
            return f"{num:.10g}"
        return str(num)
    
    def _update_display(self):
        display_expr = self.expression if self.expression else ""
        self.expr_label.config(text=f">>> {display_expr}")
        
        if self.expression:
            try:
                calc_expr = self.expression.replace("×", "*").replace("÷", "/").replace("−", "-")
                result = eval(calc_expr)
                self.display_value = self._format_number(result)
            except:
                self.display_value = self.expression.replace("×", "*").replace("÷", "/").replace("−", "-")
        else:
            self.display_value = "0"
        
        self.result_label.config(text=self.display_value)


def main():
    root = tk.Tk()
    
    # Center window on screen
    root.update_idletasks()
    width = 380
    height = 580
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    app = Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
