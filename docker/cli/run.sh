docker build -t snow/mangasee_cli -f ./docker/cli/Dockerfile-cli .    
docker run --rm -v /tmp/downloads:/downloads snow/mangasee_cli $@