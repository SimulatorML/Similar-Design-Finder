# Test image for CICD
FROM alpine
CMD ["sh", "-c", "echo 'HeLlo!?' && tail -f /dev/null"]
