from extractor.AgencyExtraction import AgencyExtraction
from extractor.RouteExtraction import RoutesExtraction
from extractor.StopsDownload import StopsDownload
from extractor.StopTimesExtraction import StopTimesExtraction
from extractor.TripExtraction import TripsExtraction


# StopsDownload().download()
# AgencyExtraction().extract()
RoutesExtraction().extract()
# TripsExtraction().extract()
# StopTimesExtraction().extract()
