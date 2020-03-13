export DOCKER_IMAGE_TAG=$(git log --format="%H" -n 1)
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml push
export DOCKER_IMAGE_TAG=latest
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml push
