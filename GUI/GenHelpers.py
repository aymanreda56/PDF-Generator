import docx
import docx.document
import numpy as np
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import RGBColor, Pt
from docx.enum.table import WD_TABLE_DIRECTION, WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from math import floor
from datetime import date
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import helpers
import enums
import docx2pdf




days_map = {0: 'الإثنين', 1: "الثلاثاء", 2: "الأربعاء", 3: "الخميس", 4: "الجمعة", 5: "السبت", 6:"الأحد"}

arabic_numbers={'0':'٠', '1':'١', '2': '٢', '3':'٣', '4':'٤', '5':'٥', '6':'٦', '7':'٧', '8':'٨', '9':'٩'}


def translate_all_numbers_to_arabic(English_text):
    arabicText=list(English_text)
    for i,c in enumerate(English_text):
        if c in list('0123456789'):
            arabicText[i] = arabic_numbers[c]
        elif c == '-':
            arabicText[i] = '/'
        else:
            arabicText[i] = c
    
    return ''.join(arabicText)


Department_Name = "إدارة المتابعة"
Vacation_Begin_Hour = '900'
Vacation_End_Hour = '1000'
Date_Arabic =translate_all_numbers_to_arabic(date.today().isoformat())
Weekday = days_map[date.today().weekday()]






def replace_placeHolders(fields_to_replace, carrier_object):
    for k,v in fields_to_replace.items():
        carrier_object = carrier_object.replace(k, translate_all_numbers_to_arabic(str(v)))
    return carrier_object


def Replace_Placeholders_Inside_Document(doc, fields_to_replace:dict, Iterable_Fields):
    # Iterate over paragraphs
   
    for section in doc.sections:
        for p in section.header.paragraphs:
            for run in p.runs:
                run.text = replace_placeHolders(fields_to_replace=fields_to_replace, carrier_object=run.text)
                
                

        for p in section.footer.paragraphs:
            for run in p.runs:
                run.text = replace_placeHolders(fields_to_replace=fields_to_replace, carrier_object=run.text)


     
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.text = replace_placeHolders(fields_to_replace=fields_to_replace, carrier_object=run.text)
            

    # Iterate over tables
    Vacations_Table = False
    
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.text = replace_placeHolders(fields_to_replace=fields_to_replace, carrier_object=run.text)
                        if('$LOGO$' in run.text):
                            run.text = ''
                            run.add_picture('../data/logo.png', width=Inches(2.5))
                            cell.alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                        if('$NUM$' in run.text or Vacations_Table == table):
                            Vacations_Table = table
                            break
    
    if(Vacations_Table):
        num_Vacations = len(Iterable_Fields)
        for i in range(num_Vacations-1):
            Vacations_Table.add_row()
        
        counter = 1
        for i, row in enumerate(Vacations_Table.rows):
            
            if(i < 2):
                continue

            j= i-2
            row.cells[5].paragraphs[0].text = Iterable_Fields[j]['To_Date']
            row.cells[4].paragraphs[0].text = Iterable_Fields[j]['From_Date']
            row.cells[3].paragraphs[0].text = "أجازة ميدانية"
            row.cells[1].paragraphs[0].text = Iterable_Fields[j]['Level']
            row.cells[2].paragraphs[0].text = Iterable_Fields[j]['Name']
            row.cells[0].paragraphs[0].text = str(Iterable_Fields[j]['Num'])

            for cell in row.cells:
                cell.style = doc.styles['Strong Par']
                cell.alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER





def Replace_Placeholders_Inside_Vac_Passes(doc, fields_to_replace:list, Iterable_Fields:list):
    # Iterate over tables    
    counter = 0
    for table in doc.tables:
        for row in table.rows:
            for i, cell in enumerate(row.cells):
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        for field in fields_to_replace:
                            if counter < len(Iterable_Fields):
                                run.text = run.text.replace(field, Iterable_Fields[counter][field])
                                print(Iterable_Fields[counter][field])
                            else:
                                run.text = ''
                                
                counter += 1
                        



def Export_Vacation_Passes_PDF():
    AllVacations = helpers.getActiveVacations()

    IterableFieldsDict = []
    for i, tup in enumerate(AllVacations):
        sampleDict = {}
        sampleDict['$SOLDNAME$'] = tup[1]
        sampleDict["$FROM_DATE$"] = translate_all_numbers_to_arabic(tup[2])
        sampleDict["$TO_DATE$"] = translate_all_numbers_to_arabic(tup[3])
        sampleDict['$LEVEL$'] = "جندي" if (enums.ArmyLevels[int(helpers.getLevelFromID(tup[0]))-1] == 'عسكري') else enums.ArmyLevels[int(helpers.getLevelFromID(tup[0]))-1]
        sampleDict["$BH$"] = translate_all_numbers_to_arabic(Vacation_Begin_Hour)
        sampleDict["$EH$"] = translate_all_numbers_to_arabic(Vacation_End_Hour)
        IterableFieldsDict.append(sampleDict)

    fields_to_replace = ["$SOLDNAME$",
                        "$FROM_DATE$",
                        "$TO_DATE$", "$LEVEL$", "$BH$", "$EH$"]

    doccc = docx.Document('../pdf/templates/vacation_passes.docx')
    Replace_Placeholders_Inside_Vac_Passes(doccc, fields_to_replace=fields_to_replace, Iterable_Fields = IterableFieldsDict)
    ConvertAndSave(document=doccc, name="vacation_passes")




def Export_Tamam_PDF():

    number_officers = int(helpers.getNumOfficers())
    absent_officers = len(helpers.getAbsentOfficers())
    present_officers = number_officers - absent_officers



    number_caps = int(helpers.getNumCaps())
    absent_caps = len(helpers.getAbsentCaps())
    present_caps = number_caps - absent_caps


    number_soldiers = int(helpers.getNumSoldiers())
    absent_soldiers = len(helpers.getAbsentSoldiers())
    present_soldiers = number_soldiers - absent_soldiers


    AllVacations = helpers.getActiveVacations()
    print(AllVacations)

    IterableFieldsDict = []
    for i, tup in enumerate(AllVacations):
        sampleDict = {}
        sampleDict['Soldier_ID'] = tup[0]
        sampleDict['Name'] = tup[1]
        sampleDict['From_Date'] = tup[2]
        sampleDict['To_Date'] = tup[3]
        sampleDict['State'] = tup[4]
        sampleDict['Summoned'] = tup[5]
        sampleDict['Level'] = enums.ArmyLevels[int(helpers.getLevelFromID(tup[0]))-1]
        sampleDict["Num"] = i
        IterableFieldsDict.append(sampleDict)

    fields_to_replace = {"$DEPT_NAME$": Department_Name,
                        "$DATE_AR$": Date_Arabic,
                        "$WEEKDAY$": Weekday,
                        "$NUM_OFFIC$": number_officers,
                        "$PRES_OFFIC$":present_officers,
                        "$ABS_OFFIC$":absent_officers,
                        "$NUM_CAPS$":number_caps,
                        "$PRES_CAPS$":present_caps,
                        "$ABS_CAPS$":absent_caps,
                        "$NUM_SOLD$":number_soldiers,
                        "$PRES_SOLD$":present_soldiers,
                        "$ABS_SOLD$":absent_soldiers,
                        }
    

    doccc = docx.Document('../pdf/templates/tamam.docx')
    Replace_Placeholders_Inside_Document(doccc, fields_to_replace=fields_to_replace, Iterable_Fields = IterableFieldsDict)
    ConvertAndSave(document=doccc, name="Tamam")

def ConvertAndSave(document, name):
    document.save(f'{name}.docx')
    docx2pdf.convert(f'{name}.docx', f"{name}.pdf")
    doc.save(f"{name}.pdf")