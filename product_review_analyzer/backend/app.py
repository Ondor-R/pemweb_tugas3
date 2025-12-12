from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from database import Base, engine, get_db_session
from wsgicors import CORS

from models import Review

def main():
    Base.metadata.create_all(engine)

    with Configurator() as config:
        config.add_request_method(get_db_session, 'dbsession', reify=True)
        
        config.add_route('analyze_review', '/api/analyze-review')
        config.add_route('get_reviews', '/api/reviews')
        
        config.scan('views')
        
    app = config.make_wsgi_app()
    
    # Bungkus app dengan CORS agar Frontend React bisa akses
    app = CORS(app, headers="*", methods="*", origin="*")

    print("Server running on http://localhost:6543")
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

if __name__ == '__main__':
    main()