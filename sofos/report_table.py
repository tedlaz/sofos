"""
Create an html report
"""

html_template = """
<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<style>
table, th, td {{
    border: 1px solid black;
    border-collapse: collapse;
}}
th, td {{
    padding: 3px;
}}
@page {{
  size: A4 landscape;
  @top-left {{
    content: "Hamlet";
  }}
  @top-right {{
    content: "Page " counter(page);
  }}
}}
@page :left {{
margin-left: 3cm;
margin-right: 4cm;
}}

@page :right {{
margin-left: 4cm;
margin-right: 3cm;
}}
</style>
</head>
<body style=" font-size:8pt; font-weight:400; font-style:normal; text-decoration:none;">
</body>
<table border="1" align="center" width="100%" cellspacing="0" cellpadding="4">
  <tbody>
    {}
  </tbody>
</table>
</html>
"""


ttr1 = "    <tr>%s</tr>\n"
ttr2 = "    <tr>%s</tr>"


def render_html_table(data):
    labels = ttr1 % ''.join(['<th>%s</th>' % col for col in data['labels']])
    lines = []
    for lin in data['lines']:
        lines.append(ttr2 % ''.join(['<td>%s</td>' % col for col in lin]))
    html_lines = labels + '\n'.join(lines)
    return (html_template.format(html_lines))


if __name__ == '__main__':
    head = ['Επώνυμο', 'Ονομα', 'Πατρώνυμο']
    vals = [['Λάζαρος', 'Θεόδωρος', 'Κωνσταντίνος'],
            ['Μαραβέλιας', 'Σπύρος', 'Νικόλαος']] * 100
    data = {'labels': head, 'lines': vals}
    print(render_html_table(data))
