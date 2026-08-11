# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: Cá nhân (Lương Hoàng Minh)
- Repository URL: https://github.com/hoangminh37/K4-DAY13-2A202601490
- Commit SHA cuối: d7f6e23
- Thành viên và vai trò: Lương Hoàng Minh

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100
- Tổng số traces: Đã tạo và ghi nhận đầy đủ (≥ 10 traces) trên Langfuse.
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: `docs/dashboard-spec.md` và `config/dashboard.yaml`

## 3. Logging và tracing

- Evidence correlation ID: Đã chụp màn hình và lưu trong `submission/evidence/`
- Evidence PII redaction: Đã chụp màn hình và lưu trong `submission/evidence/`
- Evidence trace waterfall: Đã chụp màn hình và lưu trong `submission/evidence/`
- Giải thích một span đáng chú ý: Nhờ decorator `@observe(as_type="span")`, bên dưới span cha `run` giờ đây có 2 sub-span là `retrieve` (đại diện cho RAG) chạy trước mất khoảng 50ms, và `generate` (đại diện cho LLM) mất khoảng 150ms. Việc tách biệt này giúp kỹ sư dễ dàng xác định chính xác nút thắt cổ chai nằm ở RAG (DB chậm) hay LLM (API chậm).

## 4. Prompt versioning

- Prompt name:
- Version/label baseline:
- Version/label candidate:
- Trace ID của mỗi version:
- Bằng chứng đổi label hoặc rollback:

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: Hợp lệ 6/6 panel
- Evidence dashboard: Đã lưu spec và config trong `docs/dashboard-spec.md` và `config/dashboard.yaml`
- SLO đã chọn và lý do: 
  + Latency P95 < 3000ms: Đảm bảo chatbot phản hồi nhanh, giữ chân người dùng.
  + Error rate < 2%: Đảm bảo hệ thống ổn định cao.
  + Cost < 2.5 USD/ngày: Ngăn chặn các đợt gọi API lãng phí hoặc bị tấn công làm vượt ngân sách.
  + Quality >= 0.75: Giữ chất lượng câu trả lời luôn ở mức tốt.
- Alert rules và runbook: Đã cấu hình 3 Symptom-based Alerts (`high_latency_p95`, `elevated_error_rate`, `cost_budget_exceeded`) ở file `config/alert_rules.yaml`. Runbook tương ứng ghi rõ cách xử lý tạm thời (mitigation) và các bước kiểm tra (investigation) đã được viết tại `docs/alerts.md`.

## 6. Điều tra challenge

- Challenge ID: day13-k4-observability-v1
- Triệu chứng từ metrics: Điểm p95 latency tăng vọt lên ~3635ms, vượt quá ngưỡng SLO cho phép (< 3000ms), trong khi đó traffic và error rate vẫn giữ ở mức bình thường.
- Trace ID liên quan: Bất kỳ Trace nào trong đợt tải có kèm tag `monitoring` (ví dụ chứa Correlation ID: `req-d94fcae7`).
- Log line/correlation ID liên quan: Dùng Correlation ID `req-d94fcae7` để lọc file `data/logs.jsonl`. Kết quả cho thấy thời gian từ lúc `request_received` đến lúc `response_sent` kéo dài hơn 3.5 giây.
- Root cause: Bằng chứng từ biểu đồ Trace Waterfall trên Langfuse chỉ ra rõ ràng sub-span `retrieve` (đại diện cho bước lấy context từ RAG / Vector DB) đã tiêu tốn thêm tận 2.5 giây so với bình thường. Nguyên nhân gốc nằm ở hệ thống Retrieval (do Vector DB chậm hoặc timeout).
- Fix action: Tạm thời vô hiệu hóa tính năng RAG hoặc kích hoạt bản RAG cache/dự phòng để khôi phục tốc độ dịch vụ ngay lập tức. Sau đó scale tài nguyên của Vector Store.
- Preventive measure: Cần thiết lập Alert Rule riêng biệt cho độ trễ của RAG (ví dụ: retrieve span > 1s). Bổ sung timeout cứng vào code RAG để không làm treo toàn bộ API (ví dụ nếu quá 500ms không lấy được docs thì trả về list rỗng thay vì chờ đợi).

## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| | | | |
