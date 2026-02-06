import calendar
from datetime import date, timedelta
import customtkinter as ctk
from typing import Callable

class CalendarFrame(ctk.CTkFrame):
    """
    Displays a monthly calendar.
    Allows navigating months and selecting a date.
    """
    def __init__(self, master, on_date_click: Callable[[date], None], **kwargs):
        super().__init__(master, **kwargs)
        self.on_date_click = on_date_click
        self.current_date = date.today()
        self.selected_date = None
        
        # Header (Month Year + Navigation)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        self.btn_prev = ctk.CTkButton(self.header_frame, text="<", width=30, command=self.prev_month)
        self.btn_prev.pack(side="left")
        
        self.lbl_month = ctk.CTkLabel(self.header_frame, text="Month Year", font=("Arial", 16, "bold"))
        self.lbl_month.pack(side="left", expand=True)
        
        self.btn_next = ctk.CTkButton(self.header_frame, text=">", width=30, command=self.next_month)
        self.btn_next.pack(side="right")
        
        # Calendar Grid
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(expand=True, fill="both")
        
        self.day_buttons = []
        self._build_calendar_grid()
        self._update_calendar()

    def _build_calendar_grid(self):
        """Creates the grid layout for days."""
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            lbl = ctk.CTkLabel(self.grid_frame, text=day, font=("Arial", 12, "bold"))
            lbl.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)
            self.grid_frame.grid_columnconfigure(i, weight=1)

    def _update_calendar(self):
        """Refreshes the calendar view for the current month."""
        self.lbl_month.configure(text=self.current_date.strftime("%B %Y"))
        
        # Clear old buttons
        for btn in self.day_buttons:
            btn.destroy()
        self.day_buttons.clear()
        
        # Get calendar days
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day == 0:
                    continue
                
                # Check if today
                is_today = (day == date.today().day and 
                           self.current_date.month == date.today().month and 
                           self.current_date.year == date.today().year)
                
                fg_color = "green" if is_today else None # distinct color for today
                
                dt = date(self.current_date.year, self.current_date.month, day)
                
                btn = ctk.CTkButton(
                    self.grid_frame, 
                    text=str(day),
                    fg_color=fg_color,
                    height=40,
                    command=lambda d=dt: self.on_date_click(d)
                )
                btn.grid(row=r+1, column=c, sticky="nsew", padx=2, pady=2)
                self.day_buttons.append(btn)

    def prev_month(self):
        first = self.current_date.replace(day=1)
        prev_month = first - timedelta(days=1)
        self.current_date = prev_month
        self._update_calendar()

    def next_month(self):
        # Stupid simple next month logic
        days_in_month = calendar.monthrange(self.current_date.year, self.current_date.month)[1]
        next_month = self.current_date + timedelta(days=days_in_month + 1) # simple jump
        self.current_date = next_month.replace(day=1)
        self._update_calendar()
