import customtkinter as ctk
from datetime import date
from typing import List, Callable
from src.models.record import WorkRecord

class RecordsFrame(ctk.CTkFrame):
    """
    Displays a list of work records for a specific date.
    """
    def __init__(self, master, 
                 on_delete: Callable[[int], None], 
                 on_edit: Callable[[int, WorkRecord], None],
                 **kwargs):
        super().__init__(master, **kwargs)
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.current_date = None
        
        # Header
        self.lbl_date = ctk.CTkLabel(self, text="Select a date to view records", font=("Arial", 16, "bold"))
        self.lbl_date.pack(pady=10)
        
        # Scrollable list
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def display_records(self, target_date: date, records: List[tuple[int, WorkRecord]]):
        """Populates the list with records."""
        self.current_date = target_date
        self.lbl_date.configure(text=f"Records for {target_date.strftime('%Y-%m-%d')}")
        
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        if not records:
            ctk.CTkLabel(self.scroll_frame, text="No records found.").pack(pady=20)
            return

        # Headers
        # Simple headers
        header_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(header_frame, text="Project", width=100, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Summary", width=200, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        
        # Rows
        for row_idx, record in records:
            self._create_record_row(row_idx, record)

    def _create_record_row(self, row_idx: int, record: WorkRecord):
        frame = ctk.CTkFrame(self.scroll_frame)
        frame.pack(fill="x", pady=2)
        
        # Project
        ctk.CTkLabel(frame, text=record.project_name, width=100, anchor="w").pack(side="left", padx=5)
        
        # Summary
        ctk.CTkLabel(frame, text=record.summary, width=200, anchor="w").pack(side="left", padx=5)
        
        # Actions
        btn_del = ctk.CTkButton(frame, text="Del", width=40, fg_color="red", 
                                command=lambda r=row_idx: self.on_delete(r))
        btn_del.pack(side="right", padx=5)
        
        btn_edit = ctk.CTkButton(frame, text="Edit", width=40, 
                                 command=lambda r=row_idx, rec=record: self.on_edit(r, rec))
        btn_edit.pack(side="right", padx=5)
