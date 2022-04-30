import calendar

calendar_example =  calendar.HTMLCalendar()
calendar_file = open('templates/calendar.html', 'w')
html_code = calendar_example.formatmonth(2021, 4)
calendar_file.write(html_code)
calendar_file.close()