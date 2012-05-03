from elixir import *

metadata.bind = 'sqlite:///:memory:'
metadata.bind.echo = True

class Movie(Entity):
    title = Field(Unicode(30))
    year = Field(Integer)
    description = Field(UnicodeText)
    director = ManyToOne('Director')

    def __repr__(self):
        return '<Movie "%s" (%d)>' % (self.title, self.year)

class Director(Entity):
	name = Field(Unicode(6))
	movies = OneToMany('Movie')

	def __repr__(self):
		return '<Director "%s">' % self.name