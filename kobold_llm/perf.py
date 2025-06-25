import requests


port = 5001
url = f'http://localhost:{port}/api/extra/perf'

# GET
response = requests.get(url, headers={"accept": "application/json"})
if response.status_code == 200:
    data = response.json()

    # values selection
    input_tokens = data.get("last_input_count", 0)
    output_tokens = data.get("last_token_count", 0)
    process_time = data.get("last_process_time", 0)
    generation_speed = data.get("last_eval_speed", 0)

    # calculate speeds
    processing_speed = (input_tokens / process_time) if process_time else 0
    total_tokens = input_tokens + output_tokens
    total_time = data.get("last_process", 0)  # Full time for entire inference cycle
    total_tps = (total_tokens / total_time) if total_time else 0

    print(f"Processing Speed: {processing_speed:.2f} tokens/sec")
    print(f"Generation Speed: {generation_speed:.2f} tokens/sec")
    print(f"Total Tokens per Second: {total_tps:.2f} tokens/sec")

else:
    print(f"Request failed with status code {response.status_code}")
