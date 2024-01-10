from flask import Flask, request
from flask_restx import Api, Resource, fields, reqparse, marshal
from flask_sqlalchemy import SQLAlchemy
from models import db, Movie

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:11112222@localhost:3306/db_movie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api = Api(app, version='1.0', title='Movie Database System', description='API for managing movies')
movies_ns = api.namespace("movies", path='/movies', description="Operations related to movies")

# search_ns = api.namespace("movies", path='/movies', description="Operations related to movies")

movie_model = api.model('Movie', {
    'title': fields.String(required=True, description='The movie title'),
    'running_time': fields.String(required=True, description='The movie running time'),
    'language': fields.String(required=True, description='The movie language'),
    'genre': fields.String(required=True, description='The movie genre'),
    'release_date': fields.String(required=True, description='The movie release_date'),
    'cast_detail': fields.String(required=True, description='The movie cast')
})


put_movie_parser = reqparse.RequestParser()
put_movie_parser.add_argument('title', type=str, required=True, help='Title is required')
put_movie_parser.add_argument('running_time', type=int, required=True, help='Running time is required')
put_movie_parser.add_argument('language', type=str, required=True, help='Language is required')
put_movie_parser.add_argument('genre', type=str, required=True, help='Genre is required')
put_movie_parser.add_argument('release_date', type=str, required=True, help='Release_date is required')
put_movie_parser.add_argument('cast_detail', type=str, required=True, help='Cast detail is required')


# create and get all
@movies_ns.route('/')
class MoviesResource(Resource):  
    def get(self):
        try:
            movies = db.session.query(Movie).all()
            return [{   
                       'id': movie.show_id,
                        'title':movie.title,
                        'running_time':movie.running_time,
                        'language': movie.language,
                        'genre':movie.genre,
                        'release_date': movie.release_date,
                        'cast_detail': movie.cast_detail}
                        for movie in movies]
        except Exception as e:
            return {'error': f'Error fetching movies: {str(e)}'}, 500

    @movies_ns.expect(put_movie_parser)
    def post(self):
        try:
            data = put_movie_parser.parse_args()
            for field in ['title', 'running_time', 'language', 'genre','release_date' ,'cast_detail']:
                if not data[field]:
                    return {'error': f'{field} is required'}, 400
                
            new_movie = Movie(
                title=data['title'],
                running_time=data['running_time'],
                language=data['language'],
                genre=data['genre'],
                release_date= data['release_date'],
                cast_detail=data['cast_detail']
            )
            db.session.add(new_movie)
            db.session.commit()
            return {'message': 'successfully',   
                        'id': new_movie.show_id,
                        'title':new_movie.title,
                        'running_time':new_movie.running_time,
                        'language': new_movie.language,
                        'genre':new_movie.genre,
                        'release_date':new_movie.release_date,
                        'cast_detail': new_movie.cast_detail}, 201
            
        except Exception as e:
            db.session.rollback()  
            return {'error': f'Error adding movie: {str(e)}'}, 500

# update, delete and get user by id   
@movies_ns.route('/<int:movie_id>')
class MovieResource(Resource):
    def get(self, movie_id):
        try:
            movie = Movie.query.get_or_404(movie_id)
            return marshal(movie, movie_model)
        except Exception as e:
            return {'error': f'Error fetching movie: {str(e)}'}

    @movies_ns.expect(put_movie_parser)
    def put(self, movie_id):
        try:
            movie = Movie.query.get_or_404(movie_id)
            data = put_movie_parser.parse_args()
            movie.title = data['title']
            movie.running_time = data['running_time']
            movie.language = data['language']
            movie.genre = data['genre']
            movie.release_date = data['release_date']
            movie.cast_detail = data['cast_detail']
            db.session.commit()
            return marshal(movie, movie_model)
        except Exception as e:
            return {'error': f'Error updating movie: {str(e)}'}

    def delete(self, movie_id):
        try:
            movie = Movie.query.get_or_404(movie_id)
            db.session.delete(movie)
            db.session.commit()
            return {'message': 'Movie deleted successfully'}
        except Exception as e:
            return {'error': f'Error deleting movie: {str(e)}'}



# search 
@movies_ns.route('/filter/<string:movie_title>')
class Search(Resource):
     def get(self, movie_title):
        try:
            movie = Movie.query.filter(Movie.title.ilike(f'%{movie_title}%')).all()
            if movie:
                return [{   
                       'id': movies.show_id,
                        'title':movies.title,
                        'running_time':movies.running_time,
                        'language': movies.language,
                        'genre':movies.genre,
                        'release_date': movies.release_date,
                        'cast_detail': movies.cast_detail}
                        for movies in movie]
            else:
                return {'message': f'Movie with title "{movie_title}" not found'}
        except Exception as e:
            return {'error': f'Error fetching movie: {str(e)}'}

if __name__ == '__main__':
    with app.app_context():
        try:
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            db.create_all()
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {str(e)}")

    app.run(host='127.0.0.1', port=5500)


    