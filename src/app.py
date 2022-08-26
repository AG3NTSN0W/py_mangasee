from flask import Flask
from repository.setup import setupDataBase
from resource.manga import bp as mangas_bp
from resource.chapter import bp as chapters_bp
from service.app_scheduler import AppScheduler



if __name__ == "__main__":

    setupDataBase().setup()

    AppScheduler.start_scheduler()

    app = Flask(__name__)
    app.register_blueprint(mangas_bp)
    app.register_blueprint(chapters_bp)
    app.run(host='0.0.0.0', port=80)

    pass
