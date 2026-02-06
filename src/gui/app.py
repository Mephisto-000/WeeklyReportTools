import customtkinter as ctk
from datetime import date
from typing import Optional

from src.services.storage import ExcelStorage
from src.models.record import WorkRecord
from src.gui.frames.calendar_frame import CalendarFrame
from src.gui.frames.records_frame import RecordsFrame
from src.gui.frames.maintenance_frame import MaintenanceFrame
from src.utils.logger import setup_logger

logger = setup_logger("App")

class App(ctk.CTk):
    """
    Main Application Window.
    Orchestrates tabs and data flow.
    """
    def __init__(self):
        super().__init__()
        
        self.title("Weekly Report Tool")
        self.geometry("800x600")
        
        # Services
        self.storage = ExcelStorage()
        
        # UI Setup
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_home = self.tab_view.add("Home (Calendar)")
        self.tab_records = self.tab_view.add("Daily Records")
        self.tab_maint = self.tab_view.add("Maintenance")
        
        # -- Tab 1: Home --
        self.calendar_frame = CalendarFrame(self.tab_home, on_date_click=self.on_date_selected)
        self.calendar_frame.pack(fill="both", expand=True)
        
        # -- Tab 2: Records --
        self.records_frame = RecordsFrame(self.tab_records, 
                                          on_delete=self.delete_record,
                                          on_edit=self.edit_record_request)
        self.records_frame.pack(fill="both", expand=True)
        
        # -- Tab 3: Maintenance --
        self.maintenance_frame = MaintenanceFrame(self.tab_maint, on_save=self.save_record)
        self.maintenance_frame.pack(fill="both", expand=True)

    def on_date_selected(self, selected_date: date):
        """Called when a date is clicked in the calendar."""
        logger.info(f"Date selected: {selected_date}")
        self.tab_view.set("Daily Records")
        self.load_records_for_date(selected_date)

    def load_records_for_date(self, target_date: date):
        """Fetches records and updates the view."""
        records = self.storage.get_records_by_date(target_date)
        self.records_frame.display_records(target_date, records)

    def save_record(self, record: WorkRecord, row_index: Optional[int]):
        """Callback from Maintenance frame to save data."""
        if row_index:
            self.storage.update_record_by_row(row_index, record)
        else:
            self.storage.save_record(record)
        
        # Refresh views if needed
        # Switch to records view to show the new record? 
        # Or stay on maintenance?
        # Let's switch to the date of the record we just saved/edited
        self.tab_view.set("Daily Records")
        self.load_records_for_date(record.date)

    def delete_record(self, row_index: int):
        """Callback to delete a record."""
        # Confirmation dialog could go here
        self.storage.delete_record_by_row(row_index)
        
        # Refresh current view
        if self.records_frame.current_date:
            self.load_records_for_date(self.records_frame.current_date)

    def edit_record_request(self, row_index: int, record: WorkRecord):
        """Callback to initiate edit."""
        self.tab_view.set("Maintenance")
        self.maintenance_frame.load_record(record, row_index)
