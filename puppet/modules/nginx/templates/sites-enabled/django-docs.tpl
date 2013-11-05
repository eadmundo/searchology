server {
    listen 80 default_server;
    server_name docs.djangoproject.dev;

    location / {
        root /vagrant/django-docs-1.5-en;
        index  index.html;
    }
}