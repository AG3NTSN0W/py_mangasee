docker build -t snow/mangasee -f ./docker/app/dockerfile .    
docker run --rm -v /tmp/downloads:/downloads -v /tmp/config:/config snow/mangasee