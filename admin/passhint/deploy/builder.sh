#!/bin/bash

network_name="isolated_network"
if docker network ls | grep -q "$network_name"; then
    echo "Network $network_name exists."
else
    echo "Network $network_name does not exist. Creating the network..."
    docker network create "$network_name"
    if [ $? -eq 0 ]; then
        echo "Network $network_name created successfully."
    else
        echo "Failed to create network $network_name."
        exit 1
    fi
fi

for dir in */; do
    taskname=$(basename "$dir" | tr '[:upper:]' '[:lower:]')

    if [ -f "$dir/config.sh" ]; then
        source "$dir/config.sh"

        if [ -f "$dir/pre_install.sh" ]; then
            echo "Running pre_install.sh..."
            bash "$dir/pre_install.sh"
            if [ $? -ne 0 ]; then
                echo "pre_install.sh failed for $taskname."
                continue
            fi
        else
            echo "Not found pre_install.sh"
        fi

        if id "$taskname" &>/dev/null; then
            echo "User $taskname exists. Deleting user and home directory."
            sudo sed -i "/^$taskname:/d" /etc/passwd
            sudo userdel -r "$taskname" > /dev/null
        else
            echo "User $taskname does not exist."
        fi

        if getent group "$taskname" &>/dev/null; then
            echo "Group $taskname exists. Deleting group."
            sudo groupdel "$taskname"
        else
            echo "Group $taskname does not exist."
        fi

        if [ -d "/home/$taskname" ]; then
            echo "Home directory /home/$taskname exists. Deleting home directory."
            sudo rm -rf "/home/$taskname"
        else
            echo "Home directory /home/$taskname does not exist."
        fi

        build_command="docker build -t $taskname $dir > /dev/null"
        eval "$build_command"
        if [ $? -ne 0 ]; then
            echo "Docker build failed for $taskname."
            continue
        fi

        script_path="/opt/shells/$taskname.sh"
        sudo mkdir -p /opt/shells/
        sudo echo "#!/bin/sh" > "$script_path"

        command="/usr/bin/docker run -it --rm"

        if [[ "$privileged_mode" =~ ^(True|true|1)$ ]]; then
            command="$command --privileged"
        fi

        if [[ "$isolated_network" =~ ^(True|true|1)$ ]]; then
            command="$command --network $network_name"
        fi

        if [ -n "$options" ]; then
            command="$command $options"
        fi

        command="$command $taskname"

        sudo echo "$command" >> "$script_path"
        sudo chmod +x "$script_path"

        sudo groupadd "$taskname" 2>/dev/null || true
        sudo useradd -m -s "$script_path" -g "$taskname" "$taskname" 2>/dev/null || true
        echo "$taskname:$taskname" | sudo chpasswd
        sudo usermod -aG docker "$taskname" 2>/dev/null || true
        sudo usermod -aG "$taskname" "$taskname" 2>/dev/null || true
    else
        echo "config.sh file not found for $taskname"
    fi
done