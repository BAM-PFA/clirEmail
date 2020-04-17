# CLIR project CSV to form emails (via G Drive API)

This is a script to take a CSV of filmmakers who we need to contact for permissions to post audio online thanks to a CLIR audio digitization [project](https://github.com/BAM-PFA/audio-database-merge).

What I hope it demonstrates is how to take CSV data and generate a batch of Google Docs based on the input data.

## Background 

Staring in the 1970s, PFA has been recording guest filmmakers who speak at the theater in conjuction with film programs. In 2018 we received a grant to digitize the first \~10 years (\~1976-1986) and make most of them available online.

Some of the audiotapes we have in our collection already have signed releases that give sufficient permission for us to post digitized audio online. A significant chunk, though, will require new permissions, since of course the releases were signed before streaming audio was a glint in Steve Jobs's eye. We have a database describing these recordings and I used it to create a CSV for parsing which tapes need additional permissions.

For this task I wanted to take the CSV--which contains columns for NAME, DECEASED, FILM TITLES, RECORDING DATE, and DB RECORDING ID--and use it to create a form letter/email for each individual speaker. The [Google Drive API](https://developers.google.com/drive) seemed like a good way to accomplish this, and for the moment, this script just creates Docs with the text of the email. 

CSV column headings are expected to be in this order:

|name|deceased?|film titles|permissions|record numbers|dates|
|-|-|-|-|-|-|

## Usage

Once it's all set up, just run `python3 clirEmail.py` from the project directory. It should start populating the Drive folder you specify with new Docs based on the text you have fed the script.

## Setup

Ha. Ok.

First you need a CSV with the data you want to parse. In my case, it includes the columns listed above. Here's a sample:

|name|deceased?|film titles|permissions|record numbers|dates|
|-|-|-|-|-|-|
|Anthony Harvey|y|"['LOLITA', 'The Glass Menagerie', 'They Might Be Giants', 'Dr. Strangelove: Or How I Learned to Stop Worrying and Love the Bomb', 'The Lion in Winter', 'Dutchman']"|['no form given']|"['03551', '03552', '03555']","['9/28/1977', '9/21/1977', '9/14/1977']"|

This is super-specifically hard coded into the `Email` class in `letterContent.py`, which builds the Doc text paragraph by paragraph. This approach allows each doc to be written in reverse, which the Google API documentation recommends (trying to write top to bottom means that you would need to calculate the `insert` index of every paragraph you want to add to all the stuff that came before; just inserting each paragraph at index 0 is way easier!). 

If you are intending to create your own Doc, you'll need to replace this text with whatever you are working with.

Next, obviously you need to set up a Drive API account/project. The Google Docs API [quickstart](https://developers.google.com/docs/api/quickstart/python) is the only really useful part of their documentation. The rest of it is pretty inconsistent/incoherent. One **important** thing to keep in mind is that there are different APIs for each Google product (Drive, Docs, Sheets, Ads, etc.) and they're all slightly different and use different parts of the Python API client. You should also check out the [Python API client setup](https://github.com/googleapis/google-api-python-client/blob/master/docs/start.md) for more details.

Basically you:

* install the Python client (`pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`)
* make a Google API [project](https://console.developers.google.com/apis/dashboard)
* set up authentication (see the links above for details on setting up OAuth)
  * create a credentials.json file based on the OAuth credentials (it's pretty straightforward, read the instructions mentioned above)
* enable the Docs (and Drive) APIs for your project
* run it once (the auth token setup as is needs to open in a browser, do it once and it will save `token.pickle` to the secrets dir and you shouldn't have to sign in again)
* in `other.py` define a folder ID for the Drive folder where you want the batch of Docs to wind up,

That... should be it. I would recommend looking around at the different Google API documentation pages to get a sense of how the APIs are structured, what methods are defined, etc., though as I mentioned they are not all super clear.



