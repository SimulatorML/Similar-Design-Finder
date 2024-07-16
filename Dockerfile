# Test image for CICD
FROM alpine
CMD ["sh", "-c", "echo 'HEllo!?' && tail -f /dev/null"]
