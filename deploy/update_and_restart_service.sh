sudo cp deploy/uw-notify.service /etc/systemd/system/uw-notify.service
sudo cp deploy/uw-notify-poller.service /etc/systemd/system/uw-notify-poller.service
sudo systemctl daemon-reload
sudo systemctl restart uw-notify
sudo systemctl restart uw-notify-poller
