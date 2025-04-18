import pandas as pd
from apartment_data_db_mysql import ApartmentDataDatabase  
import os
from tkinter import filedialog
import openpyxl

def show_data():
    handler = ApartmentDataDatabase()
    data = handler.fetch_data_from_db()
    handler.close()
    
    # Adataid list of tuples formában jönnek [(dátum, ár1, ár2, ár3), ...]
    df = pd.DataFrame(data, columns=[
        'Date', 
        'Universal sqm price HUF', 
        'Universal sqm price EUR', 
        'One million HUF to EUR'
    ])
    
    # Mentés Excelbe
    save_path = filedialog.asksaveasfilename(defaultextension='.xlsx', 
                                              filetypes=[("Excel files", "*.xlsx")],
                                              title="Save data as Excel file")
    if save_path:
        df.to_excel(save_path, index=False)
        print("file saved")
#        success_label.config(text=f"Data saved to {os.path.basename(save_path)}!")
        os.startfile(save_path)  # automatikusan megnyitja a fájlt

    else:
        print("file not saved")
#        success_label.config(text="Save cancelled.")

