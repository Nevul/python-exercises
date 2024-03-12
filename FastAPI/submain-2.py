from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional     #Podemos usar Optional o Union, para definir que puede ser de un tipo u otro

app = FastAPI()
app.title = 'Project LxNevul'
app.version = '0.0.1'
app.description = 'Este proyecto consiste en dar los primeros pasos en FastAPI para posteriormente dar paso a una App de Películas'
app.contact = {
    'name': 'API Support',
    'email': 'alexivan.code@gmail.com',
    'url': 'https://github.com/Nevul' 
}

class Movie(BaseModel):
    id: Optional[int] = None    #También puede ser Union[int, None], esto sería lo mismo que Optional[int]
    title: str = Field(min_length=5, max_length=25)
    overview: str = Field(min_length=30, max_length=60)
    year: int = Field(le = 2024)
    rating: float = Field(ge = 0, le = 10)
    category: str

    model_config = ConfigDict(
        json_schema_extra = {
            'examples': [
                {
                    'id': 1,
                    'title': 'Nombre de la película',
                    'overview': 'Descripción breve acerca de la película, en sí un resumen.',
                    'year': 1995,
                    'rating': 5.5,
                    'category': 'Clasificación'
                }
            ]
        }
    )
'''
    class Config:
        json_schema_extra = {
            'examples': [
                {
                    'id': 1,
                    'title': 'Nombre de la película',
                    'overview': 'Descripción breve acerca de la película, en sí un resumen.',
                    'year': 1995,
                    'rating': 5.5,
                    'category': 'Clasificación'
                }
            ]
        }
'''

movies = [
    {
        'id': 0,
        'title': 'Película o Serie no encontrada',
        'year': 0,
        'category': ''
    },
    {
        'id': 1,
        'title': 'La chica de al lado',
        'overview': 'Matt es un estudiante que está por graduarse de la preparatoria, mientras tiene como proyecto traer un potencial estudiante de otro país por medio de una beca escolar, pero pronto conocería a Danielle quien alteraría el curso normal de su vida.',
        'year': 2004,
        'rating': 6.7,
        'category': 'Comedy/Romance'
    },
    {
        'id': 2,
        'title': 'Smallville',
        'overview': 'Trata sobre la vida adolescente de superman, quien poco a poco va desarrollando sus habilidades y su mente para llegar a portar el traje del superhéroe que todos conocemos.',
        'year': 2001,
        'rating': 7.5,
        'category': 'Drama'
    }
]

@app.get('/', tags = ['Inicio'])
def message():
    return HTMLResponse('<h2>Bienvenidos, soy LxNevul</h2>')

@app.get('/movies', tags = ['Movies'])
async def get_movies():
    return movies

@app.get('/movies/{id}', tags = ['Movies'])
async def get_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            return movie
    return 'No se encontró el recurso indicado'

@app.get('/movies/', tags = ['Movies'])
async def get_movie_by_category(category: str, year: int):
    for movie in movies:
        if movie['category'] == category and movie['year'] == str(year):
            return movie  
    return 'No se encontró el recurso indicado'

@app.post('/movies', tags = ['Movies'])
async def create_movie(film: Movie):
    movies.append(film)
    return movies

@app.put('/movies/{id}', tags = ['Movies'])
async def modify_movie(id: Optional[int], film: Movie):
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = film.title
            movie['overview'] = film.overview
            movie['year'] = film.year
            movie['rating'] = film.rating
            movie['category'] = film.category
            return movies
    return 'No se encontró el recurso indicado'

@app.delete('/movies/{id}', tags = ['Movies'])
async def delete_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return movies
    return 'No se encontró el recurso indicado'