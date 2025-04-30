FROM ubuntu:latest

RUN apt update && apt install -y gcc libc-dev strace bash

WORKDIR /home/cuctf

COPY app.c /home/cuctf/app.c
COPY entrypoint /entrypoint
COPY ssh_wrapper.sh /usr/local/bin/ssh_wrapper.sh
COPY sshd_config /etc/ssh/sshd_config

RUN echo '#!/bin/sh' > /etc/banner \
    && echo 'echo "\n##########################################################"' >> /etc/banner \
    && echo 'echo "# – Алло, Виктор, можете говорить?!                      #"' >> /etc/banner \
    && echo 'echo "# – Да, здравствуйте                                     #"' >> /etc/banner \
    && echo 'echo "# – У нас оно опять не работает, сегодня на работу       #"' >> /etc/banner \
    && echo 'echo "#   пришла, компьютер включила, открываю, ни в какую     #"' >> /etc/banner \
    && echo 'echo "# – Пробовали перезагружать?                             #"' >> /etc/banner \
    && echo 'echo "# – Да конечно, Андрей тоже копался, да ничего не вышло, #"' >> /etc/banner \
    && echo 'echo "#   вся надежда на вас 🙏                                #"' >> /etc/banner \
    && echo 'echo "# – Ладно, выезжаю, ждите                                #"' >> /etc/banner \
    && echo 'echo "##########################################################"' >> /etc/banner \
    && chmod +x /etc/banner

RUN gcc -o app app.c -O3 -fPIC -fomit-frame-pointer -ffunction-sections -fdata-sections -fvisibility=hidden -flto -Wl,--strip-all -Wl,--gc-sections -Wl,-z,relro,-z,now -s
RUN chmod +x /home/cuctf/app
RUN chmod +x /entrypoint
RUN rm -rf app.c

RUN echo "* soft nofile 1024" >> /etc/security/limits.conf && \
    echo "* hard nofile 2048" >> /etc/security/limits.conf

RUN useradd -m -s /bin/bash cuctf && \
    echo "cuctf:cuctf" | chpasswd

RUN chown -R cuctf:cuctf /home/cuctf && \
    chmod -R 755 /home/cuctf

ENTRYPOINT ["/entrypoint"]