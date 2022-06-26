import sys
from application import create_app
from application.controllers.auth import AuthController

app = create_app()

def runserver():
    """Run in local machine."""
    app.run(host='0.0.0.0', port=app.config['PORT'], use_reloader=app.debug, threaded=True, debug=app.debug)

def init_db():
    auth_controller = AuthController()
    app.logger.info("Check account existed or not")
    result = auth_controller.find_account_by_username("administrator")
    if result:
        app.logger.info("Account administrator has been already existed!")
    else:
        app.logger.info("Init default administrator account")
        auth_controller.add_account({"username": "administrator", "password": "123456aA@"})
    app.logger.info("Done")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        runserver()
    if sys.argv[1] == "init_db":
        init_db()