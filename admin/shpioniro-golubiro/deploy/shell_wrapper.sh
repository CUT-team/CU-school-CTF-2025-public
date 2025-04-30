#!/bin/sh

echo "Приветствуем на нашем сервере! Попробуй подсмотреть флаг, прямо как Shpioniro Golubiro."

while true; do
    printf "> "
    read -r line

    if echo "$line" | grep -Eq '[|&;<>`$()]'; then
        echo "This command is not allowed"
        continue
    fi

    case "$line" in
        ls*|cat*|base32*|exit)
            eval "$line"
            ;;
        *)
            echo "This command is not allowed"
            ;;
    esac
done