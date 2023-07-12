## Simple HTTP client in Javascript

```javascript
const https = require('https');

class HTTPResponse {
  constructor(response) {
    this._response = response;
    this.headers = response.headers;
    this.statusCode = response.statusCode;
  }

  async data() {
      return new Promise((resolve, reject) => {
        let data = Buffer.from('');
        this._response
          .on('data', chunk => data = Buffer.concat([data, chunk]))
          .on('error', error => reject(error))
          .on('end', () => resolve(data));
      })
  }

  async text() {
    const buffer = await this.data();
    return buffer.toString();
  }

  async json() {
    const isJson = this.headers['content-type'] === 'application/json';
    if (isJson) {
      return JSON.parse(await this.text());
    }
  }
}

class HTTPClient {
  async request(url, method, params, body, options) {
    return new Promise((resolve, reject) => {
      const URLObject = new URL(url);
      const request = https.request({
        hostname: URLObject.hostname,
        path: URLObject.pathname,
        method,
        body,
        ...options
      }, response => {
        const result = new HTTPResponse(response);
        if (response.statusCode >= 400) {
          reject(result);
        }
        else {
          resolve(result);
        }
      });

      request.on('error', error => reject(error));
      request.end();
    });
  }

  async get(url, params, options) {
    return this.request(url, "GET", params, undefined, options);
  }

  async post(url, params, body, options) {
    return this.request(url, "POST", params, body, options);
  }

  async put(url, params, body, options) {
    return this.request(url, "PUT", params, body, options);
  }

  async patch(url, params, body, options) {
    return this.request(url, "PATCH", params, body, options);
  }

  async delete(url, params, body, options) {
    return this.request(url, "DELETE", params, body, options);
  }
}

async function main() {
  const c = new HTTPClient();
  const resp = await c.get('https://google.vn');
  const data = await resp.text();
  console.log(data);
}

main();
```
