import socket
import subprocess
from urllib.parse import urlparse

from lib.utils.container import Services
from .. import AttackPlugin


class Crime(AttackPlugin):
    def process(self, start_url, crawled_urls):
        output = Services.get('output')

        output.info('Scanning crime (SPDY) vuln...')
        ip = ''
        port = '443'
        try:
            ip += socket.gethostbyname(urlparse(start_url).hostname)
            socket.inet_aton(ip)
            r = subprocess.Popen(
                ['openssl', 's_client', '-connect', ip + ":" + port, "-nextprotoneg", "NULL"],
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE).communicate()[0]
            if 'Protocols advertised by server' not in str(r):
                output.finding('That site is vulnerable to CRIME (SPDY), CVE-2012-4929.')
        except Exception as e:
            output.error("Error occured\nAborting this attack...\n")
            return
