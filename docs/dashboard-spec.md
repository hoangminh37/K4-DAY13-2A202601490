# Yêu cầu dashboard

Contract có thể kiểm tra bằng máy nằm tại `config/dashboard.yaml`. Hướng dẫn dựng và kiểm tra runtime nằm tại [DASHBOARD_SETUP.md](DASHBOARD_SETUP.md).

Dashboard chính bao gồm 6 nhóm panel (Time range mặc định 60 phút, refresh rate 30 giây):

1. **Latency**: Hiển thị độ trễ P50, P95, P99 (ms) của API.
   - Nguồn: `latency_ms` từ `response_sent`.
   - Threshold: P95 <= 3000ms.
2. **Traffic**: Đếm tổng số request và tốc độ Request Per Minute (RPM).
   - Nguồn: count event `request_received`.
   - Threshold: RPM >= 1.
3. **Error**: Tỷ lệ lỗi (%) và bảng breakdown nguyên nhân.
   - Nguồn: tỷ lệ `request_failed` so với `request_received`.
   - Threshold: error_rate_pct <= 2%.
4. **Cost**: Chi phí LLM theo thời gian (USD).
   - Nguồn: tổng trường `cost_usd` từ `response_sent`.
   - Threshold: total cost <= 2.5 USD.
5. **Tokens**: Tổng token input và output.
   - Nguồn: tổng `tokens_in` và `tokens_out`.
   - Threshold: tổng tokens <= 50000.
6. **Quality**: Điểm chất lượng trung bình của hệ thống.
   - Nguồn: trung bình `quality_score`.
   - Threshold: avg score >= 0.75.

Kiểm tra contract trước khi chụp evidence:

```bash
python scripts/validate_dashboard.py
```
