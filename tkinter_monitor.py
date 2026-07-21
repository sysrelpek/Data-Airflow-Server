import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import os
import sys

# Add project root so we can still use local services for the "Run" button
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.business_lib.services.generate_test_data_service import GenerateTestDataService
from src.business_lib.infrastructure.storage.json_adapter import JsonAdapter


class DataAirflowMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Airflow Monitor")
        self.root.geometry("820x560")
        self.root.configure(bg="#f4f4f4")

        # Change this to your server's IP if you run Tkinter from another machine
        # self.API_URL = "http://localhost:8000"
        self.API_URL = "http://192.168.1.218:8000"

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground="#2c3e50")
        style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1)
        style.configure("Metric.TLabel", font=("Segoe UI", 15, "bold"))

        self.create_widgets()
        self.refresh_data()

    def create_widgets(self):
        # Header
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")
        ttk.Label(header, text="🚀 Data Airflow Monitor", style="Title.TLabel").pack(side="left")
        self.conn_label = ttk.Label(header, text="● Connecting...", foreground="orange")
        self.conn_label.pack(side="right")

        # Metrics Cards
        metrics_frame = ttk.Frame(self.root, padding=10)
        metrics_frame.pack(fill="x", padx=10)

        self.metric_vars = {
            "Records in Storage": tk.StringVar(value="—"),
            "Last Updated": tk.StringVar(value="—"),
            "Server Status": tk.StringVar(value="—")
        }

        for i, (label, var) in enumerate(self.metric_vars.items()):
            card = ttk.Frame(metrics_frame, style="Card.TFrame", padding=12)
            card.grid(row=0, column=i, padx=8, sticky="nsew")
            ttk.Label(card, text=label, font=("Segoe UI", 10)).pack()
            ttk.Label(card, textvariable=var, style="Metric.TLabel").pack(pady=3)

        # Activity Log
        log_frame = ttk.LabelFrame(self.root, text="Recent Activity", padding=8)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log = tk.Text(log_frame, height=10, font=("Consolas", 10))
        self.log.pack(fill="both", expand=True)

        # Buttons
        btn_frame = ttk.Frame(self.root, padding=12)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="🔄 Refresh from Server", command=self.refresh_data, width=22).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🚀 Run File Pipeline", command=self.run_file_pipeline, width=20).pack(side="left", padx=5)

    def refresh_data(self):
        """Fetch real metrics from the FastAPI server"""
        self.conn_label.config(text="● Connecting...", foreground="orange")
        self.log.delete("1.0", "end")

        try:
            response = requests.get(f"{self.API_URL}/metrics", timeout=5)
            data = response.json()

            if data.get("status") == "ok":
                self.metric_vars["Records in Storage"].set(str(data.get("records_in_storage", 0)))
                self.metric_vars["Last Updated"].set(str(data.get("last_updated", "—"))[:19])
                self.metric_vars["Server Status"].set("Connected")
                self.conn_label.config(text="● Connected to Server", foreground="#27ae60")

                self.log.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] Fetched real data from FastAPI server\n")
                self.log.insert("end", f"Records currently in storage: {data.get('records_in_storage')}\n")
            else:
                self.metric_vars["Records in Storage"].set("0")
                self.metric_vars["Server Status"].set("No Data Yet")
                self.conn_label.config(text="● No Data Yet", foreground="#f39c12")
                self.log.insert("end", "No data in storage yet. Run the pipeline first.\n")

        except requests.exceptions.RequestException as e:
            self.metric_vars["Server Status"].set("Offline")
            self.conn_label.config(text="● Cannot Reach Server", foreground="#e74c3c")
            self.log.insert("end", f"Connection error: {e}\n")
            messagebox.showwarning("Connection Error", "Could not connect to FastAPI server.\nIs it still running?")

    def run_file_pipeline(self):
        """Run the pipeline locally (still uses local services for now)"""
        self.conn_label.config(text="● Running pipeline...", foreground="#3498db")

        try:
            demo_path = "./demo_storage"
            os.makedirs(demo_path, exist_ok=True)

            storage = JsonAdapter(base_path=demo_path, file_name="demo_run")
            gen_service = GenerateTestDataService(storage=storage)

            result = gen_service.generate(
                rows=50,
                schema={
                    "id": "integer",
                    "name": "string",
                    "created_at": "timestamp",
                    "amount": "float"
                }
            )

            if result.get("status") == "success":
                messagebox.showinfo("Success", f"Pipeline completed!\nRecords generated: {result.get('rows_created')}")
                self.refresh_data()  # Pull fresh data from server after run
            else:
                messagebox.showerror("Error", result.get("message", "Unknown error"))

        except Exception as e:
            messagebox.showerror("Pipeline Error", str(e))
        finally:
            self.conn_label.config(text="● Connected to Server", foreground="#27ae60")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataAirflowMonitor(root)
    root.mainloop()