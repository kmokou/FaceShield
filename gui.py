import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
import threading
import warnings

# Suppress TensorFlow warnings
warnings.filterwarnings('ignore', category=UserWarning, module='tensorflow')

class FaceShieldGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FaceShield")
        self.root.geometry("400x550")
        self.root.config(bg="black")
        self.current_process = None
        self.log_visible = True
        self.setup_ui()
        
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure main button style
        style.configure("RoundedButton.TButton",
                      foreground="#FF80AB", background="black",
                      bordercolor="#FF80AB", borderwidth=2,
                      font=("Montserrat", 14), padding=10)
        
        # Configure small button style
        style.configure("Small.TButton",
                      foreground="#FF80AB", background="black",
                      bordercolor="#FF80AB", borderwidth=1,
                      font=("Montserrat", 10), padding=5)
        
        # Title and subtitle
        tk.Label(self.root, text="FaceShield", font=("Montserrat", 20, "bold"), 
                fg="#FF4081", bg="black").pack(pady=(20,0))
        tk.Label(self.root, text="Защити свои данные автоматически", 
                font=("Montserrat", 14), fg="#FF80AB", bg="black").pack(pady=(0,25))
        
        # Buttons frame
        self.button_frame = tk.Frame(self.root, bg="black")
        self.button_frame.pack()
        
        # Main buttons
        self.start_button = ttk.Button(self.button_frame, text="START", style="RoundedButton.TButton",
                                     command=self.start_faceshield)
        self.start_button.pack(pady=(0, 10))
        
        self.quit_button = ttk.Button(self.button_frame, text="QUIT", style="RoundedButton.TButton",
                                    command=self.stop_current_process)
        
        self.register_button = ttk.Button(self.button_frame, text="REGISTER", style="RoundedButton.TButton",
                                        command=self.run_register_script)
        self.register_button.pack(pady=(10, 0))
        
        # Log control frame (above the log box)
        self.log_control_frame = tk.Frame(self.root, bg="black")
        self.log_control_frame.pack(pady=(20, 0))
        
        # Small toggle button (now above the log box)
        self.toggle_log_btn = ttk.Button(self.log_control_frame, text="Hide Log", style="Small.TButton",
                                       command=self.toggle_log)
        self.toggle_log_btn.pack()
        
        # Log box frame (to maintain consistent layout)
        self.log_frame = tk.Frame(self.root, bg="black")
        self.log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log box
        self.log_box = tk.Text(self.log_frame, height=10, width=60, bg="black", fg="pink")
        self.log_box.pack(fill=tk.BOTH, expand=True)
        self.log_box.configure(state='disabled')
        
        # Website link (packed after log frame)
        self.link_label = tk.Label(self.root, text="kmoku.ru/FaceShield", font=("Montserrat", 10), 
                       fg="#FF80AB", bg="black", cursor="hand2")
        self.link_label.pack(pady=10)
        self.link_label.bind("<Button-1>", lambda e: os.system("start https://kmoku.ru/FaceShield"))
    
    def toggle_log(self):
        self.log_visible = not self.log_visible
        if self.log_visible:
            self.log_box.pack(fill=tk.BOTH, expand=True)
            self.toggle_log_btn.config(text="Hide Log")
        else:
            self.log_box.pack_forget()
            self.toggle_log_btn.config(text="Show Log")
    
    def start_faceshield(self):
        self.show_quit_button()
        threading.Thread(target=self.stream_output, args=("main.py",), daemon=True).start()
    
    def run_register_script(self):
        self.show_quit_button()
        threading.Thread(target=self.stream_output, args=("register.py",), daemon=True).start()
    
    def stream_output(self, script_name):
        self.current_process = subprocess.Popen(
            [sys.executable, os.path.join(os.getcwd(), script_name)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1, creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        for line in self.current_process.stdout:
            if self.log_visible:
                self.log_box.configure(state='normal')
                self.log_box.insert(tk.END, line)
                self.log_box.see(tk.END)
                self.log_box.configure(state='disabled')
        
        self.current_process.stdout.close()
        self.current_process.wait()
        self.show_main_buttons()
    
    def stop_current_process(self):
        if self.current_process:
            self.current_process.terminate()
        self.show_main_buttons()
    
    def show_quit_button(self):
        self.start_button.pack_forget()
        self.register_button.pack_forget()
        self.quit_button.pack(pady=10)
    
    def show_main_buttons(self):
        self.quit_button.pack_forget()
        self.start_button.pack(pady=(0, 10))
        self.register_button.pack(pady=(10, 0))

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceShieldGUI(root)
    root.mainloop()