from repository.setup import setupDataBase
from service.app_scheduler import AppScheduler


if __name__ == "__main__":
    setupDataBase()

    AppScheduler.start_scheduler()

    pass
