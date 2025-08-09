sudo cp deploy/uw-notify.service /etc/systemd/system/uw-notify.service
sudo systemctl daemon-reload
sudo systemctl restart uw-notify
sudo systemctl status uw-notify --no-pager -l