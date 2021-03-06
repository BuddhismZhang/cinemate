# coding=utf-8
"""
    Модуль реализует класс персоны Person,
    а также класс фотографии персоны Photo
"""
from six import iteritems
from .utils import require, BaseCinemate


class Photo(BaseCinemate):
    """ Фотография персоны. Включает в себя 3 тега со ссылками на фотографии
    разных размеров.

    :param small: фотография в маленьком разрешении
    :type small: :py:class:`str`
    :param medium: фотография в среднем разрешении
    :type medium: :py:class:`str`
    :param big: фотография в большом разрешении
    :type: big: :py:class:`str`
    """
    fields = ('small', 'medium', 'big')

    def __init__(self, small, medium, big):
        self.small = small
        self.medium = medium
        self.big = big

    @classmethod
    def from_dict(cls, dct):
        """ Фотография персоны из словаря, возвращаемого API.

        :param dct: словарь, возвращаемый API
        :type dct: :py:class:`dict`
        :return: фотография
        :rtype: :class:`.Photo`
        """
        if dct is None:
            return
        fields = {k: dct.get(k).get('url') for k in cls.fields if k in dct}
        return cls(**fields)

    def __unicode__(self):
        sizes = '/'.join(k for k, v in sorted(iteritems(self.__dict__)) if k)
        return '<Photo {sizes}>'.format(sizes=sizes)


class Person(BaseCinemate):
    """ Класс персоны.

    :param person_id: идентификатор персоны на cinemate.cc
    :type person_id: :py:class:`int`
    :param name: русскоязычное имя персоны
    :type name: :py:class:`str`
    :param name_original: имя персоны в оригинале
    :type name_original: :py:class:`str`
    :param photo: фотграфия персоны
    :type photo: :class:`.Photo`
    :param url: ссылка на страницу персоны
    :type url: :py:class:`str`
    """
    def __init__(self, person_id, **kwargs):
        self.id = int(person_id)
        self.name = kwargs.get('name')
        self.name_original = kwargs.get('name_original')
        self.photo = kwargs.get('photo')
        self.url = kwargs.get('url')

    @classmethod
    def from_dict(cls, dct):
        """ Информация о персоне из словаря, возвращаемого API.

        :param dct: словарь, возвращаемый API
        :type dct: :py:class:`dict`
        :return: персона
        :rtype: :class:`.Person`
        """
        return cls(
            person_id=dct.get('id') or dct.get('attrib').get('id'),
            name=dct.get('name') or dct.get('value'),
            name_original=dct.get('name_original'),
            photo=Photo.from_dict(dct.get('photo')),
            url=dct.get('url')
        )

    @require('apikey')
    def fetch(self):
        """ Метод API `person <http://cinemate.cc/help/api/person/>`_
        получает полную информацию о персоне

        :return: персона
        :rtype: :class:`.Person`
        """
        url = 'person'
        cinemate = getattr(self, 'cinemate')
        params = {'id': self.id}
        req = cinemate.api_get(url, apikey=True, params=params)
        person = req.json().get('person', {})
        return cinemate.person.from_dict(person)

    @classmethod
    @require('apikey')
    def get(cls, person_id):
        """ Короткий аналог person(123).fetch()

        :param person_id: идентификатор персоны
        :type person_id: :py:class:`int`
        :return: персона
        :rtype: :class:`.Person`
        """
        return cls(person_id).fetch()

    @require('apikey')
    def movies(self):
        """ Метод API
        `person.movies <http://cinemate.cc/help/api/person.movies/>`_
        возвращает фильмы, в съемке которых персона принимала участие
        в качестве актера или режиссера.

        :return: словарь с ключами actor, director
        :rtype: :py:class:`dict`
        """
        url = 'person.movies'
        cinemate = getattr(self, 'cinemate')
        params = {'id': self.id}
        req = cinemate.api_get(url, apikey=True, params=params)
        movies = req.json().get('person').get('movies', {})
        actor = movies.get('actor', {}).get('movie', [])
        director = movies.get('director', {}).get('movie', [])
        return {
            'actor': list(map(cinemate.movie.from_dict, actor)),
            'director': list(map(cinemate.movie.from_dict, director)),
        }

    @classmethod
    @require('apikey')
    def search(cls, term):
        """ Метод API
        `movie.search <http://cinemate.cc/help/api/movie.search/>`_ возвращает
        первые 10 результатов поиска по базе персон.

        :param term: искомая строка; поддерживает коррекцию ошибок при печати
        :type term: :py:class:`str`
        :return: список персон
        :rtype: :py:class:`list`
        """
        url = 'person.search'
        cinemate = getattr(cls, 'cinemate')
        params = {'term': term}
        req = cinemate.api_get(url, apikey=True, params=params)
        persons = req.json().get('person', [])
        return list(map(cls.from_dict, persons))

    def __unicode__(self):
        fields = str(self.id), self.name_original or self.name
        fields = ' '.join(fields)
        return '<Person {fields}>'.format(fields=fields)
