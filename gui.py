import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import sys
import threading
import socket

try:
    import main
except ImportError:
    import __main__ as main  # fallback if bundled

# Handle safe path for Routes.json
if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
    ROUTES_FILE = os.path.join(os.path.dirname(sys.executable), "Routes.json")
else:
    BASE_PATH = os.path.abspath(".")
    ROUTES_FILE = os.path.join("Routes.json")

class TapTriggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TapTrigger")
        self.root.geometry("700x700")
        self.root.configure(bg="#670303")

        icon_file = os.path.join(BASE_PATH, "TapTrigger.ico")
        if os.path.exists(icon_file):
            try:
                self.root.iconbitmap(icon_file)
            except:
                pass

        self.routes = self.load_routes()

        title_label = tk.Label(root, text="TapTrigger - Beta Version", font=("Arial", 24, "bold"), fg="white", bg="#670303")
        title_label.pack(pady=(10, 5))

        subtitle_label = tk.Label(root, text="Developed By Vishnu Ganesh", font=("Arial", 12), fg="white", bg="#670303")
        subtitle_label.pack(pady=(0, 20))

        self.create_input_section()
        self.create_routes_section()
        self.create_buttons()

    def create_input_section(self):
        input_frame = tk.Frame(self.root, bg="#670303")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Add New Route", font=("Arial", 14, "bold"), fg="white", bg="#670303").pack(pady=10)

        self.trigger_entry = tk.Entry(input_frame, bg="pink")
        self.trigger_entry.pack(pady=5)

        self.action_type = tk.StringVar(value="launch")
        type_frame = tk.Frame(input_frame, bg="#670303")
        type_frame.pack()

        tk.Radiobutton(type_frame, text="Launch Program", variable=self.action_type, value="launch",
                       bg="#670303", fg="white", selectcolor="#670303", activebackground="#670303").pack(side="left")

        tk.Radiobutton(type_frame, text="Type Text", variable=self.action_type, value="type",
                       bg="#670303", fg="white", selectcolor="#670303", activebackground="#670303").pack(side="left")

        self.path_entry = tk.Entry(input_frame, bg="pink")
        self.path_entry.pack(pady=5)

        tk.Button(input_frame, text="Browse Program", command=self.browse_file, bg="maroon", fg="white").pack(pady=5)
        tk.Button(input_frame, text="Save Route", command=self.save_route, bg="maroon", fg="white").pack(pady=5)

    def create_routes_section(self):
        section_frame = tk.Frame(self.root, bg="#670303")
        section_frame.pack(pady=10)

        tk.Label(section_frame, text="Saved Routes", font=("Arial", 14, "bold"), fg="white", bg="#670303").pack(pady=5)

        self.routes_listbox = tk.Listbox(section_frame, bg="pink", width=60, height=10)
        self.routes_listbox.pack(pady=5)
        self.refresh_routes()

    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#670303")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Delete Selected Route", command=self.delete_route, bg="maroon", fg="white").pack(pady=5)
        tk.Button(btn_frame, text="Run Server", command=self.run_server, bg="maroon", fg="white").pack(pady=5)
        tk.Button(btn_frame, text="Instructions", command=self.show_instructions, bg="maroon", fg="white").pack(pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")])
        if file_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, file_path)

    def save_route(self):
        name = self.trigger_entry.get().strip()
        action_type = self.action_type.get()
        action = self.path_entry.get().strip()

        if not name or not action:
            messagebox.showerror("Error", "Both trigger name and action are required.")
            return

        self.routes[name] = {"type": action_type, "action": action}
        self.write_routes()
        self.refresh_routes()
        self.trigger_entry.delete(0, tk.END)
        self.path_entry.delete(0, tk.END)

    def delete_route(self):
        selected = self.routes_listbox.curselection()
        if not selected:
            return
        trigger_name = self.routes_listbox.get(selected[0]).split(" → ")[0]
        if trigger_name in self.routes:
            del self.routes[trigger_name]
            self.write_routes()
            self.refresh_routes()

    def refresh_routes(self):
        self.routes_listbox.delete(0, tk.END)
        for key, value in self.routes.items():
            self.routes_listbox.insert(tk.END, f"{key} → {value['type']}:{value['action']}")

    def load_routes(self):
        if not os.path.exists(ROUTES_FILE):
            return {}
        with open(ROUTES_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def write_routes(self):
        with open(ROUTES_FILE, "w") as f:
            json.dump(self.routes, f, indent=4)

    def run_server(self):
        server_thread = threading.Thread(target=main.start_server, daemon=True)
        server_thread.start()

    def show_instructions(self):
        ip = socket.gethostbyname(socket.gethostname())
        top = tk.Toplevel(self.root)
        top.title("Phone Setup Instructions")
        top.geometry("550x350")
        top.configure(bg="#670303")

        trigger_list = "\n".join([f"- {key}" for key in self.routes.keys()]) or "No triggers yet."
        url_example = f"http://{ip}:8000/trigger?trigger=YourTriggerName"

        instructions = (
            "1. Ensure your iPhone is connected to the same Wi-Fi/LAN as this PC.\n"
            "2. Open the Shortcuts app and create a new Automation using any trigger method.\n"
            "3. Add 'Get Contents of URL' as the action.\n"
            f"4. Use this URL:\n   {url_example}\n"
            "5. Replace 'YourTriggerName' with one of your triggers below:\n"
            f"{trigger_list}"
        )

        tk.Label(top, text="Trigger Setup Instructions", font=("Arial", 14, "bold"), fg="white", bg="#670303").pack(pady=10)
        tk.Label(top, text=instructions, font=("Arial", 10), fg="white", bg="#670303", justify="left", anchor="w").pack(padx=10, anchor="w")

if __name__ == "__main__":
    root = tk.Tk()
    app = TapTriggerGUI(root)
    root.mainloop()
