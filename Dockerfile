FROM python:3-alpine3.18 as base

ENTRYPOINT ["tail"]
CMD ["-f","/dev/null"]