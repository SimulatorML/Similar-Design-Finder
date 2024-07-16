# Test image for CICD
FROM alpine
CMD ["sh", "-c", "echo 'Hello Wo!?' && tail -f /dev/null"]

