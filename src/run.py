# from app import create_app
# app = create_app()

from app import app


if __name__ == '__main__':
    app.run(host='comment-cloud', debug=True)
