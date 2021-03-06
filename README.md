[![PyPI version](http://badge.fury.io/py/cinemate.png)](http://badge.fury.io/py/cinemate)
[![Build status](http://secure.travis-ci.org/Pentusha/cinemate.png?branch=master)](https://travis-ci.org/Pentusha/cinemate)
[![Tests Coverage](http://coveralls.io/repos/Pentusha/cinemate/badge.png?branch=master)](https://coveralls.io/r/Pentusha/cinemate)
[![Wheel Status](http://pypip.in/wheel/cinemate/badge.png)](https://pypi.python.org/pypi/cinemate/)

Cinemate - реализация API сайта [сinemate.cc][cinemate] на языке python.
Реализация использует методы [api v2][api].


Установка
=========
Используйте слудуюую команду для получения последней версии:

    pip install cinemate

Страница на [PyPI][pypi].

Документация на [Read the Docs][readthedocs].

Использование
=============
Ниже приведены простые примеры, подробные примеры находятся в каталоге `examples`.

Инициализация:

```python
>>> from cinemate import Cinemate
>>> cin = Cinemate('username', 'password', 'passkey', 'apikey')
```

Получить подробную информацию о персоне:

```python
>>> person = cin.person.get(57658)
>>> print(person)
<Person 57658 Noel Fielding>
>>> print(person.photo.big)
http://c.cinemate.cc/media/p/8/5/57658/0.big.jpg
```

Получить подробную информацию о фильме:

```python
>>> print(movie)
<Movie 114458 Africa>
>>> print(movie.title.original)
Africa
>>> movie.runtime is None
True
>>> print(movie.imdb)
<Rating rating=8.9 votes=1984>
>>> print(movie.imdb.rating)
8.9
```

Получить список слежения пользователя:

```python
>>> watchlist = cin.account.watchlist()
>>> for person in watchlist['person']:
...     print(person.name_original)
...
Kar Wai Wong
Gregg Araki
Jan Svankmajer
Gaspar Noe
```

Участие в разработке
====================
Проверяйте внесенные изменения на соответсвие [pep-20][pep20], [pep-8][pep8], [pep-287][pep287].
Пожалуйста, документируйте код на русском языке, т.к. проект cinemate.cc рассчитан на росскоговорящую аудиторию.
Тесты должны выполняться в версиях py27, py32, py33, py34.
В остальном никаких особенностей нет, форкаете, меняете, pull-request.

[cinemate]: http://cinemate.cc/
[pep8]: http://www.python.org/dev/peps/pep-0008/
[pep20]: http://www.python.org/dev/peps/pep-0020/
[pep287]: http://www.python.org/dev/peps/pep-0287/
[pypi]: https://pypi.python.org/pypi/cinemate
[readthedocs]: http://cinemate.rtfd.org/
[api]: http://cinemate.cc/help/api/
