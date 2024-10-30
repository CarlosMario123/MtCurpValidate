from flask import Flask,render_template
from routes.curpRoute import curp_bp
app = Flask(__name__)
app.secret_key = "key123"
app.register_blueprint(curp_bp, url_prefix='/curp')
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)