ARG ROS_DISTRO=humble
FROM ros:${ROS_DISTRO}
ARG ROS_DISTRO=humble
ARG USERNAME=chuongnguyen
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Detect if user/group exists; rename existing UID/GID entries or create new ones
RUN if ! getent group $USER_GID > /dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME; \
    else \
        groupmod -n $USERNAME $(getent group $USER_GID | cut -d: -f1) 2>/dev/null || true; \
    fi
RUN if id -u $USERNAME > /dev/null 2>&1; then \
        echo "User $USERNAME already exists"; \
    elif getent passwd $USER_UID > /dev/null 2>&1; then \
        EXISTING=$(getent passwd $USER_UID | cut -d: -f1) \
        && usermod -l $USERNAME -d /home/$USERNAME -m "$EXISTING"; \
    else \
        useradd --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi
RUN mkdir -p /home/$USERNAME && chown $USER_UID:$USER_GID /home/$USERNAME
#
# [Optional] Add sudo support. Omit if you don't need to install software after connecting.
RUN apt-get update && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get upgrade -y \
    && apt-get install -y \
        ros-${ROS_DISTRO}-ament-cmake \
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
