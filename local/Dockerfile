ARG ROS_DISTRO=humble
FROM ros:${ROS_DISTRO}
ARG ROS_DISTRO=humble
ARG USERNAME=chuongnguyen
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME
RUN useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
#
# [Optional] Add sudo support. Omit if you don't need to install software after connecting.
RUN apt-get update && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get upgrade -y \
    && apt-get install -y \
        ament-cmake \
        ccls \
        python3-colcon-common-extensions \
        python3-pip \
        clang \
        clang-format \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /home/$USERNAME/.bashrc
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-demo-nodes-cpp \
    ros-${ROS_DISTRO}-foxglove-bridge \
    ros-${ROS_DISTRO}-tf2-ros \
    ros-${ROS_DISTRO}-turtlesim && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV SHELL=/bin/bash

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME
CMD ["/bin/bash"]
