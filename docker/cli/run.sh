docker build -t snow/mangasee_cli -f ./docker/cli/dockerfile .    
docker run --rm -v /tmp/downloads:/downloads -v /tmp/config:/config snow/mangasee_cli $@