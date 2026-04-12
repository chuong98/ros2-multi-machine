# SETUP ISAAC-SIM and ISAAC ROS with DOCKER for REMOTE DEVELOPMENT

## 1. ISAAC-SIM on Remote Server

Reference: https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/install_container.html 

Steps: 
1. Pull the latest Isaac Sim container image from NVIDIA GPU Cloud (NGC):
```bash
docker pull nvcr.io/nvidia/isaac-sim:5.1.0
```
2. Create Folders to store the ISAAC-SIM data and configuration files:
```bash
mkdir -p ~/docker/isaac-sim/cache/main/ov
mkdir -p ~/docker/isaac-sim/cache/main/warp
mkdir -p ~/docker/isaac-sim/cache/computecache
mkdir -p ~/docker/isaac-sim/config
mkdir -p ~/docker/isaac-sim/data/documents
mkdir -p ~/docker/isaac-sim/data/Kit
mkdir -p ~/docker/isaac-sim/logs
mkdir -p ~/docker/isaac-sim/pkg
sudo chown -R 1234:1234 ~/docker/isaac-sim
```
3. Run the container with the following command:
```bash
isaac_sim/scripts/docker_run.sh
```
4. To attach to the running container, use the following command `isaac_sim/scripts/docker_exe.sh` or directly:   

```bash
docker exec -it isaac-sim bash
```
5. In the container, you can start Isaac Sim with the following command:
```bash
./runheadless.sh
```
6. Turn WebRTC on your remote server
Select the IP address of your remote server, e.g. 192.168.120.111.
Make sure the port 49100 is forwarded with VScode.
## 2. ISAAC ROS on Remote Server

Use `isaac-ros-cli` to build and run ROS packages in the container. Reference: `https://github.com/NVIDIA-ISAAC-ROS/isaac-ros-cli`
1. Install `isaac-ros-cli` on your local machine:
```bash
sudo apt-get install isaac-ros-cli
```
2. Add the following lines to your `.zshrc` file to set the environment variables for ISAAC-SIM and ISAAC-ROS workspaces:
```bash
export ISAAC_DIR="$HOME/docker/isaac-sim/"
export ISAAC_ROS_WS="$HOME/Workspace/isim/IsaacSim-ros_workspaces/jazzy_ws"
```
Note: You can clone the `IsaacSim-ros_workspaces` repository and follow their example workspaces, e.g. `jazzy_ws` or `humble_ws`, to build your ROS packages. For example, to clone the repository and use the `jazzy_ws` workspace:
```bash
git clone git@github.com:isaac-sim/IsaacSim-ros_workspaces.git
export ISAAC_ROS_WS="$HOME/Workspace/isim/IsaacSim-ros_workspaces/jazzy_ws"
```
3. Source the `.zshrc` file to apply the changes:
```bash
source ~/.zshrc
```
4. Build your ROS packages in the `ISAAC_ROS_WS` workspace and run them in the container using `isaac-ros-cli`. For example, to build the workspace:
```bash
# Initialize environment (pick a mode)
sudo isaac-ros init <docker|venv|baremetal> # choose one of the 3 options
# Activate environment
isaac-ros activate
```

## 3. Local Development with ROS Docker Container
1. Build the ROS docker image with the following command:
```bash
cd local
# Default (humble)
docker compose build

# Jazzy
ROS_DISTRO=jazzy docker compose build
```

2. Run the ROS docker container with the following command:
```bash
cd local
# Default (humble)
./docker_run.sh

# Jazzy
./docker_run.sh ros2-jazzy:foxglove ros-jazzy
```