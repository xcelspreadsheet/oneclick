
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import redirect
from flask import render_template, redirect, url_for
from flask import request
import urllib
import zlib

app = Flask(__name__)

def utf8len(s):
    return len(s.encode('utf-8'))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template('index.html')

@app.route("/created", methods=["GET","POST"])
def renderCreated():
    if request.method == "POST":
        createdRecipients = " ".join(request.form['recipients'].replace(',', ' ').split()).replace(" ", ',')
        createdCC = " ".join(request.form['cc'].replace(',', ' ').split()).replace(" ", ',')
        createdBCC = " ".join(request.form['bcc'].replace(',', ' ').split()).replace(" ", ',')
        createdSubject = request.form['subject'].strip().replace('\n', ' ')
        createdMessage = urllib.parse.quote(request.form['message'].strip())
        createdPurpose = urllib.parse.quote(request.form['purpose'].strip())

        recipients = createdRecipients
        displayrecipients = createdRecipients.replace(',', ', ')
        cc = createdCC
        displaycc = createdCC.replace(',', ', ')
        bcc = createdBCC
        displaybcc = createdBCC.replace(',', ', ')
        subject = createdSubject
        message = createdMessage
        displaymessage = urllib.parse.unquote_plus(createdMessage).replace('\n', '<br>')
        displaysubject = urllib.parse.unquote_plus(createdSubject)
        purpose = urllib.parse.unquote_plus(createdPurpose).replace('\n', '<br>')
        baseurl = request.base_url.replace('/created','')

        url = baseurl + url_for('renderEmail', purpose=purpose, recipients=recipients, cc=cc, bcc=bcc, subject=subject, message=message ).replace('/oneclick','')
        openurl = baseurl + url_for('openEmail', purpose=purpose, recipients=recipients, cc=cc, bcc=bcc, subject=subject, message=message ).replace('/oneclick','')

        if utf8len(openurl) > 4950:
            return render_template('error.html', error="Unfortunately, your email is too long for this service. Try delivering your message via other easy web publishing services like Google Docs.")

        return render_template('success.html', openurl=openurl, url=url, purpose=purpose, displayrecipients=displayrecipients, displaycc=displaycc, displaybcc=displaybcc, displaysubject=displaysubject, displaymessage=displaymessage, recipients=recipients, cc=cc, bcc=bcc, subject=subject, message=message)
    if request.method == "GET":
        return redirect(url_for('home'))

@app.route("/success", methods=["GET"])
def renderSuccess():
    recipients = request.args.get('recipients', default = "")
    displayrecipients = request.args.get('recipients', default = "").replace(',', ', ')
    cc = request.args.get('cc', default = "")
    displaycc = request.args.get('cc', default = "").replace(',', ', ')
    bcc = request.args.get('bcc', default = "")
    displaybcc = request.args.get('bcc', default = "").replace(',', ', ')
    subject = request.args.get('subject', default = "")
    message = request.args.get('message', default = "")
    displaymessage = urllib.parse.unquote_plus(request.args.get('message', default = "")).replace('\n', '<br>')
    displaysubject = urllib.parse.unquote_plus(request.args.get('subject', default = ""))
    purpose = urllib.parse.unquote_plus(request.args.get('purpose', default = "")).replace('\n', '<br>')
    url = request.args.get('baseurl', default = "").rstrip('/') + url_for('renderEmail', purpose=purpose, recipients=recipients, cc=cc, bcc=bcc, subject=subject, message=message ).replace('/oneclick','')
    openurl = request.args.get('baseurl', default = "").rstrip('/') + url_for('openEmail', purpose=purpose, recipients=recipients, cc=cc, bcc=bcc, subject=subject, message=message ).replace('/oneclick','')

    try:
        url = shortener.shorten_urls([url])[0]
    except:
        print("Error")

    return render_template('success.html', openurl=openurl, url=url, purpose=purpose, displayrecipients=displayrecipients, displaycc=displaycc, displaybcc=displaybcc, displaysubject=displaysubject, displaymessage=displaymessage, recipients=recipients, cc=cc, bcc=bcc, subject=subject, message=message)


@app.route("/email", methods=["GET"])
def renderEmail():
    recipients = request.args.get('recipients', default = "")
    displayrecipients = request.args.get('recipients', default = "").replace(',', ', ')
    cc = request.args.get('cc', default = "")
    displaycc = request.args.get('cc', default = "").replace(',', ', ')
    bcc = request.args.get('bcc', default = "")
    displaybcc = request.args.get('bcc', default = "").replace(',', ', ')
    subject = request.args.get('subject', default = "")
    message = request.args.get('message', default = "")
    displaysubject = urllib.parse.unquote_plus(request.args.get('subject', default = ""))
    displaymessage = urllib.parse.unquote_plus(request.args.get('message', default = "")).replace('\n', '<br>')
    purpose = urllib.parse.unquote_plus(request.args.get('purpose', default = ""))

    return render_template('email.html', purpose=purpose, displayrecipients=displayrecipients, displaycc=displaycc, displaybcc=displaybcc, displaysubject=displaysubject, displaymessage=displaymessage, recipients=recipients, cc=cc, bcc=bcc, subject=subject, message=message)


@app.route("/openemail", methods=["GET"])
def openEmail():
    recipients = request.args.get('recipients', default = "")
    cc = request.args.get('cc', default = "")
    bcc = request.args.get('bcc', default = "")
    subject = request.args.get('subject', default = "")
    message = request.args.get('message', default = "")

    return redirect('mailto:'+recipients+'?cc='+cc+'&bcc='+bcc+'&subject='+subject+'&body='+message)

@app.route("/about", methods=["GET"])
def displayAbout():
    print("about")
    return render_template('about.html')

@app.errorhandler(404)
def pageNotFound(e):
    # your processing here
    return redirect(url_for('home'))

@app.errorhandler(504)
def tooLong(e):
    # your processing here
    return redirect(url_for('home'))
