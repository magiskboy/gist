import time
import math
from parser import Parser


class Protocol:
    def on_method(self, method):
        ...

    def on_path(self, path):
        ...

    def on_http_version(self, version):
        ...

    def on_header(self, name, value):
        ...

    def on_headers_completed(self):
        ...

    def on_body(self, body):
        ...


if __name__ == '__main__':
    data = (
        "GET /wp-content/uploads/2010/03/hello-kitty-darth-vader-pink.jpg HTTP/1.1\r\n"
        + "Host: www.kittyhell.com\r\n"
        + "User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; ja-JP-mac; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 Pathtraq/0.9\r\n"
        + "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        + "Accept-Language: ja,en-us;q=0.7,en;q=0.3\r\n"
        + "Accept-Encoding: gzip,deflate\r\n"
        + "Accept-Charset: Shift_JIS,utf-8;q=0.7,*;q=0.7\r\n"
        + "Keep-Alive: 115\r\n"
        + "Connection: keep-alive\r\n"
        + "Cookie: wp_ozh_wsa_visits=2; wp_ozh_wsa_visit_lasttime=xxxxxxxxxx; __utma=xxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.xxxxxxxxxx.x; __utmz=xxxxxxxxx.xxxxxxxxxx.x.x.utmccn=(referral)|utmcsr=reader.livedoor.com|utmcct=/reader/|utmcmd=referral\r\n\r\n"
    )

    data = data.encode("utf-8")
    buf_size = 65536
    n = 1_000_000

    start = time.perf_counter()

    for _ in range(n):
        protocol = Protocol()
        parser = Parser(protocol)
        parser.feed_data(data) 

    end = time.perf_counter()
    n_req = math.floor(n / (end-start))
    print(f"{n_req} req/s")
