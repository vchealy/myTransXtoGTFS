import csv
import os
import sys
import xml.etree.ElementTree as et

from models.CalendarModel import Calendar

class CalendarExtraction:
  PRINT_PROGRESS_INTERVAL = 0.1
  TXC_NAMESPACES = {'txc': 'http://www.transxchange.org.uk/'}

  inputfiles = os.listdir('input')
  totalfiles = len(inputfiles)          # This states how many input files there \are in the input folder
  progress = 0.0
  calendars = set()

  def extract(self):
    print("Extracting calendars from input folder")
    self.__extractcalendars()
    self.__writegtfscalendars()
    print(".")

  def __extractcalendars(self):
    sys.stdout.write('- Reading TXC Information to GTFS calendars in memory')
    sys.stdout.flush()
    for index, file in enumerate(self.inputfiles):            # Iter the input files
      self.__printprogress(index)
      if file.endswith('.xml'):
        self.__process(file)
    print (".")

  def __printprogress(self, currentindex):
    if(currentindex / float(self.totalfiles) > self.progress + self.PRINT_PROGRESS_INTERVAL):
      sys.stdout.write('.')
      sys.stdout.flush()
      self.progress += 0.1

  def __process(self, file):
    for calendar in self.__getdaysofweek(file):
      self.calendars.add(self.__convertcalendars(calendar))

  def __getdaysofweek(self, file):
    root = et.parse('input/' + file).getroot()
    return root.findall('txc:Service/txc:OperatigProfile/txc:RegularDayType/txc:DaysofWeek/txc:MondaytoSunday', self.TXC_NAMESPACES)

  def __convertcalendars(self, calendars):
    service_id = calendars.attrib['id']
    start_date = calendars.find('txc:StartDate', self.TXC_NAMESPACES).text
    end_date = calendars.find('txc:EndDate', self.TXC_NAMESPACES).text
    return Calendar(service_id, start_date, end_date)

  def __writegtfscalendars(self):
    print ("- Writing calendars.txt")
    with open('output/calendar.txt', 'w') as csvfile:
      csvwriter = csv.writer(csvfile, delimiter= ' ')
      csvwriter.writerow(['service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date'])
      for calendar in self.calendars:
        csvwriter.writerow(calendar.getgtfsvalues())
