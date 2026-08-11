import json
from pathlib import Path

LOG_PATH = Path("data/logs.jsonl")

def detect_anomalies():
    print(f"Bắt đầu quét {LOG_PATH} để tìm bất thường (Anomalies)...")
    if not LOG_PATH.exists():
        print("Không tìm thấy file log!")
        return

    anomalies_found = 0
    with LOG_PATH.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                
                # Rule 1: High Latency (> 3000ms)
                if data.get("latency_ms", 0) > 3000:
                    anomalies_found += 1
                    print(f"[ALERT - {data.get('ts')}] High Latency ({data['latency_ms']}ms) tại request: {data.get('correlation_id', 'unknown')}")
                
                # Rule 2: Errors
                if data.get("event") == "request_failed":
                    anomalies_found += 1
                    print(f"[ALERT - {data.get('ts')}] Error ({data.get('error_type')}) tại request: {data.get('correlation_id', 'unknown')}")

            except json.JSONDecodeError:
                pass
                
    if anomalies_found == 0:
        print("Hệ thống hoạt động ổn định, không phát hiện sự cố!")
    else:
        print(f"Phát hiện tổng cộng {anomalies_found} sự cố từ hệ thống log.")

if __name__ == "__main__":
    detect_anomalies()
