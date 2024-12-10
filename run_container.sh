xhost +local:

container_name="kalibr"
bag=${1-"close.bag"}

if docker ps -a --format '{{.Names}}' | grep -q $container_name; then
  echo "removing existing container: $container_name"
  docker rm -f $container_name
fi

docker run -id \
  --name $container_name \
  --network=host \
  --ipc=host \
  --memory=8g \
  --memory-swap=-1 \
  -v `pwd`/config/:/root/config/ \
  --env=DISPLAY \
  kalibr bash

docker exec -it kalibr bash -c \
  "source /opt/ros/noetic/setup.bash \
  && source /catkin_ws/devel/setup.bash \
  && cd /root/config/ \
  && rosrun kalibr kalibr_calibrate_cameras \
    --target /root/config/april_6x6.yaml \
    --models pinhole-radtan pinhole-radtan \
    --topics /cam0/image_raw /cam2/image_raw \
    --bag /root/config/$bag"
