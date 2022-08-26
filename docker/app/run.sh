docker build -t snow/mangasee -f ./docker/app/dockerfile .    
docker run --rm -p 4200:80 -v /tmp/downloads:/downloads -v /tmp/config:/config snow/mangasee