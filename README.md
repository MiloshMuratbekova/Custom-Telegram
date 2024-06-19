INSTALATION

sudo apt install weasyprint
/var/ossec/framework/python/bin/pip3 install weasyprint

cd /var/ossec/integrations

git clone project and unpack

cp ./slack ./custom-telegram

/var/ossec/framework/python/bin/pip3 install -r requrements.txt

chmod 530 custom-telegram
chmod 530 custom-telegram.py
chmod 530 temp
chmod 530 temp/report.html
chown root:wazuh custom-telegram
chown root:wazuh custom-telegram.py
chown root:wazuh temp
chown root:wazuh temp/report.html

systemctl restart wazuh-manager
