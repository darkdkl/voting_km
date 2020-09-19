from django.core.mail import EmailMessage
import xlsxwriter



def send(user_email):
    email = EmailMessage(
            'Hello',
            'Body goes here',
            'from@example.com',
            ['to1@example.com'],
            headers={'Message-ID': 'foo'},)

def make_xls(data,name):
    workbook = xlsxwriter.Workbook(f'reports/{name}.xlsx')
    persona,votes =map(list, zip(*data))
    letter_name='Победители'
    worksheet = workbook.add_worksheet(letter_name)
    chart = workbook.add_chart({'type': 'line'})
    worksheet.write_column('A1', persona)
    worksheet.write_column('B1', votes)
    chart.add_series({
                    'categories': f'={letter_name}!A1:A{len(persona)}',
                    'values': f'={letter_name}!B1:B{len(votes)}'
                    })
    worksheet.insert_chart('D5', chart)
    workbook.close()