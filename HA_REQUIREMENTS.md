# High Availability (HA) Requirements
**Project:** GEOPRAM TECHNOLOGIES Website  
**Version:** 1.0  
**Date:** 2026-04-17

---

## 1. Overview

This document defines the High Availability requirements for the GEOPRAM TECHNOLOGIES Django-based GIS website. The system must maintain operational continuity with minimal downtime to ensure business operations and client access to the dashboard.

---

## 2. HA Objectives

| Metric | Target | Description |
|--------|--------|-------------|
| **Availability SLA** | 99.9% Uptime | Maximum 8.76 hours downtime per year |
| **Recovery Time Objective (RTO)** | < 15 minutes | Maximum time to restore service after failure |
| **Recovery Point Objective (RPO)** | < 5 minutes | Maximum data loss threshold |
| **Mean Time Between Failures (MTBF)** | > 30 days | Average time between system failures |
| **Planned Maintenance Window** | 2 hours/month | Scheduled downtime for updates |

---

## 3. System Architecture Requirements

### 3.1 Redundant Infrastructure

- **[REQ-HA-001]** Deploy at least **2 web server instances** behind a load balancer
- **[REQ-HA-002]** Configure **auto-scaling group** with minimum 2, maximum 4 instances
- **[REQ-HA-003]** Deploy across **2+ availability zones** within the same region
- **[REQ-HA-004]** Implement **health checks** on all instances with automatic failover

### 3.2 Load Balancing

- **[REQ-HA-005]** Use a managed load balancer (AWS ALB/NLB, GCP LB, Azure LB)
- **[REQ-HA-006]** Configure **sticky sessions** (session affinity) for Django dashboard
- **[REQ-HA-007]** Implement **health check endpoint** at `/health/` returning HTTP 200
- **[REQ-HA-008]** Enable **cross-zone load balancing** for even traffic distribution
- **[REQ-HA-009]** Configure SSL/TLS termination at load balancer

---

## 4. Database High Availability

### 4.1 Database Configuration

- **[REQ-HA-010]** Use managed database service with HA enabled (AWS RDS Multi-AZ, Cloud SQL HA)
- **[REQ-HA-011]** Enable **automatic failover** with standby replica in different AZ
- **[REQ-HA-012]** Configure **automated backups** with point-in-time recovery (PITR)
- **[REQ-HA-013]** Enable **read replicas** (minimum 1) for load distribution
- **[REQ-HA-014]** Implement **connection pooling** (pgbouncer/pgpool for PostgreSQL)

### 4.2 Data Persistence

- **[REQ-HA-015]** Daily automated backups retained for 30 days
- **[REQ-HA-016]** Weekly full backups with off-site replication
- **[REQ-HA-017]** Transaction log shipping to separate region (for disaster recovery)
- **[REQ-HA-018]** Database encryption at rest and in transit (TLS)

---

## 5. Session Management

### 5.1 Django Session Backend

- **[REQ-HA-019]** Configure **database-backed sessions** for persistence across instances
  ```python
  SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
  ```
- **[REQ-HA-020]** Implement **Redis Cluster** for session cache (3+ nodes)
- **[REQ-HA-021]** Configure session timeout: 2 hours idle, 24 hours absolute
- **[REQ-HA-022]** Enable **session cleanup** cron job to purge expired sessions

### 5.2 Static & Media Files

- **[REQ-HA-023]** Serve static files via **CDN** (CloudFlare, AWS CloudFront, etc.)
- **[REQ-HA-024]** Use **object storage** (S3, GCS, Azure Blob) for media files with versioning
- **[REQ-HA-025]** Configure **cross-region replication** for critical assets
- **[REQ-HA-026]** Enable **cache busting** with hashed filenames

---

## 6. Application Layer HA

### 6.1 Django Configuration

- **[REQ-HA-027]** Set `DEBUG = False` in production
- **[REQ-HA-028]** Configure **multiple ALLOWED_HOSTS** for load balancer and failover
- **[REQ-HA-029]** Implement **custom error pages** (500, 502, 503, 504)
- **[REQ-HA-030]** Enable **gzip compression** for static assets
- **[REQ-HA-031]** Configure **connection keep-alive** and timeouts

### 6.2 Background Tasks

- **[REQ-HA-032]** Use **Redis Queue (RQ)** or **Celery** with separate worker pool
- **[REQ-HA-033]** Deploy **3+ Celery workers** with automatic retry on failure
- **[REQ-HA-034]** Configure **dead letter queue** for failed tasks
- **[REQ-HA-035]** Monitor queue length and set alerts for backlog

---

## 7. Monitoring & Alerting

### 7.1 Health Monitoring

- **[REQ-HA-036]** Deploy **application monitoring** (New Relic, Datadog, or Prometheus)
- **[REQ-HA-037]** Implement **synthetic monitoring** with uptime checks every 5 minutes
- **[REQ-HA-038]** Configure **log aggregation** (ELK stack, Loki, CloudWatch Logs)
- **[REQ-HA-039]** Set up **real-time alerting** for:
  - Instance health (CPU > 80%, Memory > 85%)
  - Database connections ( > 80% of max)
  - Response time (p95 > 2 seconds)
  - Error rate (5xx > 1%)

### 7.2 Dashboards

- **[REQ-HA-040]** Create Grafana/dashboard showing:
  - Request rate and latency
  - Instance health by AZ
  - Database performance metrics
  - Cache hit/miss ratios
  - Error rates by endpoint

---

## 8. Disaster Recovery (DR)

### 8.1 Backup Strategy

- **[REQ-HA-041]** **Real-time replication** to standby region (warm standby)
- **[REQ-HA-042]** **Database snapshots** taken daily, retained 90 days
- **[REQ-HA-043]** **Code repository backups** (Git mirror) stored separately
- **[REQ-HA-044]** **Configuration files** stored in version-controlled IaC (Terraform/CloudFormation)

### 8.2 Failover Procedure

- **[REQ-HA-045]** Documented **runbook** for manual failover execution
- **[REQ-HA-046]** Quarterly **DR drills** simulating region failure
- **[REQ-HA-047]** Automated **DNS failover** using Route 53/Cloud DNS health checks
- **[REQ-HA-048]** **Load balancer failover** within 30 seconds of instance failure

---

## 9. Security & Compliance

### 9.1 HA Security

- **[REQ-HA-049]** All inter-service communication over **TLS 1.3**
- **[REQ-HA-050]** **Network segmentation** using VPC/subnets across AZs
- **[REQ-HA-051]** **WAF (Web Application Firewall)** with rate limiting
- **[REQ-HA-052]** **DDoS protection** (CloudFlare/AWS Shield Advanced)
- **[REQ-HA-053]** **Secrets management** (AWS Secrets Manager, HashiCorp Vault)

### 9.2 Compliance

- **[REQ-HA-054]** Audit logs retained for 365 days
- **[REQ-HA-055]** Regular security scans (weekly) on all instances
- **[REQ-HA-056]** **Vulnerability patching** SLA: critical patches within 24 hours

---

## 10. Performance & Scalability

### 10.1 Auto-Scaling Policies

- **[REQ-HA-057]** Scale-out trigger: CPU > 70% averaged over 5 minutes
- **[REQ-HA-058]** Scale-in trigger: CPU < 30% averaged over 15 minutes
- **[REQ-HA-059]** Minimum instances: 2 (for HA)
- **[REQ-HA-060]** Maximum instances: 10 (budget cap)
- **[REQ-HA-061]** **Scheduled scaling** for anticipated traffic patterns (business hours)

### 10.2 Caching Strategy

- **[REQ-HA-062]** **Redis Cluster** (3 nodes) for Django cache backend
- **[REQ-HA-063]** **CDN caching** for static assets (TTL: 1 year)
- **[REQ-HA-064]** Database query caching with Redis
- **[REQ-HA-065]** Template fragment caching for expensive renders

---

## 11. Testing & Validation

### 11.1 HA Testing

- **[REQ-HA-066]** Monthly **chaos engineering** tests (kill random instance)
- **[REQ-HA-067]** Quarterly **load testing** to verify scaling triggers (target: 1000 concurrent users)
- **[REQ-HA-068]** Biannual **full DR failover** test
- **[REQ-HA-069]** **Automated integration tests** covering all critical paths

### 11.2 Deployment Process

- **[REQ-HA-070]** **Blue-green deployments** with zero-downtime release
- **[REQ-HA-071]** **Canary releases** for major updates (5% traffic first)
- **[REQ-HA-072]** **Rollback capability** within 5 minutes of failed deployment
- **[REQ-HA-073]** **Immutable infrastructure** - recreate instances, don't modify in-place

---

## 12. Cost Optimization

### 12.1 HA Cost Controls

- **[REQ-HA-074]** Use **spot instances** for non-critical components (Celery workers)
- **[REQ-HA-075]** Implement **auto-scaling schedule** to scale down during off-hours (night/weekend)
- **[REQ-HA-076]** Monitor and alert on **unutilized resources** (> 7 days)
- **[REQ-HA-077]** Use **reserved instances/savings plans** for baseline capacity (2-3 instances)

---

## 13. Implementation Roadmap

### Phase 1: Core HA (Weeks 1-2)
- Deploy load balancer + 2 web instances in 2 AZs
- Configure managed database with Multi-AZ
- Setup Redis cluster for sessions/cache
- Implement health checks and monitoring

### Phase 2: Resilience (Weeks 3-4)
- Add auto-scaling group
- Configure CDN + object storage
- Implement CI/CD with blue-green deployment
- Setup backup and recovery procedures

### Phase 3: Optimization (Weeks 5-6)
- Implement caching strategy
- Add WAF and security hardening
- Configure advanced monitoring dashboards
- Conduct initial chaos testing

### Phase 4: DR & Compliance (Weeks 7-8)
- Setup cross-region replication (warm standby)
- Implement DR runbook and conduct drill
- Configure audit logging and compliance reports
- Performance testing and tuning

---

## 14. Success Metrics

| KPI | Target | Measurement |
|-----|--------|-------------|
| **Uptime** | ≥ 99.9% | Monthly monitoring report |
| **Mean Time To Recovery (MTTR)** | < 15 min | Incident post-mortem |
| **Deployment Success Rate** | ≥ 98% | CI/CD pipeline metrics |
| **Response Time (p95)** | < 500ms | Application Performance Monitoring |
| **Database Failover Time** | < 30 sec | DR test results |
| **Backup Success Rate** | 100% | Backup job logs |

---

## 15. Maintenance & Operations

### 15.1 Operational Procedures

- Daily: Review error logs and performance metrics
- Weekly: Security patches on non-production, then production (if critical)
- Monthly: DR drill (rotate), capacity planning review
- Quarterly: Full HA architecture review, cost optimization audit

### 15.2 Documentation Requirements

- **Architecture diagrams** (current and target states)
- **Runbooks** for all failure scenarios
- **Contact matrix** with escalation paths
- **Change management** procedure for all infrastructure modifications

---

## Appendix A: Django Settings Snippet

```python
# settings.py - HA enhancements

# Multiple instances behind load balancer
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = ['www.geopramtech.com', 'api.geopramtech.com', 'dashboard.geopramtech.com']

# Database connection retry
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 300,  # Persistent connections
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}

# Cache configuration (Redis Cluster)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis-cluster:6379',
        'TIMEOUT': 300,
    }
}

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 7200  # 2 hours

# Static files (CDN)
STATIC_URL = 'https://cdn.geopramtech.com/static/'
STORAGES = {
    'staticfiles': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
    }
}
```

---

## Appendix B: Health Check Endpoint

Create `geopram_tech/health/` view:

```python
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request):
    checks = {
        'database': False,
        'cache': False,
        'status': 'unhealthy'
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks['database'] = True
    except Exception:
        pass
    
    # Check cache
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            checks['cache'] = True
    except Exception:
        pass
    
    if all([checks['database'], checks['cache']]):
        checks['status'] = 'healthy'
        return JsonResponse(checks, status=200)
    
    return JsonResponse(checks, status=503)
```

---

## Appendix C: Nginx Configuration (Web Server)

```nginx
upstream django_backend {
    least_conn;
    server web-01.internal:8000 max_fails=3 fail_timeout=30s;
    server web-02.internal:8000 max_fails=3 fail_timeout=30s;
    server web-03.internal:8000 backup;
}

server {
    listen 443 ssl http2;
    server_name www.geopramtech.com;
    
    # SSL configuration
    ssl_certificate /etc/ssl/certs/geopramtech.crt;
    ssl_certificate_key /etc/ssl/private/geopramtech.key;
    ssl_protocols TLSv1.3 TLSv1.2;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    
    location / {
        proxy_pass http://django_backend;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
    
    location /health/ {
        proxy_pass http://django_backend;
        access_log off;
    }
    
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 16. WSGI & Application Server Configuration

### 16.1 WSGI Server Requirements

- **[REQ-HA-078]** Use **Gunicorn** or **uWSGI** as WSGI application server with multiple worker processes
- **[REQ-HA-079]** Configure **pre-fork model**: (2 × CPU cores) + 1 workers per instance
- **[REQ-HA-080]** Set worker timeout to 120 seconds, graceful timeout to 30 seconds
- **[REQ-HA-081]** Implement **max requests** of 10,000 with **max requests jitter** of 1,000 to prevent memory leaks
- **[REQ-HA-082]** Enable **worker lifecycle logging** for debugging
- **[REQ-HA-083]** Use **shared sockets** (Unix domain socket or TCP) behind load balancer

### 16.2 Gunicorn Configuration

Create `gunicorn.conf.py`:

```python
import multiprocessing
import os

# Server socket
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'sync')
worker_connections = 1000
max_requests = 10000
max_requests_jitter = 1000
timeout = 120
graceful_timeout = 30
keepalive = 5

# Logging
errorlog = '-'
loglevel = 'warning'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'geopram_tech-gunicorn'

# Server mechanics
daemon = False
raw_env = ['DJANGO_SETTINGS_MODULE=geopram_tech.settings.production']
pidfile = '/run/gunicorn/geopramtech.pid'
user = os.getenv('GUNICORN_USER', 'www-data')
group = os.getenv('GUNICORN_GROUP', 'www-data')

# SSL configuration (if terminating at Gunicorn)
# keyfile = '/etc/ssl/private/geopramtech.key'
# certfile = '/etc/ssl/certs/geopramtech.crt'
```

### 16.3 uWSGI Configuration

Create `uwsgi.ini`:

```ini
[uwsgi]
# Django project
project = geopramtech
base = /app

chdir = %(base)
home = /app/.venv
module = %(project).wsgi:application

# Master & processes
master = true
processes = %(%k * 2 + 1)

# Socket
socket = /run/uwsgi/geopramtech.sock
chmod-socket = 660
vacuum = true
die-on-term = true

# Limits
harakiri = 120
harakiri-verbose = true
limit-as = 512

# Request handling
buffer-size = 32768
post-buffering = 8192

# Stats
stats = /run/uwsgi/geopramtech.stats

# Logging
logto = /var/log/uwsgi/%n.log
log-4xx = true
log-5xx = true

# Background tasks (spooler)
spooler = /var/spool/uwsgi
```

### 16.4 Systemd Service (Gunicorn)

Create `/etc/systemd/system/geopramtech.service`:

```systemd
[Unit]
Description=GEOPRAMTECH Django Gunicorn Service
Documentation=https://geopramtech.com
After=network.target postgresql.service redis.service
Wants=network.target

[Service]
Type=notify
NotifyAccess=main

# User & Group
User=www-data
Group=www-data

# Working directory
WorkingDirectory=/app/geopramtech

# Environment
Environment="DJANGO_SETTINGS_MODULE=geopram_tech.settings.production"
Environment="PYTHONPATH=/app"

# ExecStart
ExecStart=/app/.venv/bin/gunicorn \
    --config /app/gunicorn.conf.py \
    --preload \
    geopram_tech.wsgi:application

# Restart policy
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=60
StartLimitBurst=3

# Limits
LimitNOFILE=65535
LimitNPROC=4096

# Security hardening
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/app /var/log/geopramtech /run/gunicorn
NoNewPrivileges=true
PrivateDevices=true

# Timeout
TimeoutStartSec=60
TimeoutStopSec=30
KillMode=mixed
KillSignal=SIGQUIT

[Install]
WantedBy=multi-user.target
```

**Systemd commands:**

```bash
# Start & enable
sudo systemctl daemon-reload
sudo systemctl start geopram
sudo systemctl enable geopram

# Status & logs
sudo systemctl status geopram
sudo journalctl -u geopram -f

# Restart
sudo systemctl restart geopram
```

### 16.5 Supervisor Configuration (Alternative)

Create `/etc/supervisor/conf.d/geopram.conf`:

```ini
[program:geopram]
command=/app/.venv/bin/gunicorn --config /app/gunicorn.conf.py geopram.wsgi:application
directory=/app/geopramtech
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/geopramtech/gunicorn.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
stopwaitsecs=120
killasgroup=true
```

**Supervisor commands:**

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status geopramtech
sudo supervisorctl restart geopramtech
```

### 16.6 Nginx + Gunicorn Integration

Nginx config for proxying to Gunicorn Unix socket:

```nginx
upstream geopramtech_backend {
    # Unix socket (preferred)
    server unix:/run/gunicorn/geopramtech.sock fail_timeout=0;
    
    # Or TCP for distributed deployments
    # server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80;
    server_name www.geopramtech.com geopramtech.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name www.geopramtech.com;
    
    # SSL (managed by Let's Encrypt/CloudFlare)
    ssl_certificate /etc/ssl/certs/geopramtech.crt;
    ssl_certificate_key /etc/ssl/private/geopramtech.key;
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    
    # Client max body size (for uploads)
    client_max_body_size 50M;
    
    # Static files (served directly by Nginx)
    location /static/ {
        alias /app/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable, max-age=31536000";
        add_header Vary "Accept-Encoding";
        access_log off;
        try_files $uri $uri/ =404;
    }
    
    # Media files
    location /media/ {
        alias /app/media/;
        expires 7d;
        add_header Cache-Control "public, max-age=604800";
        try_files $uri $uri/ =404;
    }
    
    # Health check endpoint
    location /health/ {
        access_log off;
        proxy_pass http://geopramtech_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 3s;
        proxy_send_timeout 5s;
        proxy_read_timeout 5s;
    }
    
    # Main application (Django)
    location / {
        proxy_pass http://geopramtech_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        
        # Connection settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 4 32k;
        proxy_busy_buffers_size 64k;
        
        # Keepalive
        keepalive_timeout 65;
        keepalive_requests 1000;
        
        # WebSocket support (if using channels)
        # proxy_http_version 1.1;
        # proxy_set_header Upgrade $http_upgrade;
        # proxy_set_header Connection "upgrade";
    }
    
    # Deny access to sensitive files
    location ~ /\.(?!well-known) {
        deny all;
        log_not_found off;
    }
    
    location ~ ~$ {
        deny all;
        log_not_found off;
    }
}
```

### 16.7 Docker Deployment

`Dockerfile`:

```dockerfile
FROM python:3.11-slim-bookworm

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -d /app geopramtech && chown -R geopramtech:geopramtech /app

# Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy code
COPY . /app/
RUN chown -R geopram:geopram /app

# Collect static
USER geopram
RUN python manage.py collectstatic --noinput

# Nginx config
USER root
COPY nginx.conf /etc/nginx/nginx.conf
RUN chown -R geopram:geopram /var/log/nginx /var/cache/nginx

USER geopram

EXPOSE 8000
CMD ["sh", "-c", "gunicorn --config gunicorn.conf.py geopram_tech.wsgi:application"]
```

`docker-compose.yml` (production):

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: geopramtech
      POSTGRES_USER: geopramtech
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  web:
    build: .
    command: gunicorn --config gunicorn.conf.py geopram_tech.wsgi:application
    environment:
      DATABASE_URL: postgres://geopramtech:${DB_PASSWORD}@postgres/geopramtech
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY}
      DEBUG: "False"
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    expose:
      - 8000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - static_volume:/static
      - media_volume:/media
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - web
    restart: unless-stopped

  celery:
    build: .
    command: celery -A geopram_tech worker -l info --concurrency=4
    environment:
      DATABASE_URL: postgres://geopramtech:${DB_PASSWORD}@postgres/geopramtech
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
```

### 16.8 Kubernetes Deployment

`deployment.yaml` (1 replica controlled by HPA):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: geopramtech-web
  namespace: production
  labels:
    app: geopramtech
    tier: web
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: geopramtech
      tier: web
  template:
    metadata:
      labels:
        app: geopramtech
        tier: web
    spec:
      containers:
      - name: geopramtech
        image: geopramtech/geopramtech:${IMAGE_TAG}
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
         env:
        - name: DJANGO_SETTINGS_MODULE
          value: "geopram_tech.settings.production"
         - name: DATABASE_URL
           valueFrom:
             secretKeyRef:
               name: geopramtech-secrets
               key: database-url
         - name: SECRET_KEY
           valueFrom:
             secretKeyRef:
               name: geopramtech-secrets
               key: secret-key
         - name: REDIS_URL
           valueFrom:
             secretKeyRef:
               name: geopramtech-secrets
               key: redis-url
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        livenessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        startupProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
          failureThreshold: 30
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 30"]
         volumeMounts:
         - name: static-storage
           mountPath: /app/staticfiles
       volumes:
       - name: static-storage
         emptyDir: {}
       - name: django-settings
         secret:
           secretName: geopramtech-settings
      imagePullSecrets:
      - name: registry-secret
```

`hpa.yaml` (Horizontal Pod Autoscaler):

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: geopramtech-web-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: geopramtech-web
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 2
        periodSeconds: 30
      selectPolicy: Max
```

`service.yaml` (LoadBalancer service):

```yaml
apiVersion: v1
kind: Service
metadata:
  name: geopramtech-web
  namespace: production
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-interval: "30"
spec:
  selector:
    app: geopramtech
    tier: web
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  type: LoadBalancer
  sessionAffinity: ClientIP
  externalTrafficPolicy: Local
```

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-17 | Kilo | Initial HA requirements document |
| 1.1 | 2026-04-17 | Kilo | Added WSGI & application server section |
| 1.2 | 2026-04-17 | Kilo | Updated all references to use geopramtech project name |
