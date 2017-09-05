# -*-coding:utf-8 -*-
from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

import logging
import logging.config
import spyder4ss

CONF_LOG = "logger.conf"
logging.config.fileConfig(CONF_LOG);  # 采用配置文件
logger = logging.getLogger('main')


def tick():
    logger.info('Tick! The time is: %s' % datetime.now())


def hello():
    logger.info('hello time is: %s' % datetime.now())


jobstores = {
    # 'mongo': MongoDBJobStore(),
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

# scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
# scheduler.add_job(tick, trigger='cron', second='*/30', id='cron_id')
scheduler.add_job(spyder4ss.getss, trigger='interval', seconds=3360, id='interval_id')

try:
    scheduler.start()  # 采用的是阻塞的方式，只有一个线程专职做调度的任务
except (KeyboardInterrupt, SystemExit):
    logger.info("clear jobs")
    scheduler.remove_all_jobs()
    logger.info('Exit The Job!')
