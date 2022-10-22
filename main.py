from distutils.log import debug

from sqlalchemy import true
from src import createApp

app = createApp()

if __name__ == '__main__':
    app.run(debug=True)
