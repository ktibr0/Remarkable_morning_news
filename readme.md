

git clone https://github.com/ktibr0/Remarkable_morning_news
cd Remarkable_morning_news
mkdir -p ./config ./data ./app
sudo chown -R 1000:1000 ./data ./config ./app


docker compose up -d --build


docker ps

look for rmapi container ID


docker exec -it "rmapi container ID"  /bin/sh #without ""
rmapi



go to https://my.remarkable.com/device/browser?showOtp=true
copy verification code and insert to command line









https://github.com/ddvk/rmapi


https://github.com/gotenberg/gotenberg

