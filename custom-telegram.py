#!/var/ossec/framework/python/bin/python3

import sys
import json
import traceback

try:
    import requests
    from weasyprint import HTML
    from jinja2 import Environment, FileSystemLoader
except ImportError as e:
    with open('/var/ossec/logs/integrations.log', 'a') as f:
        f.write(f"Error: {traceback.format_exc()}\n")

try:
    env = Environment(loader=FileSystemLoader("/var/ossec/integrations/temp"))
except Exception as e:
    with open('/var/ossec/logs/integrations.log', 'a') as f:
        f.write(f"Error: {traceback.format_exc()}\n")


def generate_pdf(alert):
    template = env.get_template("report.html")
    try:
        template = HTML(string=template.render(data=alert))
    except Exception:
        with open('/var/ossec/logs/integrations.log', 'a') as f:
            f.write(f'\ntemplate error')
        template = HTML(string=template.render(data=alert['data']))
    template.write_pdf("/var/ossec/integrations/temp/report.pdf")
    return "/var/ossec/integrations/temp/report.pdf"


def send_telegram_message(hook_url, chat_id, pdf_path, alert):
    caption = f"New Incident detected!\n{alert['rule']['description']}\nLevel {alert['rule']['level']}.\nAgent: {alert['agent']['name']} {alert['agent']['id']}"
    payload = {
        'chat_id': chat_id,
        'caption': caption,
        'parse_mode': 'HTML'
    }
    files = {
        'document': open(pdf_path, 'rb')
    }
    r = requests.post(hook_url, data=payload, files=files, stream=True)
    return r

if __name__ == "__main__":
    CHAT_ID = '1307538868'

    try:
        alert_file = sys.argv[1]
        hook_url = sys.argv[3]
        with open(alert_file, 'r') as f:
            try:
                alert_json = json.loads(f.read())
            except Exception:
                with open('/var/ossec/logs/integrations.log', 'a') as f:
                    f.write('\nalertjson error')
                alert_json = json.loads(f.readlines()[-1])

        with open('/var/ossec/logs/integrations.log', 'a') as f:
            f.write(f'\n{str(alert_json)}')

        pdf_path = generate_pdf(alert_json)
        response = send_telegram_message(hook_url, CHAT_ID, pdf_path, alert_json)
        if not response.ok:
            with open('/var/ossec/logs/integrations.log', 'a') as f:
                f.write(f"Error response: {response.text}\n")
    except Exception as e:
        with open('/var/ossec/logs/integrations.log', 'a') as f:
            f.write(f"Error: {traceback.format_exc()}\n")

    sys.exit(1)
