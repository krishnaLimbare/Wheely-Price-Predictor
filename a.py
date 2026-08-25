from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Pass the image filename to the template
    image_filename = '1.jpg'
    return render_template('index.html', image_filename=image_filename)

if __name__ == '__main__':
    app.run(debug=True)
