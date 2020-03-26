# stockx-future-releases
## v1.1
Prerequisites:
1. Install Firefox https://www.mozilla.org/en-US/firefox/new/
2. Download corresponding Firefox webdriver that support your Firefox version from here: https://github.com/mozilla/geckodriver/releases
3. Turn on Less secure app access if your are using Gmail account to send email: https://support.google.com/accounts/answer/6010255
4. Install selenium via pip 
```bash
pip3 install selenium 
```
5. Python 3.5 + is required

Note: 
2020-03-25:
Chrome webdriver can be detected and no longer works, use Firefox instead.
Firefox 74.0 is tested as of today.
### Update the following lines in main.py
```python
email_server = ""
email_user = ""
email_pass = ""
send_to_email = ""
```
```text
Note: send_to_email can be send as text if your carrier support that. For example AT&T in the US: <phone number>@txt.att.net.
```


###Run main.py
```bash
python3 main.py
```



