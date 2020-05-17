from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='comment-cloud', debug=True)
