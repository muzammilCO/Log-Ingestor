from celery import Celery

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)

if __name__ == '__main__':
    celery.start(argv=['celery', 'worker', '-l', 'info'])
