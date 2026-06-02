# Báo Cáo Cá Nhân Lab Day 04 — Research Agent

## Thông Tin Sinh Viên

- **Họ và tên**: Đặng Tiến Quyền
- **Mã số sinh viên**: 2A202600896
- **Lớp / Nhóm**: Zone 8 - Team 5
- **Nhà cung cấp / Mô hình**: OpenRouter / `openai/gpt-4o-mini`

---

## 1. Kết Quả Đạt Được (Metrics)

Sau quá trình nghiên cứu, tinh chỉnh prompt và mở rộng các công cụ cùng tập kiểm thử, tôi đã phối hợp cùng nhóm đưa hệ thống đạt độ chính xác tuyệt đối:

- **Phiên bản tối ưu cuối cùng**: `v3`
- **Mã băm phiên bản (Artifact Version)**: `v3+pa4f40e6bf80e+te7ddb1d9334d`
- **Độ chính xác bộ test cơ bản (Base Cases)**: **100% (20/20 PASS)**
  * *File chạy kết quả:* `runs/v3_B_base_openrouter_20260602T153650945291.json`
- **Độ chính xác bộ test nhóm mở rộng (Group Cases)**: **100% (22/22 PASS)**
  * *File chạy kết quả:* `runs/v3_B_group_openrouter_20260602T154510214638.json`
- **File lịch sử hội thoại minh chứng**: `transcripts/v3_openrouter_20260602T154720695314.transcript.json`

---

## 2. Nhật Ký Tối Ưu Hóa (Version Evidence)

Tôi đã tham gia phân tích lỗi baseline và cùng nhóm thiết lập các phiên bản tối ưu hóa qua các vòng:

| Phiên bản | Thành phần thay đổi | Giả thuyết tối ưu | Điểm trước | Điểm sau | File kết quả chạy |
|---|---|---|---:|---:|---|
| **v0** | Baseline | Cấu hình mặc định ban đầu của prompt và khai báo công cụ | N/A | 0.65 | `v0_B_base...json` |
| **v1** | `system_prompt.md` | Đưa ra quy tắc cụ thể cho out-of-scope, các case thiếu tham số (missing handle) và thiết lập mapping cho tài khoản của chuyên gia công nghệ để tránh phỏng đoán vô căn cứ | 0.65 | 0.75 | `v1_B_base...json` |
| **v2** | `system_prompt.md` | Bắt buộc kiểm tra sự hiện diện của URL thực tế trước khi fetch, bắt buộc cấu hình tham số `response_type` cho clarify để làm rõ thông tin | 0.75 | 0.90 | `v2_B_base...json` |
| **v3** | `system_prompt.md` | Xử lý triệt để việc làm sạch từ khóa tìm kiếm (Query Cleaning) để loại bỏ các từ phụ như "tin", "tweet" và củng cố logic tắt vĩnh viễn công cụ bị loại trừ | 0.90 | 1.00 | `v3_B_base...json` |

---

## 3. Đóng Góp Cá Nhân Nổi Bật

### A. Triển khai các công cụ dịch thuật và thông tin thị trường (`tools/translate/` & `tools/crypto/`)
* **Lập trình công cụ `translate`**: Thiết kế và triển khai module dịch thuật đa ngôn ngữ dựa trên API Google Translate công khai, tự động xử lý ngoại lệ và trả về định dạng chuẩn cho agent tổng hợp thông tin nghiên cứu từ tài liệu nước ngoài.
* **Lập trình công cụ `crypto`**: Xây dựng module kết nối API của Binance để lấy giá tiền điện tử thời gian thực. 
  - Khắc phục lỗi truyền tham số: API của Binance yêu cầu tên cặp giao dịch đầy đủ (như `BTCUSDT`), do đó tôi đã viết logic tự động ánh xạ thông minh từ các truy vấn viết tắt của người dùng (ví dụ: `BTC`, `ETH`) thành các mã cặp chuẩn của sàn giao dịch trước khi gửi request.

### B. Mở rộng & Sửa lỗi bộ kiểm thử tự động (`eval_group.json`)
* **Bổ sung các test case bao phủ diện rộng**: Tự thiết kế và bổ sung các ca kiểm thử đơn turn và đa turn cho các công cụ mới: `G07_translate_text`, `G08_crypto_price`, `G09_weather_info`, `GM08_translate_refinement`, `GM09_crypto_switching`, `GM10_weather_switching`.
* **Khắc phục lỗi logic đa turn trong kiểm thử (`GM07_send_telegram_confirmed` & `GM11_github_stars`):**
  - Giải quyết lỗi agent gọi song song trùng lặp tool github khi thiếu turn làm rõ bằng cách cấu trúc lại quy trình 3 turn chi tiết.
  - Sửa lỗi mô phỏng xác nhận của Agent trong bộ chấm điểm: Thiết lập cấu trúc turn `assistant` trung gian trong `eval_group.json` để agent nhận thức được bản tin đã được xác nhận trước khi gọi tool ghi `send`, giúp bộ test đạt độ chính xác **100% PASS**.

---

## 4. Phân Tích Lỗi & Giải Pháp (Failure Analysis)

Tôi đã tập trung nghiên cứu xử lý các ranh giới hoạt động của Agent:
* **Xác nhận hành vi ghi (Write Action Confirmation):** Ở baseline, Agent tự động gửi tin lên Telegram ngay khi có yêu cầu. Tôi đã đề xuất luật chặn bắt buộc phải tạo turn tương tác `yes_no` để đảm bảo an toàn thông tin.
* **Lọc nhiễu từ khóa (Query Cleaning):** Agent thường lấy nguyên cụm từ người dùng yêu cầu (ví dụ: `"tin tức về AI"`) để đưa vào công cụ tìm kiếm, làm giảm chất lượng kết quả. Việc thêm bước tiền xử lý lọc bỏ các từ khóa phụ đã nâng cao độ chính xác của kết quả tra cứu web.

---

## 5. Minh Chứng Chạy Thử Nghiệm Thực Tế (Live Chat Evidence)

Hội thoại kiểm thử thủ công trên Streamlit Web UI chứng minh sự hoạt động trơn tru của các tính năng tự thêm:
* **Lượt dịch thuật:** Người dùng yêu cầu *"Dịch câu 'Hello' sang tiếng Pháp (fr) giúp mình."* -> Agent gọi chính xác `translate(text="Hello", target_lang="fr")` và hiển thị kết quả dịch thuật chuẩn xác.
* **Lượt tra cứu giá coin:** Người dùng hỏi *"ETH hôm nay bao nhiêu?"* -> Agent tự động ánh xạ thành `crypto(symbol="ETH")` để lấy tỷ giá ETH/USDT thực tế từ Binance.

---

## 6. Bài Học & Đúc Kết

* **Tầm quan trọng của dữ liệu test**: Việc viết thêm và tối ưu hóa bộ test case không chỉ giúp chấm điểm cao hơn mà còn phát hiện ra những lỗ hổng logic tinh vi của Prompt khi đối mặt với ngữ cảnh thực tế (như lỗi gọi trùng lặp công cụ khi thiếu dữ liệu làm rõ).
* **Ranh giới bảo mật (Guardrails)**: Việc phân biệt rõ ràng giữa các tác vụ đọc (Wikipedia, Binance) và viết (Send Telegram) để áp dụng quy trình xác nhận nghiêm ngặt là bài học lớn về an toàn hệ thống khi phát triển các Agent tự hành.
