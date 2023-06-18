from app import app
from app.controllers import users_controller, sightings_controller

if __name__=="__main__":
    app.run(debug=True)