# Using RoutesExtraction as the template  ---- Change searxh to StopPoints Elements

import os
import sys
import csv
import xml.etree.ElementTree as et  #Used to read from the xml file

from models.RouteModel import Route
from models.MappingModel import txcmodetogtfstype

class StopsExtraction:
  PRINT_PROGRESS_INTERVAL = 0.1
  TXC_NAMESPACES = {'txc': 'http://www.transxchange.org.uk/'}

  inputfiles = os.listdir('input')  # Location of the xml file to be read
  totalfiles = len(inputfiles)      # Total Number of Files in Folder
  progress = 0.0
  routes = []

  def extract(self):
    print ("Extracting stops from input directory")
    self.__extractstops()
    self.__writegtfsstops()
    print (".")

  def __extractstops(self):
    sys.stdout.write('- Reading TXC Stops to GTFS Stops in memory')
    sys.stdout.flush()
    for index, file in enumerate(self.inputfiles):
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
    for service in self.__getservices(file):
      for Stop in service.findall('txc:StopPoints/txc:AnnotatedStopPointRef/txc:StopPointRef', self.TXC_NAMESPACES):   #Routes were named Lines
        self.stops.append(self.__convertserviceandRoutetoroute(service, Stop))

  def __convertserviceandRoutetoroute(self, service, Stop):
    stopid = Stop.attrib['id']
    agencyid = service.find('txc:RegisteredOperatorRef', self.TXC_NAMESPACES).text
    commonname = Stop.find('txc:Description', self.TXC_NAMESPACES).text  #Original RouteName
    txcmode = service.find('txc:Location', self.TXC_NAMESPACES)           # Original Mode
    txcmode = str(txcmode)
    routetype = txcmodetogtfstype(txcmode)
    return Stop(stopid, agencyid, commonname, routetype)

  def __getservices(self, file):
    root = et.parse('input/' + file).getroot()
    return root.findall('txc:Services/txc:Service', self.TXC_NAMESPACES)

  def __writegtfsstops(self):
    print ("- Writing routes.txt")
    with open(bytes('output/routes.txt', 'utf-8'), 'w') as csvfile:
      csvwriter = csv.writer(csvfile, delimiter= '\t')
      csvwriter.writerow(['StopID', 'AgencyID', 'CommonName'])
      for stop in self.stops:
        csvwriter.writerow(stop.getgtfsvalues())
