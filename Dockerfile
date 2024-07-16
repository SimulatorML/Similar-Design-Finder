# Test image for CICD
FROM alpine
CMD ["sh", "-c", "echo 'Hello' && tail -f /dev/null"]
