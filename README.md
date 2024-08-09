### ProspectX Deployment


```
ssh -i "prospectx.pem" ubuntu@18.223.227.40
```

```
sudo su
cd /home/prospectx/prospectx_new
```

```
source venv/bin/activate
```

```
git pull
```

```
pip install -r requirements.txt
```

```
python manage.py makemigrations
python manage.py migrate
```

```
chown prospectx:prospectx -R media/
```

#### Restart Services
```
sudo supervisorctl restart prospectx
sudo supervisorctl restart daphne_django_event
sudo supervisorctl restart celerybeat
sudo supervisorctl restart celeryworker
```


#### Check Status
```
sudo supervisorctl status prospectx
sudo supervisorctl status daphne_django_event

sudo supervisorctl status celerybeat
sudo supervisorctl status celeryworker
```

#### Check Celery Log
```
celery -A prospectx_new beat -l info
celery -A prospectx_new worker -l info

tail -f /var/log/celery/celery_worker.log
```

#### Redis
```
redis-cli ping

redis-cli flushall
sudo systemctl status redis
sudo systemctl restart redis
```

#### Elastic Search
```
sudo systemctl stop elasticsearch
sudo systemctl start elasticsearch
```

#### Test Server
```
python ./manage.py runserver 0.0.0.0:8092
http://13.59.65.15:8092/
```

#### Resize EBS volume
```
sudo resize2fs /dev/nvme0n1p1
df -h
```