# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** [Tên nhóm]
**Thành viên:** [Họ tên từng thành viên]
**Ngày:** [Ngày nộp]

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Chủ đề (Domain) & Lý Do Chọn

**Chủ đề:** Học bổng của Đại học Bách khoa Hà Nội.

**Tại sao nhóm chọn chủ đề này?**
> Đây là thông tin quan trọng, cập nhật và có nhu cầu tra cứu cao từ sinh viên, học viên cao học và nghiên cứu sinh. Tất cả nguồn đều là trang chính thức của trường (hust.edu.vn, sdh.hust.edu.vn, scls.hust.edu.vn), công khai, không chứa dữ liệu cá nhân. Chủ đề có cấu trúc rõ ràng (điều kiện, mức hỗ trợ, đối tượng, thời gian) nên phù hợp để xây dựng hệ thống RAG có khả năng lọc theo audience và category.

### Danh sách tài liệu (Data Inventory)

| #   | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự | Metadata đã gán |
| --- | ------------ | ------------------ | -------------------- | -------- | --------------- |
| 1   | Chi tiết 55 chương trình đào tạo nhận Học bổng Chính phủ theo Nghị định 179 | https://hust.edu.vn/vi/news/tin-tuc-su-kien/chi-tiet-55-chuong-trinh-dao-tao-tai-bach-khoa-ha-noi-nhan-hoc-bong-chinh-phu-theo-nghi-dinh-179-655959.html | 2026-09-19 / not-stated | Chưa đo (sau làm sạch) | audience=undergraduate-student, category=Học bổng Chính phủ (Nghị định 179), language=vi |
| 2   | Học Kỹ thuật - Công nghệ tại Bách khoa Hà Nội với Học bổng Chính phủ 2026 | https://hust.edu.vn/vi/news/tin-tuc-su-kien/hoc-ky-thuat-cong-nghe-tai-bach-khoa-ha-noi-vung-tai-chinh-voi-hoc-bong-chinh-phu-2026-655930.html | 2026-09-19 / not-stated | Chưa đo (sau làm sạch) | audience=undergraduate-student, category=Học bổng Chính phủ (Nghị định 179), language=vi |
| 3   | Bách khoa Hà Nội miễn học phí cho tất cả NCS trúng tuyển từ 2026 | https://hust.edu.vn/vi/news/tuyen-sinh-dao-tao-cong-tac-sinh-vien/bach-khoa-ha-noi-trao-4-ty-dong-hoc-bong-sau-dai-hoc-mien-hoc-phi-cho-tat-ca-ncs-trung-tuyen-tu-2026-655834.html | 2026-09-19 / not-stated | Chưa đo (sau làm sạch) | audience=graduate-student, category=Học bổng sau đại học / Miễn học phí NCS, language=vi |
| 4   | Đại học Bách khoa Hà Nội “bao trọn” học phí cho NCS từ 2026 | https://hust.edu.vn/vi/news/tuyen-sinh-dao-tao-cong-tac-sinh-vien/dai-hoc-bach-khoa-ha-noi-phat-trien-nguon-luc-nghien-cuu-bao-tron-hoc-phi-cho-ncs-655842.html | 2026-09-19 / not-stated | Chưa đo (sau làm sạch) | audience=graduate-student, category=Học bổng sau đại học / Miễn học phí NCS, language=vi |
| 5   | Danh sách học viên và nghiên cứu sinh nhận học bổng Sau đại học năm 2025 | https://sdh.hust.edu.vn/Default.aspx?scid=23&CategoryID=111&nid=3511 | 2026-09-19 / 2025 | Chưa đo (sau làm sạch) | audience=graduate-student, category=Danh sách học bổng sau đại học, language=vi |
| 6   | Thông báo Học bổng Sau đại học Hội khuyến học Thương gia Đài Loan năm 2026 | https://sdh.hust.edu.vn/Default.aspx?scid=23&CategoryID=111&nid=3554 | 2026-09-19 / 2026 | Chưa đo (sau làm sạch) | audience=graduate-student, category=Học bổng đối tác (Đài Loan), language=vi |
| 7   | Quy định mới về xét và cấp học bổng trao đổi nước ngoài | https://scls.hust.edu.vn/vi/news/dao-tao-cong-tac-sinh-vien/dai-hoc-bach-khoa-ha-noi-ban-hanh-quy-dinh-moi-ve-xet-va-cap-hoc-bong-trao-doi-nuoc-ngoai-578.html | 2026-09-19 / 2025-11 | Chưa đo (sau làm sạch) | audience=undergraduate-student, category=Học bổng trao đổi nước ngoài, language=vi |
| 8   | Bách khoa Hà Nội và doanh nghiệp tài trợ hơn 3 tỷ đồng học bổng năm 2025 | https://hust.edu.vn/vi/news/hoat-dong-chung/bach-khoa-ha-noi-va-doanh-nghiep-hop-tac-tai-tro-hon-3-ty-dong-hoc-bong-nam-2025-655389.html | 2026-09-19 / not-stated | Chưa đo (sau làm sạch) | audience=undergraduate-student, category=Học bổng doanh nghiệp (Chắp cánh Foundation), language=vi |
| 9   | 39 sinh viên vượt khó học giỏi nhận học bổng trị giá hơn 700 triệu đồng | https://hust.edu.vn/vi/news/hoat-dong-chung/39-sinh-vien-vuot-kho-hoc-gioi-nhan-hoc-bong-tri-gia-hon-700-trieu-dong-655646.html | 2026-09-19 / not-stated | Chưa đo (sau làm sạch) | audience=undergraduate-student, category=Học bổng doanh nghiệp (Chắp cánh Bách khoa), language=vi |
| 10  | Học bổng Chắp cánh Bách khoa tiếp sức tân sinh viên K70 | https://hust.edu.vn/vi/news/hoat-dong-chung/hoc-bong-chap-canh-bach-khoa-tiep-suc-tan-sinh-vien-k70-655558.html | 2026-09-19 / not-stated | Chưa đo (sau làm sạch) | audience=undergraduate-student, category=Học bổng doanh nghiệp (Chắp cánh Bách khoa), language=vi |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata       | Kiểu     | Ví dụ giá trị                                      | Tại sao hữu ích cho truy xuất (retrieval)? |
| --------------------- | -------- | -------------------------------------------------- | ------------------------------------------ |
| url / source_url      | string   | https://hust.edu.vn/...                            | Truy xuất nguồn gốc, kiểm chứng thông tin  |
| retrieved_at          | date     | 2026-09-19                                         | Biết độ mới của dữ liệu                    |
| doc_id                | string   | HB-CP-179-2026                                     | Định danh duy nhất, dễ quản lý & cập nhật  |
| title                 | string   | Chi tiết 55 chương trình...                        | Hiển thị kết quả, hỗ trợ keyword search    |
| audience              | string   | undergraduate-student / graduate-student           | Lọc chính xác theo đối tượng (sinh viên / NCS) |
| department            | string   | Ban Đào tạo - Bộ phận Sau đại học                  | Lọc theo đơn vị ban hành                   |
| category              | string   | Học bổng Chính phủ (Nghị định 179)                 | Lọc theo loại học bổng                     |
| language              | string   | vi                                                 | Đảm bảo ngôn ngữ phù hợp                   |
| document_version      | string   | 2025 / 2026 / not-stated                           | Ưu tiên tài liệu mới / đúng phiên bản      |
| license_or_permission | string   | Công khai (website chính thức HUST)                | Xác nhận quyền sử dụng hợp pháp            |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare()` trên tài liệu `vnu-ulis-cam-nang-hoc-bong.md` (tham số `chunk_size = 200`):

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| `vnu-ulis-cam-nang-hoc-bong.md` | FixedSizeChunker (`fixed_size`) | 91 | 198.09 | **Kém.** Cắt cứng nhắc theo số ký tự. Dễ cắt ngang giữa câu hoặc chia cắt danh sách làm mất tiêu đề/ngữ cảnh. |
| `vnu-ulis-cam-nang-hoc-bong.md` | SentenceChunker (`by_sentences`) | 34 | 467.82 | **Kém.** Chunk quá dài (>460 ký tự). Dễ gom thành các khối khổng lồ nếu văn bản dùng nhiều gạch đầu dòng thay vì dấu chấm câu. |
| `vnu-ulis-cam-nang-hoc-bong.md` | RecursiveChunker (`recursive`) | 123 | 130.08 | **Khá.** Ưu tiên cắt theo đoạn/câu nên giữ ngữ nghĩa tốt hơn. Tuy nhiên, các đoạn quá dài vẫn bị ép cắt ngang, có thể làm đứt liên kết với tiêu đề. |
### Chiến lược của từng thành viên

> Mỗi thành viên điền một khối dưới đây (copy thêm nếu nhóm có nhiều hơn 3 người).

<!-- **Thành viên 1 — [Tên]**
- **Loại chiến lược:** [FixedSize / Sentence / Recursive / custom]
- **Mô tả & lý do chọn cho chủ đề này:** *(2-3 câu)*
- **Code snippet (nếu custom):**
```python
# Dán mã nguồn (implementation) vào đây
``` -->

**Thành viên 1 — Hoàng Trung Khải**
- **Loại chiến lược:** MarkdownHeading
- **Mô tả & lý do chọn cho chủ đề này:** Chiến lược này phân tách văn bản dựa trên các thẻ tiêu đề (Heading) của Markdown và tự động đính kèm tiêu đề đó vào phần đầu của các chunk con nếu đoạn văn bên dưới quá dài. Vì dữ liệu về quy chế học bổng luôn được cấu trúc chặt chẽ theo các mục (ví dụ: tên học bổng, đối tượng, điều kiện, mức cấp phát), cách làm này giúp bảo toàn ngữ cảnh trọn vẹn, đảm bảo hệ thống RAG không bao giờ trả về một "điều kiện xét tuyển" lơ lửng mà thiếu đi thông tin nó thuộc loại học bổng nào.
- **Code snippet:**
```python
class MarkdownHeadingChunker:
    def __init__(self, chunk_size: int = 300):
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        chunks = []
        parts = re.split(r'(^#+\s+.*$)', text, flags=re.MULTILINE)
        
        current_heading = ""
        current_block = ""
        
        for part in parts:
            if re.match(r'^#+\s+', part):
                if current_block.strip():
                    chunks.extend(self._split_large_block(current_block, current_heading))
                current_heading = part.strip()
                current_block = current_heading + "\n"
            else:
                current_block += part
                
        if current_block.strip():
            chunks.extend(self._split_large_block(current_block, current_heading))
            
        return [c for c in chunks if c.strip()]

    def _split_large_block(self, text: str, current_heading: str) -> list[str]:
        """Chia nhỏ một khối văn bản nếu nó vượt quá chunk_size, luôn đính kèm heading."""
        if len(text) <= self.chunk_size:
            return [text.strip()]
            
        sub_chunks = []
        paragraphs = text.split('\n\n')
        
        temp_chunk = current_heading + "\n" if current_heading else ""
        
        for p in paragraphs:
            p = p.strip()
            if not p or p == current_heading:
                continue
                
            if len(temp_chunk) + len(p) < self.chunk_size:
                temp_chunk += p + "\n\n"
            else:
                if temp_chunk.strip() and temp_chunk.strip() != current_heading:
                    sub_chunks.append(temp_chunk.strip())
                temp_chunk = (current_heading + "\n" + p + "\n\n") if current_heading else (p + "\n\n")
                
        if temp_chunk.strip() and temp_chunk.strip() != current_heading:
            sub_chunks.append(temp_chunk.strip())
            
        return sub_chunks
```


**Thành viên 2 — Nguyễn Thu Trang**
- **Loại chiến lược:** RecursiveChunker
- **Mô tả & lý do chọn:** Chiến lược này phân tách văn bản đệ quy dựa trên mức độ ưu tiên của các dấu phân cách (như xuống dòng kép, dấu chấm câu, khoảng trắng) nhằm giữ trọn vẹn các đoạn văn hoặc câu dưới một giới hạn kích thước nhất định.

**Thành viên 3 — Nguyễn Minh Dương**
- **Loại chiến lược:** SentenceChunker
- **Mô tả & lý do chọn:** Chiến lược này phân tách văn bản dựa trên ranh giới của các câu hoàn chỉnh (thường được nhận diện qua dấu chấm, dấu chấm hỏi hoặc dấu chấm cảm). Việc chọn SentenceChunker giúp đảm bảo mỗi đoạn văn bản (chunk) luôn giữ được trọn vẹn ý nghĩa của câu, không bị ngắt quãng giữa chừng.

# Đánh Giá Và So Sánh Chiến Lược Phân Tách Dữ Liệu (Chunking)

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| **1. Hoàng Trung Khải** | MarkdownHeading | 9/10 | Giữ vững ngữ cảnh phân cấp, luôn gắn chặt các thông tin chi tiết (điều kiện, mức thưởng) với tên học bổng tương ứng. | Phụ thuộc hoàn toàn vào việc văn bản gốc phải được định dạng thẻ heading (Markdown) rõ ràng, chuẩn xác. |
| **2. Nguyễn Thu Trang** | RecursiveChunker | 7.5/10 | Cân bằng tốt kích thước chunk và linh hoạt xử lý được nhiều loại định dạng văn bản khác nhau. | Dễ làm đứt gãy mối liên kết giữa tiêu đề (tên học bổng) và nội dung bên dưới nếu đoạn văn bản quá dài. |
| **3. Nguyễn Minh Dương** | SentenceChunker | 5.0/10 | Đảm bảo không bao giờ bị ngắt ý giữa chừng; các đoạn trích xuất luôn là câu hoàn chỉnh về mặt ngữ pháp. | Phá vỡ hoàn toàn cấu trúc tài liệu; các câu điều kiện (VD: "GPA từ 3.2") khi đứng độc lập sẽ bị mất ngữ cảnh, không biết thuộc học bổng nào. |

### Chiến lược nào tốt nhất cho chủ đề này? Tại sao?

> MarkdownHeading là chiến lược tốt nhất cho chủ đề "Quy chế học bổng" vì loại văn bản này có tính cấu trúc phân tầng cực kỳ chặt chẽ. Việc tự động đính kèm tiêu đề mục vào mọi đoạn văn con giúp giải quyết triệt để tình trạng "mất ngữ cảnh" trong RAG, đảm bảo hệ thống luôn biết chính xác một điều kiện xét tuyển hay mức hỗ trợ tài chính đang thuộc về loại học bổng cụ thể nào. Tuy nhiên trong data không phải lúc nào cũng có cấu trúc Markdown thật nhưng MarkdownHeading có fallback về Recursive để giải quyết tình huống này.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> *Viết 2-3 câu:*

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> *Liệt kê 2-3 ý:*

**Bài học rút ra khi so sánh trong nhóm:**
> *Viết 2-3 câu — cùng tài liệu nhưng chiến lược khác nhau dẫn tới khác biệt gì?*

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | / 10 |
| Thiết kế chiến lược (Strategy Design) | / 15 |
| Chất lượng truy xuất (Retrieval Quality) | / 10 |
| Thuyết trình (Demo) | / 5 |
| **Tổng phần nhóm** | **/ 40** |
