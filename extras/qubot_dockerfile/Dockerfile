FROM ros:jazzy-ros-base-noble
#FROM arm64v8/ros:jazzy-ros-base-noble

# installing core programs
RUN apt-get update \
    && apt-get install -y \
    ros-jazzy-perception=0.11.0-1* \
    nano \
    python3-pip \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# delete default user 'ubuntu'
RUN userdel -r ubuntu

# create a new non-root user
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && mkdir /home/$USERNAME/.config && chown $USER_UID:$USER_GID /home/$USERNAME/.config


# set up sudo
RUN apt-get update \
  && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  && rm -rf /var/lib/apt/lists/*

# applications and libraries for development and testing
RUN apt-get update \
  && apt-get install -y \
  evtest \
  jstest-gtk \
  python3-serial \
  && rm -rf /var/lib/apt/lists/*
  
# ros2 utilities
RUN apt-get update \
  && apt-get install -y \
  ros-jazzy-turtlesim \
  ros-jazzy-joint-state-publisher \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-xacro \
  ros-jazzy-joy* \
  && rm -rf /var/lib/apt/lists/*


# other instalations required with non-sudo privileges
USER $USERNAME
RUN pip install modbus-crc --break-system-packages
RUN pip install pymodbus --break-system-packages
RUN pip install inputs --break-system-packages
RUN pip install opencv-python --break-system-packages
USER root

# add permissions to serial port communication
RUN usermod -aG dialout $USERNAME
  
# Create a workspace
RUN mkdir -p /home/$USERNAME/ros2_ws/src \
 && cd /home/$USERNAME/ros2_ws \
 && colcon build

# Copy the entrypoint and bashrc scripts
COPY entrypoint.sh /entrypoint.sh
COPY bashrc /home/$USERNAME/.bashrc

# Set up entrypoint and default command
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
CMD ["bash"]


