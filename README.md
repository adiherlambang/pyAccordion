# pyAccordion v.1

before run the apps.

Install any depedency for the apps by running these command,
pip install -r requirements.txt
pip install gunicorn

to setup credential for gmail services,
  1. create folder xetc
  2. upload credential json from Google Cloud Platform here.

setup gUnicorn to run flask as services

  1. sudo nano /etc/systemd/system/myapp_gunicorn.service
      Replace myapp with your application's name
  2. add the following content to the file :
      [Unit]
      Description=Gunicorn instance for myapp
      After=network.target
      
      [Service]
      User=your_username  # Replace with your username
      Group=your_group    # Replace with your group name
      WorkingDirectory=/path/to/your/app
      ExecStart=/usr/local/bin/gunicorn --workers 3 --bind unix:/path/to/your/app/app.sock your_app_module:app
      Restart=always
      
      [Install]
      WantedBy=multi-user.target

      Make sure to replace your_username, your_group, /path/to/your/app, your_app_module:app, and any other relevant values with your specific information.
  3. sudo systemctl daemon-reload
  4. sudo systemctl enable myapp_gunicorn
     sudo systemctl start myapp_gunicorn
