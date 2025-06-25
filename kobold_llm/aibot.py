import json
import time
import argparse
import sys
import os
import http.client
import base64

class AIBot:
    def __init__(self, server='localhost', api_port=5001):
        self.server = server
        self.api_port = api_port
        self.headers = {"Content-Type": "application/json"}
        self.settings = {'max_length': 384}
        self.text = ''
        self.files = []

    def log(self, msg):
        print(f"[{self.api_port}] {msg}", file=sys.stderr, flush=True)

    def connect(self):
        try:
            conn = http.client.HTTPConnection(f"{self.server}:{self.api_port}")
            return conn
        except Exception as e:
            self.log(f"connection failed: {e}")
            return None

    def get_model_info(self, conn):
        try:
            conn.request("GET", '/api/v1/model')
            resp = json.loads(conn.getresponse().read().decode('utf-8'))
            return resp.get('result', 'unknown')
        except:
            return 'unknown'

    def is_ready(self, conn):
        try:
            conn.request("GET", '/api/extra/perf')
            resp = json.loads(conn.getresponse().read().decode('utf-8'))
            return resp.get('idle', False)
        except:
            return False

    def encode_image(self, path):
        try:
            with open(path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            self.log(f"image encode failed: {e}")
            return ''

    def stream_response(self, conn):
        payload = dict(self.settings)
        payload['prompt'] = self.text

        if self.files:
            payload['images'] = [self.encode_image(f) for f in self.files if self.encode_image(f)]

        try:
            conn.request('POST', '/api/extra/generate/stream', json.dumps(payload), self.headers)
            response = conn.getresponse()
        except Exception as e:
            self.log(f"request failed: {e}")
            return 0

        if response.status != 200:
            self.log(f"bad response: {response.status}")
            return 0

        tokens = 0
        done = False

        while not done:
            line = response.readline()
            if not line:
                break

            line = line.decode('utf-8').strip()
            if not line:
                continue

            if ':' in line:
                event, data = line.split(':', 1)
                if '{' in data:
                    try:
                        parsed = json.loads(data)
                        token = parsed.get('token', '')
                        if token:
                            print(token, end='', flush=True)
                            self.text += token
                            tokens += 1

                        reason = parsed.get('finish_reason')
                        if reason in ['stop', 'length']:
                            done = True
                    except:
                        continue

        return tokens

    def run_session(self, max_turns=1):
        conn = self.connect()
        if not conn:
            return 1

        model = self.get_model_info(conn)
        self.log(f"connected to {model}")

        for turn in range(max_turns):
            while not self.is_ready(conn):
                time.sleep(0.1)

            start = time.time()
            tokens = self.stream_response(conn)
            elapsed = time.time() - start

            if tokens > 0:
                self.log(f"turn {turn+1}: {tokens} tokens in {elapsed:.2f}s")
            else:
                self.log(f"turn {turn+1}: failed")
                break

        return 0

def get_stdin():
    if sys.stdin.isatty():
        return ''
    return sys.stdin.read()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('prompt', nargs='*', help="text to send")
    parser.add_argument('-s', '--server', default='localhost', help="server address")
    parser.add_argument('-p', '--port', type=int, default=5001, help="server port")
    parser.add_argument('-l', '--loops', type=int, default=1, help="number of turns")
    parser.add_argument('-i', '--images', help="image files (newline separated)")
    parser.add_argument('-n', '--new', action='store_true', help="create new context")
    args = parser.parse_args()

    bot = AIBot(args.server, args.port)

    stdin_text = get_stdin()
    prompt_text = ' '.join(args.prompt)
    bot.text = stdin_text + prompt_text

    if args.images:
        bot.files = args.images.splitlines()

    if not bot.text.strip():
        bot.text = "Hello"

    return bot.run_session(args.loops)

if __name__ == '__main__':
    sys.exit(main())