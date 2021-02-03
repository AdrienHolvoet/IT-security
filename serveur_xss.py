#!/usr/bin/env python3

import mysql.connector
import cherrypy
import config
import html

class VulnerableApp(object):
    def __init__(self):
        self.conn = mysql.connector.connect(host=config.DB_HOST, user=config.DB_USER, database=config.DB_NAME, password=config.DB_PASS)

    @cherrypy.expose
    def index(self, **post):
        cursor = self.conn.cursor(prepared=True)
        if cherrypy.request.method == "POST":
            requete = "INSERT INTO chaines (txt,who) VALUES(%s, %s)"
            values = (html.escape(post["chaine"]), cherrypy.request.remote.ip)
            print("REQUETE: [" + requete + "]")
            cursor.execute(requete, values)
            self.conn.commit()

        chaines = []
        cursor.execute("SELECT txt,who FROM chaines");
        for row in cursor.fetchall():
            chaines.append(row[0] + " envoye par: " + row[1])

        cursor.close()
        return '''
<html>
<head>
<title>Application Python Vulnerable</title>
</head>
<body>
<p>
Bonjour, je suis une application vulnerable qui sert a inserer des chaines dans une base de données MySQL!
</p>

<p>
Liste des chaines actuellement insérées:
<ul>
'''+"\n".join(["<li>" + s + "</li>" for s in chaines])+'''
</ul>
</p>

<p> Inserer une chaine:

<form method="post" onsubmit="return validate()">
<input type="text" name="chaine" id="chaine" value="" />
<br />
<input type="submit" name="submit" value="OK" />
</form>

<script>
function validate() {
    var regex = /^[a-zA-Z0-9]+$/;
    var chaine = document.getElementById('chaine').value;
    console.log(regex.test(chaine));
    if (!regex.test(chaine)) {
        alert("Veuillez entrer une chaine avec uniquement des lettres et des chiffres");
        return false;
    }
    return true;
}
</script>

</p>
</body>
</html>
'''


cherrypy.quickstart(VulnerableApp())
