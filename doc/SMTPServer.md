
# <span style="color:CornflowerBlue"> SMTP Server


## <span style="color:Teal">Installing fake SMTP on Mac

1. Open terminal at Mac OS
2. Type this to install mailhog `brew install mailhog`
	> **Notes:**
		To start mailhog now and restart at login
			`brew services start mailhog`
		If you don't want a background service you can just run:
  			`/opt/homebrew/opt/mailhog/bin/MailHog -api-bind-addr 127.0.0.1:8025 -smtp-bind-addr 127.0.0.1:1025 -ui-bind-addr 127.0.0.1:8025`
3. Execute MailHog at the terminal `mailhog`

4. SMTP Settings
	```
		Host: localhost
		Port: 1025
		Username: (none)
		Password: (none)
		TLS: no
	```
5. Sample python code to send email using smtplib. Smtplib built in with python so no need for pip install
	```python
 	import smtplib
	from email.mime.text import MIMEText

	msg = MIMEText("Verify your email")
	msg["Subject"] = "Signup Verification"
	msg["From"] = "no-reply@local.dev"
	msg["To"] = "test@example.com"

	with smtplib.SMTP("localhost", 1025) as server:
    server.send_message(msg)
	```
6. At pyCharm, copy and paste the above code in a new python file and execute.

7. Verify if email is sent successfully at web browser using the below URL
	`http:\\localhost:8025`

8. This will let you continue your development till you deploy to production.

9. Also read something like this for <mark>Fake SMS</mark> for development of 2FA.
