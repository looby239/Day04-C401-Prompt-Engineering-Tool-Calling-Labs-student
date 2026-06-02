# Báo Cáo Lab Day 04 v2 — Research Agent

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research Agent hỗ trợ tìm kiếm tin tức trên mạng xã hội và web, tra cứu tài liệu nội bộ, tìm kiếm Wikipedia và bài báo arXiv, dịch thuật, lấy tỷ giá tiền số, dự báo thời tiết, tự động tổng hợp digest và gửi lên Telegram sau khi có sự xác nhận của người dùng.

### Link dùng thử (deploy)
**URL**: https://charter-survive-sku-model.trycloudflare.com

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại người dùng khi thiếu thông tin hoặc yêu cầu xác nhận | không |
| timeline | Lấy các bài đăng gần đây của một người dùng trên mạng xã hội | không |
| social_search | Tìm kiếm các bài đăng trên mạng xã hội theo từ khóa | không |
| lookup | Tra cứu thông tin trên internet (tin tức hoặc tìm kiếm chung) | không |
| fetch | Lấy nội dung văn bản từ một địa chỉ URL | không |
| format | Trình bày và định dạng danh sách dữ liệu thành bản tổng hợp (digest) | không |
| send | Gửi một đoạn văn bản (ví dụ lên Telegram) khi đã có cờ xác nhận | không |
| policy | Tìm kiếm trong tài liệu quy định nội bộ của công ty | không |
| papers | Tìm kiếm bài báo khoa học trên arXiv | không |
| paper_text | Lấy nội dung đầy đủ của bài báo arXiv theo đường dẫn hoặc ID | không |
| wikipedia | Tìm kiếm bài viết và lấy nội dung tóm tắt từ Wikipedia (có tự động nhận diện tiếng Việt) | **Có** |
| github_search | Tìm kiếm các repository trên GitHub (sắp xếp theo sao, forks, cập nhật) | **Có** |
| translate | Dịch đoạn văn bản sang ngôn ngữ chỉ định sử dụng Google Translate API | **Có** |
| crypto | Lấy giá thời gian thực của đồng coin (BTC, ETH...) từ Binance API | **Có** |
| weather | Lấy thông tin thời tiết hiện tại của một địa điểm từ wttr.in | **Có** |

## A3. Câu hỏi mẫu để thử

1. *"Tra Wikipedia về lịch sử phát triển của mạng Internet."*
2. *"Dịch giúp mình đoạn này sang tiếng Việt: 'Artificial Intelligence is transforming our future'"*
3. *"Giá của đồng coin ETH hiện tại trên Binance là bao nhiêu?"*
4. *"Thời tiết hiện tại ở Đà Nẵng thế nào?"*
5. *"Tìm các repository về 'stable diffusion' trên GitHub."*

---

## Team

- **Team**: Zone 8 - Team 5
Nguyễn Thành Lộc - 2A202600817
Đặng Tiến Quyền - 2A202600896
Trần Trung Kiên - 2A202600850
- **Provider/model**: OpenRouter / `openai/gpt-4o-mini`

## Chỉ số cuối cùng (Final Metrics)

- **Final version**: v4
- **Final artifact_version**: `v4+p245fdf2e05b3+te385c98358a6`
- **Best base run file**: `runs/v3_B_base_openrouter_20260602T135319192847.json`
- **Base case accuracy**: 1.0 (100%)
- **Base tool routing accuracy**: 1.0 (100%)
- **Base argument accuracy**: 1.0 (100%)
- **Group eval run file**: `runs/v3_B_group_openrouter_20260602T151548598670.json`
- **Group eval accuracy**: 1.0 (100%)
- **Chat transcript file**: `transcripts/v3_openrouter_20260602T135912332846.transcript.json`

## Minh chứng các phiên bản (Version Evidence)

| Phiên bản | Thành phần thay đổi | Giả thuyết tối ưu | Điểm trước | Điểm sau | File chạy kết quả |
|---|---|---|---:|---:|---|
| v0 | baseline | Cấu hình mặc định ban đầu của prompt và khai báo công cụ | N/A | 0.65 | `runs/v0_B_base_openrouter_20260602T125543109510.json` |
| v1 | `system_prompt.md` | Bổ sung các chỉ dẫn cụ thể cho các câu hỏi ngoài phạm vi, thiếu thông tin, xác nhận và ánh xạ handle sẽ cải thiện độ chính xác định tuyến và tham số | 0.65 | 0.75 | `runs/v1_B_base_openrouter_20260602T130157915173.json` |
| v2 | `system_prompt.md` | Kiểm tra rõ ràng sự xuất hiện của URL trong đầu vào người dùng, bắt buộc tham số response_type rõ ràng và ưu tiên xác nhận hơn làm rõ văn bản sẽ khắc phục lỗi định tuyến URL và lỗi ranh giới | 0.75 | 0.90 | `runs/v2_B_base_openrouter_20260602T130343289003.json` |
| v3 | `system_prompt.md` | Loại bỏ các từ bổ trợ như 'tin' và 'tweet' khỏi tham số truy vấn và thiết lập chuyển đổi công cụ vĩnh viễn sẽ khắc phục lỗi không khớp tên song song và lỗi giữ trạng thái chuyển đổi công cụ nhiều lượt | 0.90 | 1.00 | `runs/v3_B_base_openrouter_20260602T135319192847.json` |
| v4 | `tools.yaml`, `system_prompt.md` | Tích hợp các công cụ bonus (GitHub, Dịch thuật, Tiền số, Thời tiết) để cung cấp trải nghiệm trợ lý nghiên cứu hoàn chỉnh | 1.00 | 1.00 | `runs/v3_B_group_openrouter_20260602T151548598670.json` |

## Phân tích các trường hợp lỗi (Failure Analysis)

| ID ca lỗi | Loại lỗi | Tool thực tế gọi | Lý do lỗi | Giải pháp khắc phục |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | `send(text=...)` | Việc gộp bài toán toán học đã kích hoạt gọi công cụ khi đáng lẽ phải bị từ chối | Từ chối trả lời và không gọi công cụ nào |
| R10_missing_handle | missing_info | `timeline(screenname='sama')` | Tự đoán tài khoản 'sama' khi thiếu tên người dùng | Gọi công cụ `clarify` với `response_type: "text"` |
| R11_missing_url | missing_info | `fetch(url='https://example.com/article')` | Tự đoán địa chỉ URL khi bị thiếu | Gọi công cụ `clarify` with `response_type: "text"` |
| R12_confirm_before_send | wrong_boundary | `send(text=...)` | Gửi tin nhắn Telegram ngay lập tức mà không có sự xác nhận của người dùng | Gọi công cụ `clarify` với `response_type: "yes_no"` |
| R13_parallel_web_and_tweets | wrong_tool | `lookup(query='tin AI', ...)` | Truy vấn bị trích xuất thành 'tin AI' thay vì 'AI' | Thêm quy tắc Làm sạch Truy vấn để loại bỏ các từ bổ trợ |
| R14_out_of_scope_coding | out_of_scope | `send(text=...)` | Yêu cầu viết mã đệ quy Python kích hoạt gọi công cụ | Từ chối các tác vụ lập trình và không gọi công cụ nào |
| M06_switch_tool | wrong_tool | `lookup` + `social_search` | Không bỏ qua các cuộc gọi công cụ Twitter sau khi có hướng dẫn rõ ràng để chuyển sang web | Thêm quy tắc duy trì trạng thái chuyển đổi công cụ vĩnh viễn |

## Các ca kiểm thử của Nhóm (Team Eval Cases)

Danh sách các trường hợp được thêm vào file `data/eval_group.json`:

| ID ca kiểm thử | Nội dung kiểm thử | Kỳ vọng Tool / Hành vi | Kết quả |
|---|---|---|---|
| G01_out_of_scope_image | Yêu cầu tạo hình ảnh | Từ chối trả lời, không gọi công cụ | PASS |
| G02_wikipedia_search | Tìm kiếm Wikipedia cho một truy vấn | gọi công cụ `wikipedia` | PASS |
| G03_arxiv_search | Tìm kiếm arXiv cho Quantum Computing | gọi công cụ `papers` | PASS |
| G04_missing_handle_tweets | Lấy tweet khi thiếu screenname | gọi công cụ `clarify` (`response_type: "text"`) | PASS |
| G05_send_confirmation | Đăng bài lên Telegram | gọi công cụ `clarify` (`response_type: "yes_no"`) | PASS |
| GM01_wikipedia_refinement | Cập nhật truy vấn Wikipedia trong hội thoại nhiều lượt | gọi công cụ `wikipedia` với truy vấn mới | PASS |
| GM02_arxiv_to_text | Tìm bài báo sau đó đọc nội dung văn bản | gọi công cụ `paper_text` với các đối số chính xác | PASS |
| GM03_persistent_out_of_scope | Người dùng kiên trì yêu cầu lập trình | Từ chối trả lời, không gọi công cụ | PASS |
| GM04_clarify_name_mapping | Thiếu handle được làm rõ bằng tên thường | gọi công cụ `timeline` kèm ánh xạ handle | PASS |
| GM05_papers_to_wikipedia | Chuyển đổi từ arXiv sang Wikipedia | gọi công cụ `wikipedia` với chủ đề | PASS |
| G06_github_search | Tìm kiếm Github cho một truy vấn | gọi công cụ `github_search` | PASS |
| GM06_github_sort_refinement | Chuyển đổi truy vấn Github nhiều lượt | gọi công cụ `github_search` với đối số đúng | PASS |

## Minh chứng chat trực tiếp (Live Chat Evidence)

| Lượt | Yêu cầu của người dùng | Các cuộc gọi công cụ | Minh chứng phiên bản | Kết quả đầu ra |
|---|---|---|---|---|
| 1 | "Tin tức công nghệ hôm nay có gì mới không?" | `lookup(query="công nghệ", timeframe="day", topic="news")` | `v3` | Lấy 5 dòng tiêu đề tin tức công nghệ hàng đầu hôm nay, định dạng dưới dạng danh sách markdown kèm tiêu đề và liên kết. |

## Minh chứng phần cộng điểm (Bonus Evidence)

| Phần cộng điểm | File minh chứng | Nội dung hoạt động tốt | Rủi ro / Cơ chế bảo vệ |
|---|---|---|---|
| Tìm kiếm Wikipedia | `tools/wikipedia/tool.py` | Truy vấn MediaWiki API và lấy tóm tắt cho các kết quả tìm kiếm. | Thêm kiểm tra độ dài kết quả tìm kiếm để ngăn chặn vòng lặp rỗng. |
| Tìm kiếm GitHub | `tools/github_search/tool.py` | Truy vấn GitHub API cho các repository. | Thêm hỗ trợ cho các tham số sắp xếp và giới hạn. |
| Giao diện Web (UI) | `app.py` | Giao diện chat Streamlit với chức năng bật/tắt nhật ký theo dõi thực thi. | Thêm try-except xung quanh quá trình hoàn thành của LLM để bắt lỗi khóa API một cách nhẹ nhàng. |
| Công cụ Dịch thuật | `tools/translate/tool.py` | Dịch văn bản bằng cách sử dụng API công cộng của Google Translate. | Xử lý an toàn khi đầu vào trống. |
| Bảng giá Tiền số | `tools/crypto/tool.py` | Lấy giá coin theo thời gian thực từ API Binance. | Xử lý ánh xạ ký hiệu coin (ví dụ: BTC thành BTCUSDT). |
| Thông tin Thời tiết | `tools/weather/tool.py` | Truy vấn chi tiết thời tiết hiện tại bằng wttr.in. | Cơ chế fallback khi vị trí không hợp lệ. |

## Đúc kết và phản hồi (Reflection)

- **Những lỗi nào thuộc về cách xử lý trong file `system_prompt.md`?**
  Tất cả các ràng buộc về hành vi định tuyến, ánh xạ tên sang handle, ranh giới xác nhận, quy tắc ngoài phạm vi và duy trì trạng thái nhiều lượt.
- **Những lỗi nào thuộc về cách xử lý trong file `tools.yaml`?**
  Mô tả chính xác các tham số, giá trị mặc định và danh sách lựa chọn (enum) để có giao diện gọi công cụ sạch hơn.
- **Những lỗi nào cần đánh giá thủ công thay vì chấm điểm tự động?**
  Các thông điệp từ chối đối với các yêu cầu ngoài phạm vi hoặc các phản hồi làm rõ thông tin chat, vì chúng đòi hỏi con người đánh giá về tông giọng và tính hữu ích của cuộc hội thoại.
- **Bạn sẽ cải tiến điều gì tiếp theo?**
  Thêm tìm kiếm ngữ nghĩa (semantic search) trên các tài liệu được truy xuất để cải thiện độ chính xác của câu trả lời, hỗ trợ các yêu cầu API song song không đồng bộ để chạy công cụ nhanh hơn và mở rộng công cụ GitHub để tìm kiếm các file hoặc issue cụ thể.
