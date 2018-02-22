import multiprocessing

user      = 'www-data'
group     = 'www-data'
bind      = '0.0.0.0:80'
workers   = multiprocessing.cpu_count()
threads   = 1
accesslog = '-'
errorlog = '-'
