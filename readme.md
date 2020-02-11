# CLIR project form email (via G Drive API)

This is a script to take a CSV of filmmakers who we need to contact for permissions to post audio online thanks to a CLIR audio digitization [project](https://github.com/BAM-PFA/audio-database-merge).

For this iteration I wanted to take the CSV--which contains columns for NAME, DECEASED, FILM TITLES, RECORDING DATE (and db recording ID)--and use it to create a form letter/email for each individual. The [Google Drive API](https://developers.google.com/drive) seemed like a good way to accomplish this, and for the moment, this script just creates Docs with the text of the email. 

