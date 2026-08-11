# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1: high_latency_p95

- Tên: high_latency_p95
- Severity: warning
- SLI/SLO liên quan: latency_p95_ms (SLO: < 3000ms)
- Điều kiện và thời gian duy trì: latency_p95 > 3000ms trong 5 phút
- Ảnh hưởng tới người dùng: Người dùng cảm thấy chatbot phản hồi chậm, làm giảm trải nghiệm và có thể gây timeout ở client.
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra Langfuse waterfall trace xem RAG hay LLM đang gây ra chậm.
  2. Kiểm tra tài nguyên hệ thống (CPU/Memory) xem API có đang bị thắt cổ chai không.
  3. Kiểm tra Traffic (QPS) xem có đợt spike (tăng vọt) đột biến không.
- Mitigation tạm thời: Scale up/out số lượng pod/worker của API hoặc tạm thời bật chế độ cache chặt chẽ hơn.
- Owner: on-call-engineer

## Alert 2: elevated_error_rate

- Tên: elevated_error_rate
- Severity: critical
- SLI/SLO liên quan: error_rate_pct (SLO: < 2%)
- Điều kiện và thời gian duy trì: error_rate_pct > 5% trong 3 phút
- Ảnh hưởng tới người dùng: Chatbot trả về lỗi liên tục, người dùng hoàn toàn không thể nhận được câu trả lời.
- Ba bước kiểm tra đầu tiên:
  1. Lọc lỗi (error breakdown) trên Dashboard xem loại lỗi nào (ví dụ: `tool_fail`) đang chiếm tỷ lệ cao nhất.
  2. Lấy Correlation ID của các request bị lỗi tra cứu trong file log trung tâm (data/logs.jsonl) để xem stack trace cụ thể.
  3. Kiểm tra trạng thái của các dịch vụ phụ thuộc bên thứ 3 (như LLM provider, DB).
- Mitigation tạm thời: Rollback lại bản release gần nhất nếu vừa có deploy, hoặc kích hoạt mô hình dự phòng (fallback model).
- Owner: on-call-engineer

## Alert 3: cost_budget_exceeded

- Tên: cost_budget_exceeded
- Severity: warning
- SLI/SLO liên quan: daily_cost_usd (SLO: < 2.5 USD)
- Điều kiện và thời gian duy trì: daily_cost_usd > 2.5
- Ảnh hưởng tới người dùng: Không có ảnh hưởng trực tiếp tới tính năng, nhưng doanh nghiệp sẽ chịu rủi ro về cạn kiệt ngân sách hoặc khóa tài khoản LLM.
- Ba bước kiểm tra đầu tiên:
  1. Soi panel Tokens In/Out xem lượng tiêu thụ có tăng bất thường không.
  2. Xem Traffic có dấu hiệu bị tấn công spam (bot) không.
  3. Kiểm tra Langfuse xem context (doc_count) nhồi vào prompt có quá dài không.
- Mitigation tạm thời: Áp dụng Rate Limiting chặt chẽ hơn cho các endpoint tốn phí, hoặc chuyển sang model có giá rẻ hơn.
- Owner: team-lead
