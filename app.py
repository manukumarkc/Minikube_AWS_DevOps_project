from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello World</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background-color: #f8f8f8;
                color: #333;
            }
            header, footer {
                background-color: #004080;
                color: white;
                text-align: center;
                padding: 20px;
            }
            main {
                padding: 40px;
                text-align: center;
            }
            h1 {
                font-weight: bold;
                color: #004080;
            }
        </style>
    </head>
    <body>
        <header>
            <h2> My Static Web Page using Falsk and Kubernetes Minikube</h2>
        </header>
        <main>
            <h1>Hello, World from <strong>Kubernetes</strong>!</h1>
            <p>This is a static-style page served by Flask in a container.</p>
        </main>
        <footer>
            <p>App Created by Manu Kumar</p>
        </footer>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
