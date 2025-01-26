#!/bin/bash

SERVICE_NAME="название_сервиса"

SOURCE_DIR="/opt/misc/$SERVICE_NAME"
TARGET_DIR="/srv/data/$SERVICE_NAME"

UNIT_LIST=$(systemctl list-units --all --full --no-legend --no-pager --type=service --all --state=running --pattern="$SERVICE_NAME-*" | awk '{print $1}')

for UNIT in $UNIT_LIST; do
    echo "Processing unit: $UNIT"

    systemctl stop "$UNIT"

    if [ -d "$SOURCE_DIR" ]; then
        mkdir -p "$TARGET_DIR"
        mv "$SOURCE_DIR"/* "$TARGET_DIR"
    else
        echo "Error: Source directory $SOURCE_DIR not found."
        exit 1
    fi

    UNIT_FILE=$(systemctl show -p FragmentPath --value "$UNIT")
    sed -i "s|WorkingDirectory=$SOURCE_DIR|WorkingDirectory=$TARGET_DIR|g" "$UNIT_FILE"
    sed -i "s|ExecStart=$SOURCE_DIR/foobar-daemon|ExecStart=$TARGET_DIR/foobar-daemon|g" "$UNIT_FILE"

    systemctl start "$UNIT"
    
    echo "Unit $UNIT has been updated and started."
done

echo "All units have been processed."