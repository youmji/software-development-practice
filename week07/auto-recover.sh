
#!/bin/bash

cd "$HOME/software-development-practice" || exit 1

while true
do
    running=$(docker compose -f week07/compose.yaml -p week07 ps --status running -q | wc -l)

    echo "현재 실행 중인 web 컨테이너: ${running}개"

    if [ "$running" -lt 3 ]; then
        echo "컨테이너가 부족합니다. 복구를 시작합니다."
        docker compose -f week07/compose.yaml -p week07 up -d --scale web=3
    fi

    sleep 10
done
