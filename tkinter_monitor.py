import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime
import time
import threading


class DataAirflowMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Airflow Monitor")
        self.root.geometry("900x620")
        self.root.configure(bg="#1e1e1e")

        # Change this if needed
        self.API_URL = "http://192.168.1.218:8000"

        self.create_widgets()
        self.reset_and_refresh()   # Called on startup

    def create_widgets(self):
        # ===== Header =====
        header = tk.Frame(self.root, bg="#1e1e1e", pady=10)
        header.pack(fill="x", padx=15)

        title = tk.Label(
            header,
            text="Data Airflow Monitor",
            font=("Segoe UI", 18, "bold"),
            fg="#ffffff",
            bg="#1e1e1e"
        )
        title.pack(side="left")

        self.conn_label = tk.Label(
            header,
            text="● Connecting...",
            font=("Segoe UI", 11),
            fg="#f39c12",
            bg="#1e1e1e"
        )
        self.conn_label.pack(side="right")

        # ===== Console (Activity Log) =====
        console_frame = tk.Frame(self.root, bg="#1e1e1e")
        console_frame.pack(fill="both", expand=True, padx=15, pady=(5, 10))

        console_label = tk.Label(
            console_frame,
            text="Activity Console",
            font=("Segoe UI", 10, "bold"),
            fg="#aaaaaa",
            bg="#1e1e1e",
            anchor="w"
        )
        console_label.pack(fill="x")

        # Scrollable Text widget
        self.log = tk.Text(
            console_frame,
            bg="#121212",
            fg="#e0e0e0",
            insertbackground="white",
            font=("Consolas", 10),
            wrap="word",
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.log.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(console_frame, orient="vertical", command=self.log.yview)
        scrollbar.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=scrollbar.set)

        # ===== Buttons =====
        btn_frame = tk.Frame(self.root, bg="#1e1e1e", pady=10)
        btn_frame.pack(fill="x", padx=15)

        self.run_btn = tk.Button(
            btn_frame,
            text="▶  Run File Pipeline",
            command=self.run_file_pipeline,
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2"
        )
        self.run_btn.pack(side="left", padx=(0, 10))

        self.refresh_btn = tk.Button(
            btn_frame,
            text="⟳  Reset & Refresh",
            command=self.reset_and_refresh,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2"
        )
        self.refresh_btn.pack(side="left")

    # ------------------------------------------------------------------
    # Logging helper
    # ------------------------------------------------------------------
    def log_message(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_tags = {
            "INFO": "#e0e0e0",
            "SUCCESS": "#2ecc71",
            "ERROR": "#e74c3c",
            "WARNING": "#f39c12",
            "STEP": "#3498db"
        }

        tag = level
        self.log.tag_config(tag, foreground=color_tags.get(level, "#e0e0e0"))

        self.log.insert("end", f"[{timestamp}] {message}\n", tag)
        self.log.see("end")          # Auto-scroll to bottom
        self.root.update_idletasks()

    # ------------------------------------------------------------------
    # Reset + Refresh (also used on startup)
    # ------------------------------------------------------------------
    def reset_and_refresh(self):
        self.log.delete("1.0", "end")
        self.log_message("Resetting application...", "INFO")
        self.log_message(f"Connecting to server: {self.API_URL}", "INFO")

        self.conn_label.config(text="● Connecting...", fg="#f39c12")

        try:
            response = requests.get(f"{self.API_URL}/metrics", timeout=5)
            data = response.json()

            if data.get("status") in ("ok", "no_data"):
                self.conn_label.config(text="● Connected", fg="#2ecc71")
                self.log_message("Successfully connected to FastAPI server", "SUCCESS")

                records = data.get("records_in_storage", 0)
                self.log_message(f"Current records in storage: {records}", "INFO")

                if data.get("last_updated"):
                    self.log_message(f"Last updated: {data.get('last_updated')[:19]}", "INFO")
            else:
                self.conn_label.config(text="● Error", fg="#e74c3c")
                self.log_message(f"Server returned unexpected status: {data}", "ERROR")

        except Exception as e:
            self.conn_label.config(text="● Offline", fg="#e74c3c")
            self.log_message(f"Failed to connect to server: {e}", "ERROR")

    # ------------------------------------------------------------------
    # Run File Pipeline (now fully client → server)
    # ------------------------------------------------------------------
    def run_file_pipeline(self):
        self.run_btn.config(state="disabled")
        self.conn_label.config(text="● Running pipeline...", fg="#3498db")

        def task():
            try:
                self.log_message("Sending request to server to run File Pipeline...", "INFO")
                self.log_message("Waiting for server to process records...", "STEP")

                # Simulated live progress (makes the process feel longer)
                for i in range(1, 6):
                    time.sleep(0.4)
                    self.log_message(f"Processing batch {i}/5 ...", "STEP")

                response = requests.post(f"{self.API_URL}/run-pipeline", timeout=30)
                result = response.json()

                if result.get("status") == "success":
                    rows = result.get("rows_created", 0)
                    self.log_message(f"Pipeline completed successfully", "SUCCESS")
                    self.log_message(f"Records generated: {rows}", "SUCCESS")
                    self.log_message("Refreshing metrics from server...", "INFO")

                    # Auto refresh after success
                    self.root.after(0, self.reset_and_refresh)
                else:
                    error_msg = result.get("message", "Unknown error from server")
                    self.log_message(f"Server error: {error_msg}", "ERROR")

            except Exception as e:
                self.log_message(f"Request failed: {e}", "ERROR")

            finally:
                self.root.after(0, lambda: self.run_btn.config(state="normal"))
                self.root.after(0, lambda: self.conn_label.config(text="● Connected", fg="#2ecc71"))

        # Run in background thread so UI stays responsive
        threading.Thread(target=task, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = DataAirflowMonitor(root)
    root.mainloop()