docker build -t snow/mangasee .    
docker run --rm -v /tmp/downloads:/downloads -v /tmp/config:/config snow/mangasee $@