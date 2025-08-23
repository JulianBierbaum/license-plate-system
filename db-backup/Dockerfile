FROM postgres:14-alpine

WORKDIR /

# Copy the backup script
COPY backup_entrypoint.sh /backup_entrypoint.sh
COPY crontab_entrypoint.sh /crontab_entrypoint.sh

# Install dcron and tini
RUN apk add --no-cache dcron tini

# Make scripts executable
RUN chmod +x /backup_entrypoint.sh /crontab_entrypoint.sh

# Expose the volume where backups will be stored
VOLUME /backups

# Use tini as entrypoint (fix for crond)
ENTRYPOINT ["/sbin/tini", "--"]

# Start crontab_entrypoint.sh
CMD ["/crontab_entrypoint.sh"]
