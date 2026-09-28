[简体中文](README.md) | [English](README.en.md)

# AutoOps

> A Linux asset management (CMDB) and ops platform built on Django 2.2, integrating WebSSH, batch command execution, monitoring charts, Docker/K8s management, online MySQL SQL auditing, and code release.

![Python](https://img.shields.io/badge/Python-3.6.x-blue)
![Django](https://img.shields.io/badge/Django-2.2.x-green)
![License](https://img.shields.io/badge/License-Apache%202.0-red)
![Status](https://img.shields.io/badge/Status-Unmaintained-lightgrey)

> **⚠️ This project is no longer under development!** The code has not been maintained for a long time, so it may fail to deploy or contain bugs on different environments — please be aware. The code is provided for learning purposes only; the author no longer provides updates or maintenance.

## Introduction

AutoOps is an all-in-one ops platform for Linux administrators that brings the most common day-to-day tasks into a single web interface: asset management (CMDB), batch command execution, server CPU/memory/network monitoring, WebSSH login without a jump host, an ops knowledge base, online MySQL SQL auditing, plus basic Docker and Kubernetes management.

The permission system is built on django-guardian and provides object-level authorization: once resources are divided by user group in the admin backend (e.g. an ops group and a dev group), accounts in a group can only see the servers and databases of that group, and can only select assets from their own group when running tasks — they cannot add or view resources of other groups.

The platform ships with Celery scheduled jobs (periodically collecting host performance data and cleaning up old monitoring records) and Supervisor process management (uniformly starting uwsgi, webssh, celery, Inception, etc.). It suits small and medium teams that want a self-hosted ops platform on CentOS, and also works well as a comprehensive learning project for Django + Ansible + Celery.

## ✨ Features

- **Asset Management (CMDB)**
  - CRUD for assets with detail pages and batch deletion
  - Automatic server info collection via Ansible (hostname, OS, IP, CPU, memory, disks, SN, etc.)
  - CPU / memory / network traffic charts rendered with pyecharts, including a 7-day history
  - Export all assets to Excel; REST API for asset list/detail (built with DRF)
  - System user management (passwords encrypted with Fernet, `names/password_crypt.py`)
- **Task Center**
  - Command line: pick hosts in the web UI and run commands in batch (Ansible API)
  - Tools: store Shell / Python script snippets and dispatch them to hosts at any time
- **WebSSH**: SSH to servers directly from the browser (Tornado + Paramiko, based on [huashengdun/webssh](https://github.com/huashengdun/webssh)); one click from the asset list
- **Database Management**: manage MySQL instances and database accounts, bound to product lines / data centers
- **Database Operations Platform (Inception)**
  - Online SQL review (based on Inception, MySQL only)
  - One-click execution after a review passes, with rollback statement lookup
- **Code Release**
  - Code repository management; upload a package and distribute it to target hosts via the Ansible `copy` module
- **Docker Management**: container list (image, status, port mappings, command) with start/stop/restart actions (Docker SDK)
- **K8s Management**: cluster resource overview covering Namespace / Node / Pod / Service / ConfigMap / Secret / Deployment / DaemonSet / StatefulSet / Job / CronJob
- **GPU Resources**: browse GPU compute offers, place orders, activate orders, and track usage records
- **Documentation**: an ops knowledge base with the DjangoUeditor rich text editor — no need to search elsewhere for solutions
- **Users & Auditing**: platform login history, web operation history, command execution history, and password change
- **Admin Backend**: xadmin (`/admin/`) + the built-in Django admin (`/dadmin/`), with user-group based resource isolation; admin has the highest privileges
- **Scheduled Jobs**: Celery jobs periodically collect host CPU/memory/traffic and automatically clean up monitoring history older than one week

## 🛠 Tech Stack

| Category | Components |
| --- | --- |
| Backend | Python 3.6, Django 2.2.28, djangorestframework, django-guardian, xadmin (django2 branch) |
| Task Queue | Celery 3.1.25 + django-celery + Redis (broker) |
| Automation | Ansible (>= 2.4.5, bundled `tasks/ansible_2420` API wrapper), Paramiko |
| Frontend | Bootstrap (django-bootstrap3), pyecharts charts, DjangoUeditor rich text |
| WebSSH | Tornado 6.3.3 + Paramiko + cryptography |
| Containers/Cluster | docker (>= 6.1.3) and kubernetes (>= 29.0.0) Python clients |
| SQL Auditing | Inception (bundled binary in `script/inception/`) |
| Storage | SQLite (default) / MySQL (pymysql) |
| Deployment | uwsgi + Supervisor (started with Python 2.7), optional Nginx |

## 🚀 Quick Start

Requirements: CentOS 7.4, Python 3.6.4 (install script `script/install_python3.6.4.sh`), Python 2.7 (to run Supervisor), and Redis; Docker / Kubernetes are optional (for container and cluster management).

### 1. Base environment

```bash
cd /opt
yum install git sshpass redis -y
systemctl enable redis.service
systemctl start redis.service
git clone https://github.com/hequan2017/autoops.git
cd autoops/
pip3 install -r requirements.txt

# Install xadmin (django2 branch)
cd /usr/local/src
wget https://codeload.github.com/sshwsfc/xadmin/zip/django2
unzip django2
cd xadmin-django2/
python setup.py install
```

> It is recommended to run `yum install ipmitool dmidecode -y` on managed assets to collect more information.

### 2. Install Supervisor (Python 2.7)

```bash
chmod +x /opt/autoops/script/inception/bin/*
pip2 install supervisor    # If pip2 is missing, see script/install_pip2.sh
echo_supervisord_conf > /etc/supervisord.conf
mkdir /etc/supervisord.d/

# Edit /etc/supervisord.conf and append:
[inet_http_server]             # Account/password for the Supervisor HTTP UI
port=0.0.0.0:9001
username=user
password=321

[include]
files = /etc/supervisord.d/*.conf

cp /opt/autoops/script/supervisor.conf /etc/supervisord.d/
```

Processes managed by `supervisor.conf`: `uwsgi` (web service, listening on `0.0.0.0:8003` by default), `webssh` (port 9000), `celeryd` / `celerybeat` / `celerycam` (queue and scheduled jobs), and `Inception` (SQL audit).

### 3. Configure `autoops/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',   # Use SQLite if no MySQL
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# With MySQL, switch to:
# 'ENGINE': 'django.db.backends.mysql', 'NAME': 'autoops',
# 'USER': 'root', 'PASSWORD': '123456', 'HOST': '192.168.10.24', 'PORT': '3306'
# For MySQL installation, see the author's blog: http://hequan.blog.51cto.com/5701886/1982428

DEBUG = True                                   # Set to False in production

BROKER_URL = 'redis://127.0.0.1:6379/0'        # Redis address, usually unchanged

Webssh_ip = '114.115.132.147'                  # Public IP for WebSSH access
Webssh_port = '9000'                           # Port; if changed, also update webssh/main.py

Inception_ip = '127.0.0.1'                     # Inception address, local by default
Inception_port = '6669'

inception_remote_system_password = '654321'    # Rollback backup DB settings,
inception_remote_system_user = 'root'          # keep in sync with script/inc.cnf
inception_remote_backup_port = '3306'
inception_remote_backup_host = '192.168.10.100'
```

### 4. Compatibility patches

```bash
# Django + older MySQL client: comment out the following lines in
# /usr/local/lib/python3.6/site-packages/django/db/backends/mysql/base.py
# (ignore if not found):
# if version < (1, 3, 3):
#     raise ImproperlyConfigured("mysqlclient 1.3.3 or newer is required; ...")

# Inception does not support pymysql natively; replace the files with
# the patched ones shipped in the repo:
cp /opt/autoops/script/connections.py /usr/local/lib/python3.6/site-packages/pymysql/connections.py
cp /opt/autoops/script/cursors.py    /usr/local/lib/python3.6/site-packages/pymysql/cursors.py
```

### 5. Initialize and start

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser      # Create the admin account

/usr/bin/python2.7 /usr/bin/supervisord -c /etc/supervisord.conf
# Add the command above to /etc/rc.d/rc.local for boot start (chmod +x first)
```

- The platform port is on line 2 of `script/supervisor.conf`, `0.0.0.0:8003` by default
- Supervisor UI: `0.0.0.0:9001` (user `user` / password `321`) to start/stop uwsgi, webssh, celery, and Inception

![DEMO](static/demo/14.png)

- After logging in to the backend: set up the scheduled job for host performance charts (create the frequency first, then the job; watch whether the queue runs — restart the celery services if not), and configure data centers and user groups.

![DEMO](static/demo/9.png)

### Production deployment

Use Nginx for static files and uwsgi proxying (see the [author's blog post](http://hequan.blog.51cto.com/5701886/1982769)); remove the uwsgi sections from `supervisor.conf` and control uwsgi with:

```bash
uwsgi --ini    /opt/autoops/script/uwsgi.ini     # Start
uwsgi --stop   /opt/autoops/script/uwsgi.pid     # Stop
uwsgi --reload /opt/autoops/script/uwsgi.pid     # Reload
```

Reference Nginx configuration:

```nginx
root /opt/autoops;

location / {
    include uwsgi_params;
    uwsgi_connect_timeout 30;
    uwsgi_pass unix:/opt/autoops/script/uwsgi.sock;
}

location /static/ {
    alias /opt/autoops/static/;
    index index.html index.htm;
}
```

### Local debugging on Windows (PyCharm)

Install the pip dependencies first (ansible cannot be installed on Windows — ignore that), then comment out the ansible imports and calls below, and comment out xadmin:

```text
In asset/views.py, tasks/views.py, release/views.py:
from tasks.ansible_2420.runner import AdHocRunner, CommandRunner
from tasks.ansible_2420.inventory import BaseInventory
```

## 📁 Directory Structure

```text
autoops/
├── asset/        # Asset management (CMDB): models, API, perf charts, WebSSH entry
├── db/           # Database management: MySQL instances and accounts
├── names/        # Users & auditing: login/web/cmd history, password encryption
├── tasks/        # Task center: command line, tool scripts, Inception SQL audit
├── release/      # Code release: repo management and host distribution
├── library/      # Documentation: ops knowledge base
├── dockerops/    # Docker container management
├── k8sops/       # Kubernetes cluster overview
├── gpuops/       # GPU resources: offers, orders, allocations
├── webssh/       # WebSSH service (Tornado + Paramiko)
├── DjangoUeditor/ # Rich text editor
├── script/       # Deployment scripts: supervisor.conf, uwsgi.ini, Inception, pymysql patches
└── templates/    # Frontend templates
```

## 🧭 Architecture

![DEMO](static/demo/autoops.png)

## 📸 Screenshots

![DEMO](static/demo/13.png)
![DEMO](static/demo/12.png)
![DEMO](static/demo/1.png)
![DEMO](static/demo/4.png)
![DEMO](static/demo/5.png)
![DEMO](static/demo/7.png)

## 🗺️ Changelog

- **1.8** Final update: modified the ansible API to support playbooks (test on your own)
- **1.7.8** Backend switched to xadmin (xadmin does not yet support django-guardian object permissions; use the admin account in dadmin when needed)
- **1.7.7** Changed the webssh startup method
- **1.7.6** Code repository feature launched, with distribution support
- **1.7.4** Updated ansible and enhanced the command line feature
- **1.6** MySQL automatic SQL review + execution (MySQL only)
- **1.4** Upgraded to Django 2.0
- **1.3** Added the documentation module
- **1.2** Improved permission management + attachment upload/download
- **1.1.5** Permission management: user-group based resource isolation
- **1.1** Added platform login records, web login records, and password change

## 🌐 Demo & Community

- QQ group: `620176501` (discussions welcome)
- Blog: `http://hequan.blog.51cto.com/`
- GitHub: `https://github.com/hequan2017/autoops/`
- Gitee: `https://gitee.com/hequan2020/autoops`

## 📄 License

[Apache License 2.0](LICENSE)

## 👥 Contributors

#### 1.0

- He Quan (何全)
