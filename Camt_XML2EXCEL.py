import os
import xlwt
import xml.etree.ElementTree as ET

wb = xlwt.Workbook()
ws = wb.add_sheet('sto_py_camt')

ws.write(0, 0, 'acc')
ws.write(0, 1, 'org')
ws.write(0, 2, 'value')
ws.write(0, 3, 'summa')

pars_file = 'rest_Y5500071511M_20241230110209623'
xml = pars_file + '.xml'

tree = ET.parse(xml)
root = tree.getroot()

rownum=0

for camt in root.iter('{http://alfacapital.ru/statements}Stmt'):
    rownum = rownum+1
    try:
        acc = camt.find('{http://alfacapital.ru/statements}Acct')
        acc2 = acc.find('{http://alfacapital.ru/statements}Id')
        acc3 = acc2.find('{http://alfacapital.ru/statements}Othr')
        acc4 = acc3.find('{http://alfacapital.ru/statements}Id').text
    except:
        acc4 = 'Нет счета в XML'
    try:
        orgz = acc.find('{http://alfacapital.ru/statements}Ownr')
        orgz1 = orgz.find('{http://alfacapital.ru/statements}Nm').text
    except:
        orgz1 = 'Нет организации в XML'

    for bal in camt.findall('{http://alfacapital.ru/statements}Bal'):
        try:
            bal1 = bal.find('{http://alfacapital.ru/statements}Tp')
            bal2 = bal1.find('{http://alfacapital.ru/statements}CdOrPrtry')
            bal3 = bal2.find('{http://alfacapital.ru/statements}Cd').text
        except:
            bal3 = 'Нет валюты в XML'
        try:
            val = bal.find('{http://alfacapital.ru/statements}Amt').attrib
            val2 = bal.find('{http://alfacapital.ru/statements}Amt').text
            val3= val.get('Ccy')
        except:
            val3 = 'Нет валюты в XML'
            val2 = 'Нет суммы в XML'


        if bal3 == 'CLBD' or bal3 == 'Нет валюты в XML':
            print(rownum,'    ', acc4, '    ', orgz1, '    ', val3, '    ', val2)
            ws.write(rownum, 0, acc4)
            ws.write(rownum, 1, orgz1)
            ws.write(rownum, 2, val3)
            ws.write(rownum, 3, val2)


wb.save(os.path.join(os.getcwd(), pars_file + '.xls'))










