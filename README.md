# Gaia ZAP Pipeline

# Gaia

## Build Dockerfile

```bash
docker build -t we45_gaia -f Dockerfile .
```

## Run Dockerfile
```bash
docker run -d --env VARIABLE1=foobar TARGET_IP=$(curl -XGET -s http://checkip.amazonaws.com/)
 --net=host -v $PWD:/data we45_gaia:latest
```
