from django.core.mail import EmailMessage
from votings_km.settings import EMAIL_HOST_USER as sender
import xlsxwriter


def send(user_email,filename,voting_name):
    message = EmailMessage(
            f'Отчет голосования "{voting_name}"',
            'Приветствуем.Отчет прикреплен к сообщению',
            sender,
            [user_email],
            headers={'Message-ID': 'foo'},)
    message.attach_file("./"+filename)
    message.send(fail_silently=False)


def make_xls(data,name):
    filename=f'reports/{name}.xlsx'
    workbook = xlsxwriter.Workbook(filename)
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
    return filename