FROM alpine
RUN apk add --update docker openrc
RUN rc-update add docker boot
