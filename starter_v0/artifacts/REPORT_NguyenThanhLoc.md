# Báo Cáo Cá Nhân Lab Day 04 — Research Agent

## Thông Tin Sinh Viên

- **Họ và tên**: Nguyễn Thành Lộc
- **Mã số sinh viên**: 2A202600817
- **Lớp / Nhóm**: Zone 8 - Team 5
- **Nhà cung cấp / Mô hình**: OpenRouter / `openai/gpt-4o-mini`

---

## 1. Kết Quả Đạt Được (Metrics)

Sau các lượt tối ưu hệ thống prompt và tích hợp các công cụ mở rộng, tác vụ đã đạt tỷ lệ chính xác tuyệt đối:

- **Phiên bản tối ưu cuối cùng**: `v3`
- **Mã băm phiên bản (Artifact Version)**: `v3+pe658de69e113+t3c77e0a487fa`
- **Độ chính xác bộ test cơ bản (Base Cases)**: **100% (20/20 PASS)**
  * *File chạy kết quả:* `runs/v3_B_base_openrouter_20260602T135319192847.json`
- **Độ chính xác bộ test nhóm mở rộng (Group Cases)**: **100% (22/22 PASS)**
  * *File chạy kết quả:* `runs/v3_B_group_openrouter_20260602T154912475803.json`
- **File lịch sử hội thoại minh chứng**: `transcripts/v3_openrouter_20260602T135912332846.transcript.json`

---

## 2. Nhật Ký Tối Ưu Hóa (Version Evidence)

| Phiên bản | Thành phần thay đổi | Giả thuyết tối ưu | Điểm trước | Điểm sau | File kết quả chạy |
|---|---|---|---:|---:|---|
| **v0** | Baseline | Cấu hình mặc định ban đầu của prompt và khai báo công cụ | N/A | 0.65 | `v0_B_base...json` |
| **v1** | `system_prompt.md` | Thêm luật chặn câu hỏi ngoài phạm vi, kiểm tra thông tin thiếu (Twitter handle) và ánh xạ tên người dùng để tăng độ chính xác định tuyến | 0.65 | 0.75 | `v1_B_base...json` |
| **v2** | `system_prompt.md` | Kiểm tra sự hiện diện của URL, bắt buộc truyền tham số `response_type` rõ ràng cho clarify, yêu cầu xác nhận trước khi gửi | 0.75 | 0.90 | `v2_B_base...json` |
| **v3** | `system_prompt.md` | Chuẩn hóa làm sạch từ khóa tìm kiếm (bỏ các từ "tin", "tweet") và thiết lập quy tắc duy trì trạng thái bỏ công cụ (permanent tool drop) | 0.90 | 1.00 | `v3_B_base...json` |

---

## 3. Đóng Góp Cá Nhân Nổi Bật

### A. Triển khai & Tối ưu hóa Công cụ Wikipedia (`tools/wikipedia/`)
* **Lập trình logic tìm kiếm**: Viết mã nguồn cho công cụ `wikipedia_search` gọi trực tiếp vào API của MediaWiki để lấy thông tin tóm tắt và link bài viết tương ứng.
* **Tự động nhận diện ngôn ngữ & sửa lỗi**:
  * Phát hiện lỗi khi tìm kiếm bằng tiếng Việt có dấu trên Wikipedia tiếng Anh dẫn đến các kết quả không liên quan (ví dụ: tìm "lịch sử Internet" lại ra ca sĩ Amee).
  * Khắc phục bằng cách tự động nhận diện ký tự tiếng Việt trong truy vấn để định tuyến tìm trên `vi.wikipedia.org` trước, sau đó tự động fallback về `en.wikipedia.org` nếu không có kết quả.

### B. Xây dựng Streamlit Chat UI & Quản lý Nhật ký
* **Phát triển UI**: Thiết kế giao diện chat cao cấp theo phong cách Dark Mode Glassmorphism trực quan.
* **Tích hợp Live Trace**: Hiển thị luồng tư duy (thoughts), tham số truyền và kết quả thô dạng JSON của các công cụ trực tiếp trên giao diện qua các hộp expander.
* **Auto-Save Transcripts**: Thêm cơ chế tự động ghi lại lịch sử chat và log thực thi của Web UI vào thư mục `transcripts/` sau mỗi lượt gửi tin nhắn của người dùng, đi kèm nút xóa bộ nhớ tạm để tạo phiên mới.
* **Tích hợp Cloudflare Tunnel**: Chạy `cloudflared` tạo tunnel bảo mật chia sẻ ứng dụng localhost ra môi trường internet công cộng cho nhóm chạy thử nghiệm.

---

## 4. Phân Tích Lỗi & Giải Pháp (Failure Analysis)

Tôi đã phân tích các ca kiểm thử thất bại ở baseline và đưa ra giải pháp sửa đổi trong hệ thống prompt:

1. **Lỗi R08 & R14 (Ngoài phạm vi):** Người dùng yêu cầu giải toán hoặc viết mã nguồn Python nhưng Agent vẫn gọi tool. 
   * *Giải pháp:* Viết luật chặn chặt chẽ, từ chối thẳng thắn và không gọi bất kỳ công cụ nào.
2. **Lỗi R10 & R11 (Thiếu thông tin):** Tự ý đoán URL hoặc tài khoản Twitter khi thiếu thông tin đầu vào.
   * *Giải pháp:* Ép buộc gọi công cụ `clarify` với `response_type: "text"` để hỏi lại người dùng.
3. **Lỗi R12 (Ranh giới xác nhận):** Gửi tin nhắn Telegram ngay lập tức mà không hỏi ý kiến người dùng.
   * *Giải pháp:* Thêm ranh giới bảo mật bắt buộc hỏi xác nhận qua `clarify` với `response_type: "yes_no"` trước khi gửi.
4. **Lỗi M06 (Duy trì việc tắt công cụ):** Không tắt hẳn nguồn Twitter khi người dùng yêu cầu "bỏ Twitter, chuyển sang tìm trên web".
   * *Giải pháp:* Thiết lập luật tắt vĩnh viễn (permanent drop) đối với công cụ bị yêu cầu loại bỏ trong suốt cuộc hội thoại.

---

## 5. Minh Chứng Chạy Thử Nghiệm Thực Tế (Live Chat Evidence)

Tôi đã thực hiện kiểm tra thủ công cuộc trò chuyện thực tế để đảm bảo hệ thống phản hồi tự nhiên và chính xác:

- **Turn 1 (User):** *"Tin tức công nghệ hôm nay có gì mới không?"*
  - **Tool call thực tế:** `lookup(query="công nghệ", timeframe="day", topic="news")`
  - **Kết quả:** Trả về danh sách tóm tắt 5 bài viết công nghệ mới nhất trong ngày kèm link trích dẫn nguồn rõ ràng.
- **Turn 2 (User):** *"Dịch câu 'Hello' sang tiếng Pháp (fr) giúp mình."*
  - **Tool call thực tế:** `translate(text="Hello", target_lang="fr")`
  - **Kết quả:** Trả về từ dịch `"Bonjour"`.
- **Turn 3 (User):** *"Giá của đồng coin ETH trên Binance là bao nhiêu?"*
  - **Tool call thực tế:** `crypto(symbol="ETH")`
  - **Kết quả:** Lấy tỷ giá ETH/USDT thực tế theo thời gian thực từ sàn Binance.

---

## 6. Bài Học & Đúc Kết

* **Prompt Engineering là chìa khóa:** Sự thay đổi nhỏ trong prompt (ví dụ: yêu cầu làm sạch từ khóa tìm kiếm, strip các từ "tin", "tweet") mang lại hiệu quả định tuyến vượt trội hơn hẳn so với cấu hình mặc định.
* **Bảo mật và Kiểm soát ranh giới:** Việc thiết lập quy trình kiểm tra tham số thiếu và xác nhận trước khi thực hiện hành động viết (Telegram) giúp Agent hoạt động an toàn và tin cậy hơn, tránh phát tán thông tin rác.
* **Thiết kế phần mềm linh hoạt:** Khi viết các công cụ bổ sung như `wikipedia`, `github_search`, `translate`, `crypto`, `weather`, việc thiết kế các hàm tự động xử lý ngoại lệ và fallback (như tự động đổi sang tiếng Việt trên Wikipedia, fallback từ JSON sang Text trên wttr.in) giúp ứng dụng hoạt động ổn định trước các lỗi kết nối từ các dịch vụ API bên ngoài.
