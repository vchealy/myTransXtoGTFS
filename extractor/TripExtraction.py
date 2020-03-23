import csv
import xml.etree.ElementTree as et
import os
import sys

from models.TripsModel import Trip

class TripsExtraction:
  PRINT_PROGRESS_INTERVAL = 0.1
  TXC_NAMESPACES = {'txc': 'http://www.transxchange.org.uk/'}

  inputfiles = os.listdir('input')
  totalfiles = len(inputfiles)
  progress = 0.0
  trips = []

  def extract(self):
    print ("Extracting trips from input directory")
    self.__extracttrips()
    self.__writegtfstrips()
    print (".")

  def __extracttrips(self):
    sys.stdout.write('- Reading TXC VehicleJourneys to GTFS trips in memory')
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
    xmlroot = et.parse('input/' + file).getroot()             # This Reading from the XML file
    # for child in xmlroot:                                     # This lists the tags
      # print(child.tag)
    for VehicleJourneys in self.__getVehicleJourneys(xmlroot):
      self.trips.append(self.__convertVehicleJourneystotrip(xmlroot, VehicleJourneys))

  def __convertVehicleJourneystotrip(self, xmlroot, VehicleJourneys):
    tripid = VehicleJourneys.find('txc:VehicleJourneyCode', self.TXC_NAMESPACES).text
    serviceid = tripid
    routeid = VehicleJourneys.find('txc:LineRef', self.TXC_NAMESPACES).text
    txcserviceref = VehicleJourneys.find('txc:ServiceRef', self.TXC_NAMESPACES).text
    tripheadsign = self.__getservicedescription(xmlroot, txcserviceref)
    return Trip(tripid, serviceid, routeid, tripheadsign)

  def __getservicedescription(self, xmlroot, serviceref):
    for service in xmlroot.findall('txc:Services/txc:Service', self.TXC_NAMESPACES):
      if(service.find('txc:ServiceCode', self.TXC_NAMESPACES).text == serviceref):
        return service.find('txc:ServiceCode', self.TXC_NAMESPACES).text  #Originally Description but there was no text Value
    return null

  def __getVehicleJourneys(self, xmlroot):
    return xmlroot.findall('txc:VehicleJourneys/txc:VehicleJourney', self.TXC_NAMESPACES)  # Second txc was in plural in error txc:VehicleJourneys

  def __writegtfstrips(self):
    print ("- Writing trips.txt")
    with open(bytes('output/trips.txt', 'utf-8'), 'w') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(['trip_id', 'service_id', 'route_id', 'trip_headsign'])
      for route in self.trips:
        csvwriter.writerow(route.getgtfsvalues())
