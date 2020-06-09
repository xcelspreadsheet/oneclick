
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import redirect
from flask import render_template, redirect, url_for
from flask import request
import urllib

app = Flask(__name__)

#app.route('/')
#def hello_world():
#    return redirect("mailto:governor@governor.ri.gov,Mayor@providenceri.gov,sselleck@providenceri.gov,Ward2@providenceri.gov,Ward5@providenceri.gov,Ward7@providenceri.gov,Ward8@providenceri.gov,Ward9@providenceri.gov?subject=Defund%20Providence%20Police&body=Hello%2C%0D%0A%0D%0AMy%20name%20is%20%5B%5BNAME%5D%5D%20and%20I%20am%20a%20resident%20of%20Providence.%20I%20am%20writing%20to%20demand%20that%20Governor%20Raimondo%2C%20Mayor%20Elorza%20and%20the%20members%20of%20the%20City%20Council%20do%20everything%20in%20their%20power%20to%20adopt%20a%20budget%20that%20redirects%20all%20funds%20from%20the%20Police%20Department%20and%20towards%20community%20wellbeing%2C%20mental%20health%20and%20the%20needs%20of%20its%20residents.%20It%20has%20become%20clear%20that%20police%20forces%20are%20ineffective%20at%20keeping%20local%20communities%20safe%2C%20and%20that%20they%20perpetuate%20the%20oppression%20of%20residents%20who%20are%20people%20of%20color%2C%20undocumented%2C%20mentally%20ill%2C%20disabled%2C%20and%20LGBTQ.%20While%20Providence%20has%20received%20a%20%24700%2C000%20grant%20to%20formulate%20a%20Behavioral%20Health%20Response%20Team%2C%20that%20amount%20is%20a%20mere%20drop%20in%20the%20bucket%20of%20the%20nearly%20%2490%20million%20budgeted%20for%20Police%20in%202021.%20The%20current%20budget%20proposal%20has%20allocated%20%24961%2C000%20on%20guns%20and%20ammunition%2C%20%241%2C461%2C620%20for%2050%20new%20police%20recruits%2C%20not%20to%20mention%20%2414.9%20million%20for%20uniforms%20and%20%22wearing%20apparel%2C%E2%80%9D%20presumably%20including%20more%20of%20the%20riot%20gear%20that%20is%20currently%20being%20used%20to%20suppress%20peaceful%20protests.%20Imagine%20how%20much%20those%20dollars%20could%20accomplish%20when%20used%20to%20fund%20low-income%20and%20public%20housing%2C%20education%2C%20resources%20for%20formerly%20incarcerated%20individuals%2C%20and%20public%20transportation%2C%20as%20Direct%20Action%20for%20Rights%20and%20Equality%20has%20demanded.%0D%0A%0D%0AProvidence%20may%20be%20a%20small%20city%2C%20but%20we%20have%20shown%20that%20we%20can%20make%20a%20huge%20impact%20on%20America%20at%20large.%20We%20desperately%20need%20to%20change%20our%20financial%20priorities%20and%20let%20our%20tax%20dollars%20go%20to%20communities%2C%20not%20cops.%0D%0A%0D%0AThank%20you%20for%20your%20time%2C%0D%0A%0D%0A%5B%5BNAME%5D%5D%0D%0A%5B%5BADDRESS%5D%5D%0D%0A%0D%0A%5B%5BEMAIL%20ADDRESS%5D%5D%0D%0A%5B%5BPHONE%20NUMBER%5D%5D")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print("POSTED")
        recipients = " ".join(request.form['recipients'].replace(',', ' ').split()).replace(" ", ',')
        cc = " ".join(request.form['cc'].replace(',', ' ').split()).replace(" ", ',')
        bcc = " ".join(request.form['bcc'].replace(',', ' ').split()).replace(" ", ',')
        subject = request.form['subject'].strip().replace('\n', ' ')
        message = urllib.parse.quote(request.form['message'])
        purpose = urllib.parse.quote(request.form['purpose'])
        return redirect(url_for('renderSuccess', purpose=purpose, baseurl=request.base_url, recipients=recipients, cc=cc, bcc=bcc, subject=subject, message=message ))


    if request.method == "GET":
        return render_template('index.html')

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
    displaysubject = urllib.parse.unquote_plus(request.args.get('subject', default = ""))
    displaymessage = urllib.parse.unquote_plus(request.args.get('message', default = "")).replace('\n', '<br>')
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

    return redirect('mailto:'+recipients+'?cc='+cc+'&bcc='+bcc+'&subject='+subject+'&body='+message)

@app.route("/about", methods=["GET"])
def displayAbout():
    print("about")
    return render_template('about.html')
