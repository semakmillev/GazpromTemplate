from app import app
import admin_app
from server import template
from server import brand
from server import company


if __name__ == '__main__':
    ## host='0.0.0.0'
    import admin_app
    app.run(host='0.0.0.0', port=5005)