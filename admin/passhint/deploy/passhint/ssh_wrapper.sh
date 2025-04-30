#!/bin/sh

case "$SSH_ORIGINAL_COMMAND" in
    scp*|sftp*)
        echo "Access denied"
        exit 1
        ;;
    "")
        exec /bin/sh
        ;;
    *)
        echo "Access denied"
        exit 1
        ;;
esac
