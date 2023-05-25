from openpyxl import load_workbook, Workbook
import pyexcel
import csv

xls_bom = "/home/grzegorz/Dev/bomtocsv/NABR009_OP20_BOM.xls"
xlsx_bom = "/home/grzegorz/Dev/bomtocsv/NABR009_OP20_BOM.xlsx"

#conversion to XLSX file
def convert_xls_to_xlsx(xls_path, xlsx_path):
    pyexcel.save_book_as(file_name=xls_path,
                        dest_file_name=xlsx_path)

workbook = load_workbook("/home/grzegorz/Dev/bomtocsv/NABR009_OP20_BOM.xlsx")

print(workbook.worksheets) 