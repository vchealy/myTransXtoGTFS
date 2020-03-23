import csv
import xml.etree.ElementTree as et  #Used to read from the xml file
import os
import sys

from models.RouteModel import Route
from models.MappingModel import txcmodetogtfstype

class RoutesExtraction:
  PRINT_PROGRESS_INTERVAL = 0.1
  TXC_NAMESPACES = {'txc': 'http://www.transxchange.org.uk/'}

  inputfiles = os.listdir('input')  # Location of the xml file to be read
  totalfiles = len(inputfiles)      # Total Number of Files in Folder
  progress = 0.0
  routes = []

  def extract(self):
    print ("Extracting routes from input directory")
    self.__extractroutes()
    self.__writegtfsroutes()
    print (".")

  def __extractroutes(self):
    sys.stdout.write('- Reading TXC Services+Routes to GTFS Routes in memory')
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
      for Route in service.findall('txc:Routes/txc:Route', self.TXC_NAMESPACES):   #Routes were named Lines
        self.routes.append(self.__convertserviceandRoutetoroute(service, Route))

  def __convertserviceandRoutetoroute(self, service, Route):
    routeid = Route.attrib['id']
    routename = Route.find('txc:Description', self.TXC_NAMESPACES).text  #Original RouteName
    txcmode = service.find('txc:Location', self.TXC_NAMESPACES)           # Original Mode
    txcmode = str(txcmode)
    routetype = txcmodetogtfstype(txcmode)
    agencyid = service.find('txc:RegisteredOperatorRef', self.TXC_NAMESPACES).text
    return Route(routeid, agencyid, routename, routetype)

  def __getservices(self, file):
    root = et.parse('input/' + file).getroot()
    return root.findall('txc:Services/txc:Service', self.TXC_NAMESPACES)

  def __writegtfsroutes(self):
    print ("- Writing routes.txt")
    with open(bytes('output/routes.txt', 'utf-8'), 'w') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(['route_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_type'])
      for route in self.routes:
        csvwriter.writerow(route.getgtfsvalues())
