import os
import hashlib

def hashIt(fileData):
    hash_obj = hashlib.sha1(fileData.encode())
    hex_dig = hash_obj.hexdigest()
    return hex_dig

def downlad(user=''):
    fnames = os.listdir('static/upload')
    if user:
        for fname in fnames:
            print(fname)
            to = fname[(fname.find('to:') + 4):len(fname)]
            sender = fname[(fname.find('from: ') + 6):(fname.find('to: ') - 1)]
            if to == user:
                print('match!')
                filepath = ('href="../static/upload/'+fname+'"').strip()
                newHTML ="<tr><td>"+sender+'</td><td><a '+filepath+' download="'+fname+'"><strong>Download</strong></a></td><td>'+fname[0:fname.find('from:')]+'</td></tr>'
                with open('downloadtable.txt', 'w') as f:
                    f.write(newHTML)
            else:
                donwloadInfo = ''
    else:
        downladInfo = ''
    with open('downloadtable.txt', 'r') as f:
        tableData = f.read()
    with open('templates/download.html', 'w') as f:
        f.write(
"""{% extends "navbar.html" %}
{% block content %}
<title>MedRec</title>
<section class="hero is-primary is-bold is-small">
  <div class="hero-body">
    <div class="container has-text-centered">
      <div id="settings" class="legbox">
          <h1 class="title">Availible Downloads</h1>
            <table class="table">
  <thead>
    <tr>
      <th><abbr title="From">From</abbr></th>
      <th><abbr title="File">File</abbr></th>
      <th><abbr title="Date">Date</abbr></th>
    </tr>
  </thead>
  <tfoot>
    <tr>
      <th><abbr title="From">From</abbr></th>
      <th><abbr title="File">File</abbr></th>
      <th><abbr title="Date">Date</abbr></th>
    </tr>
  </tfoot>
  <tbody>"""
+tableData+
"""</tbody>
</table>
          <br></tr>
          <br>
          <br>
          <i><a id="feedback" class="feedback"></a></i>
      </div>
    </div>
  </div>
</section>
{% endblock %}""")

downlad('a')