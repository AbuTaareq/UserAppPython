FROM postgres:17.7-alpine
COPY *.sql /docker-entrypoint-initdb.d/

# NOTES:
# ------------
# In order to see list of files copied, use the command below at db folder
# Run this command from compose folder /UserAppPython
# docker build -f ./db/Dockerfile --progress=plain --no-cache -t postgres:latest ./db
#
# To inspect the build image to see sql files:
# docker run --rm -it postgres:latest sh
#