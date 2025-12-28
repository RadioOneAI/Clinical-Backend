from app import create_app

app = create_app()
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

if __name__ == "__main__":
    app.run(debug=True)
