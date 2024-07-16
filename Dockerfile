# Test image for CICD
FROM alpine
CMD ["sh", "-c", "echo 'hello!?' && tail -f /dev/null"]
