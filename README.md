# ukubuka

docker build -t ukubuka_app .
docker run --name ukubuka_app -d --restart always -p 80:80 ukubuka_app