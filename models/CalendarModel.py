class Calendar:
  def __init__(self, id, start_date, end_date, timezone):
    self.id = id
    self.start_date = start_date
    self.end_date = end_date
    self.timezone = timezone

  def __eq__(self, other):
    return self.id == other.getid()

  def __hash__(self):
    return hash(self.id)

  def getid(self):
    return self.id

  def getstart_date(self):
    return self.start_date

  def getend_date(self):
    return self.end_date

  def gettimezone(self):
    return self.timezone

  def getgtfsvalues(self):
    return [self.id, self.start_date, self.end_date, self.timezone]
