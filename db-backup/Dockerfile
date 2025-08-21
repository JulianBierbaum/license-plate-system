FROM postgres:14-alpine

WORKDIR /

# Copy the backup script
COPY backup-entrypoint.sh /backup-entrypoint.sh

# Install dcron AND tini
RUN apk add --no-cache dcron tini

# Create the crontab service to run every day at midnight
RUN echo '0 0 * * * /backup-entrypoint.sh' > /var/spool/cron/crontabs/root
RUN chmod +x /backup-entrypoint.sh

# Expose the volume where backups will be stored
VOLUME /backups

# Set tini as the entrypoint (fix for crond)
ENTRYPOINT ["/sbin/tini", "--"]

# Set the default command to start the cron daemon in the foreground.
CMD ["crond", "-f", "-l", "8"]