FROM alpine:latest

COPY setup.sh /setup.sh
COPY shell_wrapper.sh /usr/local/bin/shell_wrapper.sh
COPY ssh_wrapper.sh /usr/local/bin/ssh_wrapper.sh
COPY sshd_config /etc/ssh/sshd_config
COPY flag.png /home/cuctf/flag.png

RUN sh /setup.sh && rm /setup.sh

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]