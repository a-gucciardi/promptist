import json
import urllib.request
import argparse
import sys

# TEST
# returns the number of tokens calculated for the string(s) provided as positional arguments. 
# argument -l gives full list of tokens instead.


class ApiClient:
    def __init__(self, server: str, api_port: str):
        self.server_addr = server
        self.api_port = api_port

    def query_tokens(self, text: str):
        endpoint = '/api/extra/tokencount'
        payload = json.dumps({"prompt": text}).encode('utf-8')
        full_url = f'http://{self.server_addr}:{self.api_port}{endpoint}'
        return self._make_request(full_url, payload)

    def extract_count(self, api_response) -> int:
        return api_response.get('value', 0)

    def extract_ids(self, api_response) -> list:
        return api_response.get('ids', [])

    def _make_request(self, target_url: str, request_data: str):
        try:
            req = urllib.request.Request(
               target_url,
               headers = {'Content-Type': 'application/json'},
               data = request_data
            )
            resp = urllib.request.urlopen(req)
        except Exception as e:
            print("request failed for", target_url, "with error", e)
            exit(-1)
        return json.loads(resp.read().decode('utf-8'))

def main():
    stdin_content = ''
    if not sys.stdin.isatty():
        buffer = ' '
        while buffer:
            buffer = sys.stdin.readline()
            stdin_content += buffer

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('text', nargs='*', help="text input for tokenization")
    arg_parser.add_argument('-l', action='store_true', help=f"output token list")
    arg_parser.add_argument('-s', type=str, default='localhost', help=f"API server address")
    arg_parser.add_argument('-p', type=int, default=5001, help=f"server port number")

    parsed_args = arg_parser.parse_args()
    client = ApiClient(parsed_args.s, parsed_args.p)

    final_input = stdin_content + ' '.join(parsed_args.text)
    result = client.query_tokens(final_input)

    if parsed_args.l:
        print(client.extract_ids(result))
    else:
        print(client.extract_count(result))

if __name__ == '__main__':
    main()