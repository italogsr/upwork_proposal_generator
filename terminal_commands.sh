# Check PostgreSQL service status
sudo systemctl status postgresql

# If it's not running, start it
sudo systemctl start postgresql

# To enable PostgreSQL to start on boot
sudo systemctl enable postgresql