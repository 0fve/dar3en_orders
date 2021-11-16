from Website import create_app
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect



app = create_app()


if __name__ == '__main__':
    # deepcode ignore RunWithDebugTrue: we need debug to be true for the moment
    app.run(debug=True, host='0.0.0.0',port=8000)
