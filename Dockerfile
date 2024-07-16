# Test image for CICD
FROM alpine
CMD ["sh", "-c", "echo 'Hel' && tail -f /dev/null"]
