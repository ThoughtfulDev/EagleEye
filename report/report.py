from weasyprint import HTML
import os

def makeReport(name, links, preds, instnames, age):
    #sort
    links = sorted(links)
    preds = sorted(preds)
    instnames = sorted(instnames)

    name = name.strip()
    name = name.replace('%20', '-')
    with open('./report/template.html', 'r') as f:
        template_data = f.read()
    template_data = template_data.replace('{{INPUT_NAME}}', name)
    template_data = template_data.replace('{{ES_AGE}}', str(age))
    links_str = ""
    for l in links:
        links_str += "<li>"
        links_str += '<a href="{0}">{0}</a>'.format(l)
        links_str += "</li>"
    template_data = template_data.replace('{{SOCIAL_URLS}}', links_str)
    preds_str = ""
    for p in preds:
        preds_str += "<li>"
        preds_str += p
        preds_str += "</li>"
    template_data = template_data.replace('{{GOOGLE_PREDS}}', preds_str)
    insta_str = ""
    for i in instnames:
        insta_str += "<li>"
        insta_str += '<a href="https://www.instagram.com/{0}">https://instagram.com/{0}</a>'.format(i)
        insta_str += "</li>"
    template_data = template_data.replace('{{INSTA_PROFILES}}', insta_str)
    with open('tmp.html', 'w') as t:
        t.write(template_data)
    doc = HTML('tmp.html')
    doc.write_pdf('{0}_Report.pdf'.format(name))
    os.remove('tmp.html')

