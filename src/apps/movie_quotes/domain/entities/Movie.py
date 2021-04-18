class Movie(object):
    def __init__(self, id = None, name = '', year = 0, url = ''):
        self._id = id
        self._name = name
        self._year = year
        self._url = url

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def year(self):
        return self._year

    @property
    def url(self):
        return self._url

    @id.setter
    def id(self, id):
        self._id = id

    @name.setter
    def name(self, name):
        self._name = name

    @year.setter
    def year(self, year):
        self._year = year

    @url.setter
    def url(self, url):
        self._url = url