import openpyxl


fichier = openpyxl.load_workbook("fichier_test.xlsx")
for sheet in fichier:
    print("Nom: " + str(sheet.title))
