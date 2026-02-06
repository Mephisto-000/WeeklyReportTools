import customtkinter as ctk
from datetime import date
from src.models.record import WorkRecord
from typing import Callable, Optional

class MaintenanceFrame(ctk.CTkFrame):
    """
    Form to add or edit work records.
    """
    def __init__(self, master, on_save: Callable[[WorkRecord, Optional[int]], None], **kwargs):
        super().__init__(master, **kwargs)
        self.on_save = on_save
        self.editing_row_index: Optional[int] = None # If set, we are editing
        
        # Title
        self.lbl_title = ctk.CTkLabel(self, text="Add New Record", font=("Arial", 18, "bold"))
        self.lbl_title.pack(pady=10)
        
        # Form Container
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Date
        ctk.CTkLabel(self.form_frame, text="Date (YYYY-MM-DD):").pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_date = ctk.CTkEntry(self.form_frame)
        self.entry_date.pack(fill="x", padx=10, pady=(0, 10))
        self.entry_date.insert(0, date.today().isoformat())
        
        # Project
        ctk.CTkLabel(self.form_frame, text="Project Name:").pack(anchor="w", padx=10)
        self.entry_project = ctk.CTkEntry(self.form_frame)
        self.entry_project.pack(fill="x", padx=10, pady=(0, 10))
        
        # Summary
        ctk.CTkLabel(self.form_frame, text="Summary:").pack(anchor="w", padx=10)
        self.entry_summary = ctk.CTkEntry(self.form_frame)
        self.entry_summary.pack(fill="x", padx=10, pady=(0, 10))
        
        # Details
        ctk.CTkLabel(self.form_frame, text="Details:").pack(anchor="w", padx=10)
        self.txt_details = ctk.CTkTextbox(self.form_frame, height=100)
        self.txt_details.pack(fill="x", padx=10, pady=(0, 10))
        
        # Buttons
        self.btn_save = ctk.CTkButton(self, text="Save Record", command=self.save)
        self.btn_save.pack(pady=10)
        
        self.btn_clear = ctk.CTkButton(self, text="Clear Form", fg_color="gray", command=self.clear_form)
        self.btn_clear.pack(pady=(0, 10))

    def load_record(self, record: WorkRecord, row_index: int):
        """Loads a record into the form for editing."""
        self.editing_row_index = row_index
        self.lbl_title.configure(text="Edit Record")
        
        self.entry_date.delete(0, "end")
        self.entry_date.insert(0, record.date.isoformat())
        
        self.entry_project.delete(0, "end")
        self.entry_project.insert(0, record.project_name)
        
        self.entry_summary.delete(0, "end")
        self.entry_summary.insert(0, record.summary)
        
        self.txt_details.delete("0.0", "end")
        self.txt_details.insert("0.0", record.details)

    def clear_form(self):
        """Resets the form to default state."""
        self.editing_row_index = None
        self.lbl_title.configure(text="Add New Record")
        
        self.entry_date.delete(0, "end")
        self.entry_date.insert(0, date.today().isoformat())
        
        self.entry_project.delete(0, "end")
        self.entry_summary.delete(0, "end")
        self.txt_details.delete("0.0", "end")

    def save(self):
        """Collects data and triggers save callback."""
        try:
            d_str = self.entry_date.get()
            d = date.fromisoformat(d_str)
            
            record = WorkRecord(
                date=d,
                project_name=self.entry_project.get(),
                summary=self.entry_summary.get(),
                details=self.txt_details.get("0.0", "end").strip()
            )
            
            self.on_save(record, self.editing_row_index)
            self.clear_form() # optionally clear after save
            
        except ValueError:
            # Simple error handling for date
            print("Invalid date format") # In real app, show message box
