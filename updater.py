import os
import hashlib

def hashIt(fileData):
    hash_obj = hashlib.sha1(fileData.encode())
    hex_dig = hash_obj.hexdigest()
    return hex_dig

def update():
    fnames = os.listdir('static/upload')
    fnames.sort()
    for fname in enumerate(fnames):
        with open('done.txt', 'r+') as f:
            doneNames = f.read().splitlines()
        if fname[1] in doneNames:
            print('Pre')
        else:
            sender = fname[1][(fname[1].find('from: ') + 6):(fname[1].find('to: ') - 1)]
            to = fname[1][(fname[1].find('to:') + 4):len(fname[1])]
            if len(doneNames) > 0:
                previousHash = hashIt(fnames[(fname[0]-1)])
            else:
                previousHash = '0'
            currentHash = hashIt(fname[1])
            newHTML = "<tr><td>"+sender+"</td><td>"+to+"</td><td>"+currentHash+"</td><td>"+previousHash+"</td></tr>"
            with open('table.txt', 'a+') as f:
                f.write(newHTML)
            with open('done.txt', 'a+') as f:
                f.write(fname[1] + '\n')
    with open('table.txt', 'r+') as f:
        tableData = f.read()
        print(tableData)
    with open('templates/home.html', 'w') as f:
        f.write(
"""{% extends "navbar.html" %}
{% block content %}
<title>MedRec</title>
<section class="hero is-primary is-bold is-small">
  <div class="hero-body">
    <div class="container has-text-centered">
      <div id="settings" class="legbox">
          <h1 class="title">Public Transactions</h1>
            <table class="table">
  <thead>
    <tr>
      <th><abbr title="From">From</abbr></th>
      <th><abbr title="To">To</abbr></th>
      <th><abbr title="Hash">Hash</abbr></th>
      <th><abbr title="PreviousHash">Previous Hash</abbr></th>
    </tr>
  </thead>
  <tfoot>
    <tr>
      <th><abbr title="From">From</abbr></th>
      <th><abbr title="To">To</abbr></th>
      <th><abbr title="Hash">Hash</abbr></th>
      <th><abbr title="PreviousHash">Previous Hash</abbr></th>
    </tr>
  </tfoot>
  <tbody>""" +tableData+
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

update()