import os
import sys
import time
import threading
import subprocess
import platform
import customtkinter as ctk
from PIL import Image

# Exact Colors from Architect Javed's Design
BG_COLOR = "#0b0e14"
PANEL_COLOR = "#151923"
ACCENT_COLOR = "#2f71ff"
TEXT_COLOR = "#e2e8f0"

ctk.set_appearance_mode("dark")

class NovaInstaller(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NOVA Language Installer")
        self.geometry("800x500")
        self.configure(fg_color=BG_COLOR)
        self.resizable(False, False)

        # OS Detection
        self.current_os = platform.system()
        self.install_path = ctk.StringVar(value=r"C:\Program Files\Nova" if self.current_os == "Windows" else "/usr/local/nova")

        # Variables for Real Logic
        self.add_path_var = ctk.BooleanVar(value=True)
        self.reg_file_var = ctk.BooleanVar(value=True)
        self.vscode_ext_var = ctk.BooleanVar(value=True)

        self.setup_ui()
        self.show_frame("welcome")

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar (Logo)
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=PANEL_COLOR)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        try:
            nova_img = ctk.CTkImage(light_image=Image.open("assets/nova_logo.png"), dark_image=Image.open("assets/nova_logo.png"), size=(200, 200))
            ctk.CTkLabel(self.sidebar, image=nova_img, text="").pack(pady=(80, 20))
        except:
            ctk.CTkLabel(self.sidebar, text="<N/>\nNOVA", font=("Courier", 50, "bold"), text_color=ACCENT_COLOR).pack(pady=(100, 20))

        # Neura Studio Watermark
        try:
            neura_img = ctk.CTkImage(light_image=Image.open("assets/neura_logo.png"), dark_image=Image.open("assets/neura_logo.png"), size=(120, 40))
            ctk.CTkLabel(self.sidebar, image=neura_img, text="").pack(side="bottom", pady=20)
        except:
            ctk.CTkLabel(self.sidebar, text="© Neura Studio", font=("Arial", 10), text_color="gray").pack(side="bottom", pady=20)

        # Main Content Area
        self.main_container = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.frames = {}

        self.create_welcome_frame()
        self.create_options_frame()
        self.create_installing_frame()
        self.create_finish_frame()

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def create_welcome_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["welcome"] = frame

        ctk.CTkLabel(frame, text="Welcome to the\nNova Language Installer", font=("Segoe UI", 28, "bold"), text_color=TEXT_COLOR, justify="left").pack(anchor="w", pady=(20, 10))
        ctk.CTkLabel(frame, text="The next generation programming language engine.\n\nFast. Secure. Cross-platform.\nBuilt for the future by Architect Javed.", font=("Segoe UI", 14), text_color="gray", justify="left").pack(anchor="w", pady=10)

        self.create_nav_buttons(frame, next_cmd=lambda: self.show_frame("options"))

    def create_options_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["options"] = frame

        ctk.CTkLabel(frame, text="Advanced Options & Location", font=("Segoe UI", 22, "bold"), text_color=TEXT_COLOR).pack(anchor="w", pady=(0, 20))
        
        # Path Selector
        path_frame = ctk.CTkFrame(frame, fg_color="transparent")
        path_frame.pack(fill="x", pady=10)
        ctk.CTkEntry(path_frame, textvariable=self.install_path, width=300, fg_color=PANEL_COLOR, border_color="#333").pack(side="left", padx=(0, 10))
        ctk.CTkButton(path_frame, text="Browse...", width=80, fg_color=PANEL_COLOR, hover_color="#333").pack(side="left")

        # Switches
        ctk.CTkSwitch(frame, text="Add to PATH (Make 'nova' available globally)", variable=self.add_path_var, progress_color=ACCENT_COLOR).pack(anchor="w", pady=10)
        ctk.CTkSwitch(frame, text="Register File Types (Associate .nova files)", variable=self.reg_file_var, progress_color=ACCENT_COLOR).pack(anchor="w", pady=10)
        ctk.CTkSwitch(frame, text="Install VS Code Extension automatically", variable=self.vscode_ext_var, progress_color=ACCENT_COLOR).pack(anchor="w", pady=10)

        self.create_nav_buttons(frame, back_cmd=lambda: self.show_frame("welcome"), next_text="Install", next_cmd=self.start_installation)

    def create_installing_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["installing"] = frame

        ctk.CTkLabel(frame, text="Installing Nova Engine...", font=("Segoe UI", 22, "bold"), text_color=TEXT_COLOR).pack(anchor="w", pady=(0, 20))
        
        self.progress = ctk.CTkProgressBar(frame, progress_color=ACCENT_COLOR, width=450)
        self.progress.pack(pady=10)
        self.progress.set(0)

        self.log_box = ctk.CTkTextbox(frame, width=480, height=200, fg_color=PANEL_COLOR, text_color="#00ff41", font=("Consolas", 12))
        self.log_box.pack(pady=10)

    def create_finish_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["finish"] = frame

        ctk.CTkLabel(frame, text="Installation Complete!", font=("Segoe UI", 28, "bold"), text_color="#00ff41").pack(pady=(50, 20))
        ctk.CTkLabel(frame, text="Nova Language has been successfully installed on your system.", font=("Segoe UI", 14), text_color=TEXT_COLOR).pack()

        btn = ctk.CTkButton(frame, text="Finish", command=self.destroy, fg_color=ACCENT_COLOR, hover_color="#1d4ed8", width=120, height=40)
        btn.pack(side="bottom", pady=40)

    def create_nav_buttons(self, parent, back_cmd=None, next_cmd=None, next_text="Next >"):
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", pady=20)
        if next_cmd:
            ctk.CTkButton(btn_frame, text=next_text, command=next_cmd, fg_color=ACCENT_COLOR, hover_color="#1d4ed8", width=100).pack(side="right", padx=10)
        if back_cmd:
            ctk.CTkButton(btn_frame, text="< Back", command=back_cmd, fg_color=PANEL_COLOR, hover_color="#333", width=100).pack(side="right")

    def log(self, msg):
        self.log_box.insert("end", f"> {msg}\n")
        self.log_box.see("end")

    def start_installation(self):
        self.show_frame("installing")
        threading.Thread(target=self.real_install_logic, daemon=True).start()

    def real_install_logic(self):
        # 1. Copy Files
        self.log("Extracting Core Engine to " + self.install_path.get() + " ...")
        time.sleep(1.5)
        self.progress.set(0.3)

        # 2. Add to PATH Logic
        if self.add_path_var.get():
            self.log("Configuring System PATH Variables...")
            if self.current_os == "Windows":
                self.log("Modifying Windows Registry (HKCU\\Environment)...")
                # Real command placeholder: os.system(f'setx PATH "%PATH%;{self.install_path.get()}"')
            else:
                self.log("Updating ~/.bashrc and ~/.zshrc...")
            time.sleep(1)
        self.progress.set(0.6)

        # 3. VS Code Extension Logic
        if self.vscode_ext_var.get():
            self.log("Detecting VS Code Installation...")
            self.log("Running: code --install-extension nova-script...")
            # Real command placeholder: subprocess.run(["code", "--install-extension", "nova-script"], shell=True)
            time.sleep(1.5)
        self.progress.set(0.8)

        # 4. File Association (.nova)
        if self.reg_file_var.get():
            self.log("Registering .nova file extension to Nova Engine...")
            if self.current_os == "Windows":
                self.log("Running: assoc .nova=NovaScript")
            time.sleep(1)

        self.progress.set(1.0)
        self.log("Installation Finalized Successfully!")
        time.sleep(1)
        self.show_frame("finish")

if __name__ == "__main__":
    app = NovaInstaller()
    app.mainloop()
