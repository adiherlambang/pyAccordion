from time import sleep
from threading import Thread
from app.mailService import gmailServices
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

class schedulerService:

    def __init__(self,parentApp):
      self.app = parentApp
      self.scheduler = BackgroundScheduler()
      self.counter = 0

    def background_task(self):
        # Schedule the task to run every day at 08:00 AM
        trigger = CronTrigger(hour=8, minute=0)
        self.scheduler.add_job(
            self.send_email_task,
            trigger=trigger,
            id='daily_email_task'
        )
        self.scheduler.start()

    # task that runs at a fixed interval
    def send_email_task(self):
        # run forever
        while True:
            self.counter += 1
            # perform the task
            if self.counter <= 2:
                self.app.logger.info(f"Task execution email services counter: #{self.counter}")
                gmailServices.main(self.app,to="septian.adi@mastersystem.co.id",cc="kadek.sena@mastersystem.co.id",subject="testing email background service",message_text="testing email background service from python every day at 08.00")
            else:
                self.counter = 0

    def main(self):
        # create and start the daemon thread
        try:
            self.app.logger.info('Starting background task email services...')          
            daemon = Thread(target=self.background_task, daemon=True, name='Background')
            daemon.start()
        except Exception as error:
            self.app.logger.info(error)