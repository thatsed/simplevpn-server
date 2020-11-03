# SimpleVPN Server

## Deployment

```bash
~$ docker run --rm -d \
      --cap-add NET_ADMIN \
      --env SIMPLE_VPN_ENDPOINT=localhost \
      --env SIMPLE_VPN_SUBNET=10.100.20.0/24 \
      -p 8000:8000 \
      -p 1194:1194 \
      -v /opt/simplevpn:/data \
      --name simplevpn \
      registry.gitlab.com/simplevpn/simplevpn-server
```

### First Setup

#### User creation
    ```bash
    ~$ docker exec -it simplevpn python manage.py createsuperuser
    Username (leave blank to use 'root'): admin_user_name
    Email address: 
    Password: 
    Password (again): 
    Superuser created successfully.
    ```
