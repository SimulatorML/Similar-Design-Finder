# Test image for CICD
FROM alpine
CMD ["sh", "-c", "echo 'Lol' && tail -f /dev/null"]
