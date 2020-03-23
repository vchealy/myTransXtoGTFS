import csv
import os
import sys
import xml.etree.ElementTree as et

from models.AgencyModel import Agency

class AgencyExtraction:
  PRINT_PROGRESS_INTERVAL = 0.1
  TXC_NAMESPACES = {'txc': 'http://www.transxchange.org.uk/'}

  inputfiles = os.listdir('input')
  totalfiles = len(inputfiles)          # This states how many input files there \are in the input folder
  progress = 0.0
  agencies = set()

  def extract(self):
    print("Extracting agencies from input folder")
    self.__extractagencies()
    self.__writegtfsagencies()
    print(".")

  def __extractagencies(self):
    sys.stdout.write('- Reading TXC Operators to GTFS Agencies in memory')
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
    for operator in self.__getoperators(file):
      self.agencies.add(self.__convertoperatortoagency(operator))

  def __getoperators(self, file):
    root = et.parse('input/' + file).getroot()
    return root.findall('txc:Operators/txc:LicensedOperator', self.TXC_NAMESPACES)

  def __convertoperatortoagency(self, operator):
    agencyid = operator.attrib['id']
    agencyname = operator.find('txc:OperatorNameOnLicence', self.TXC_NAMESPACES).text
    agencyurl = 'https://www.google.com/#q=' + agencyname
    agencytimezone = 'Europe/London'
    return Agency(agencyid, agencyname, agencyurl, agencytimezone)

  def __writegtfsagencies(self):
    print ("- Writing agencies.txt")
    with open('output/agency.txt', 'w') as csvfile:
      csvwriter = csv.writer(csvfile, delimiter= ' ')
      csvwriter.writerow(['agency_id', 'agency_name', 'agency_url', 'agency_timezone'])
      for agency in self.agencies:
        csvwriter.writerow(agency.getgtfsvalues())
