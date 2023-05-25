from openpyxl import load_workbook, Workbook
import pyexcel
import csv

#conversion to XLSX file
pyexcel.save_book_as(file_name="/home/grzegorz/Dev/bomtocsv/NABR009_OP20_BOM.xls",
                     dest_file_name="/home/grzegorz/Dev/bomtocsv/NABR009_OP20_BOM.xlsx")

workbook = load_workbook("/home/grzegorz/Dev/bomtocsv/NABR009_OP20_BOM.xlsx")

print(workbook.worksheets) 