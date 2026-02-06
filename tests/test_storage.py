from datetime import date
from src.services.storage import ExcelStorage
from src.models.record import WorkRecord
import os

def test_storage():
    print("Testing Storage...")
    test_file = "test_work_reports.xlsx"
    if os.path.exists(test_file):
        os.remove(test_file)
        
    storage = ExcelStorage(test_file)
    
    # 1. Create
    r1 = WorkRecord(date=date(2023, 10, 27), project_name="ProjA", summary="Summary 1", details="Details 1")
    storage.save_record(r1)
    print("Saved Record 1")
    
    # 2. Read
    records = storage.get_records_by_date(date(2023, 10, 27))
    assert len(records) == 1
    assert records[0][1].project_name == "ProjA"
    print("Verified Read")
    
    # 3. Update (Assuming row 2 since row 1 is header)
    row_idx = records[0][0]
    r1_updated = WorkRecord(date=date(2023, 10, 27), project_name="ProjA-Updated", summary="Summary 1", details="Details 1")
    storage.update_record_by_row(row_idx, r1_updated)
    
    records_updated = storage.get_records_by_date(date(2023, 10, 27))
    assert records_updated[0][1].project_name == "ProjA-Updated"
    print("Verified Update")
    
    # 4. Delete
    storage.delete_record_by_row(row_idx)
    records_deleted = storage.get_records_by_date(date(2023, 10, 27))
    assert len(records_deleted) == 0
    print("Verified Delete")
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
    print("Test Passed!")

if __name__ == "__main__":
    test_storage()
