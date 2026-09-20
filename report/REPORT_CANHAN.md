# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Hoàng Trung Khải
**Nhóm:** Miniature
**Ngày:** 19/09/2026

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Độ tương tự cosine cao (tiến gần đến 1) nghĩa là hai vector embedding đang hướng về cùng một phía trong không gian vector, thể hiện rằng hai đoạn văn bản gốc có ý nghĩa ngữ nghĩa (semantic meaning) và nội dung rất giống nhau hoặc liên quan mật thiết với nhau.

**Ví dụ có độ tương tự CAO:**
- **Câu A:** "Sinh viên thuộc hộ nghèo sẽ được nhà trường xét duyệt cấp học bổng hỗ trợ tài chính 100%."
- **Câu B:** "Chính sách miễn giảm toàn bộ học phí áp dụng cho các sinh viên có hoàn cảnh đặc biệt khó khăn."
- **Tại sao tương đồng:** Dù dùng các từ vựng khác nhau (hộ nghèo/hoàn cảnh khó khăn, học bổng/miễn giảm học phí), cả hai câu đều mang cùng một ý nghĩa cốt lõi về việc hỗ trợ tài chính cho sinh viên nghèo. Mô hình ngôn ngữ sẽ map chúng vào các vector rất gần nhau.

**Ví dụ có độ tương tự THẤP:**
- **Câu A:** "Sinh viên thuộc hộ nghèo sẽ được nhà trường xét duyệt cấp học bổng hỗ trợ tài chính 100%."
- **Câu B:** "Thư viện trung tâm mở cửa phục vụ sinh viên đọc sách từ 8h sáng đến 17h chiều các ngày trong tuần."
- **Tại sao khác:** Hai câu nói về hai chủ đề hoàn toàn độc lập (hỗ trợ tài chính/học bổng và thời gian hoạt động của thư viện). Các vector sẽ hướng theo các chiều khác nhau trong không gian (độ tương tự cosine gần 0).

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Cosine similarity chỉ đo góc giữa hai vector mà bỏ qua độ lớn (magnitude) của chúng, do đó nó không bị ảnh hưởng bởi độ dài của văn bản (số lượng từ). Khoảng cách Euclid sẽ đánh giá sai lệch nếu một tài liệu dài và một tài liệu ngắn có cùng nội dung ngữ nghĩa, vì vector của tài liệu dài sẽ có độ lớn lớn hơn nhiều.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> **Trình bày phép tính:**
> - Bước nhảy (step) cho mỗi chunk = chunk_size - overlap = 500 - 50 = 450 ký tự.
> - Số chunk = 10000 / 450 = 22.22. Làm tròn lên là **23**.
> - Chunk cuối cùng bắt đầu ở vị trí 22 * 450 = 9900, bao gồm 100 ký tự cuối cùng (từ 9900 đến 10000).
> 
> **Đáp án:** 23 chunks.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> - **Thay đổi:** Khi overlap = 100, bước nhảy sẽ là 400. Số chunk = Làm tròn lên (10000 / 400) = 25 chunks. Số lượng chunk tăng lên.
> - **Lý do:** Tăng độ chồng chéo giúp đảm bảo ngữ cảnh ở phần rìa của mỗi chunk không bị cắt đứt đột ngộtngột. Điều này giúp các thuật toán tìm kiếm và LLM sau đó có đủ bối cảnh liền mạch để hiểu trọn vẹn ý nghĩa của đoạn văn.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Tôi sử dụng biểu thức chính quy (regex) `(?<=[.!?])(?:\s+)` để tách văn bản thành các câu dựa trên dấu chấm, chấm hỏi, chấm than theo sau là khoảng trắng. Ngoại lệ (edge case) được xử lý bao gồm việc loại bỏ các khoảng trắng thừa (`strip`), bỏ qua các câu rỗng, và dùng vòng lặp gom nhóm các câu lại sao cho không vượt quá tham số `max_sentences_per_chunk` được chỉ định.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Thuật toán hoạt động bằng cách đệ quy kiểm tra danh sách các ký tự phân cách (seperators) ưu tiên (như `\n\n`, `\n`, `. `). **Trường hợp cơ sở (base case)** là khi độ dài văn bản nhỏ hơn hoặc bằng `chunk_size`, hàm sẽ trả về văn bản đó. Nếu lớn hơn, nó tách văn bản bằng phân cách khả dụng đầu tiên, rồi tuần tự ghép các mảnh vỡ lại; nếu có mảnh nào vẫn vượt `chunk_size`, hàm sẽ gọi đệ quy chính nó trên mảnh đó với các phân cách ở mức độ ưu tiên thấp hơn.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Với `add_documents`, tôi kiểm tra xem hệ thống có cài ChromaDB không: nếu có, sẽ nạp thẳng vào collection qua API của Chroma; nếu không, sẽ chạy in-memory bằng cách lưu metadata, content và embedding vector (sinh từ `embedding_fn`) vào một danh sách các Dictionary. Ở phần `search`, tôi nhúng query thành vector, sau đó duyệt qua store để tính tích vô hướng (dot product) giữa query vector và từng chunk vector, cuối cùng sắp xếp giảm dần (descending) theo điểm số và trả về `top_k`.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> Tôi áp dụng chiến lược lọc trước khi tìm kiếm (Pre-filtering) để tối ưu hiệu suất. Danh sách các chunk sẽ được duyệt và chỉ giữ lại những chunk có `metadata` chứa các cặp key-value trùng khớp hoàn toàn với `metadata_filter` đầu vào, sau đó mới gọi hàm `_search_records` trên danh sách đã lọc. Chức năng `delete_document` thực hiện lọc ngược lại, loại bỏ tất cả các chunk có chứa `doc_id` tương ứng bằng List Comprehension (hoặc gọi API `delete` với điều kiện `where` nếu dùng ChromaDB).

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Agent áp dụng đúng quy trình RAG: Đầu tiên, gọi `self.store.search(question, top_k)` để lấy ra các chunks sát nghĩa nhất. Kế tiếp, trích xuất chuỗi nội dung (`content`) từ các chunk này, nối chúng lại với nhau bằng dấu phân cách (như `\n---\n`) để làm ngữ cảnh. Cuối cùng, tôi tạo một prompt rõ ràng với cấu trúc: "Dựa vào ngữ cảnh sau: {context}, hãy trả lời câu hỏi: {question}", rồi truyền vào mô hình ngôn ngữ (`llm_fn`) để sinh câu trả lời tự nhiên.

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
====================================== test session starts ======================================
platform linux -- Python 3.10.12, pytest-9.1.1, pluggy-1.6.0 -- /home/kah/vinai/K4-DAY07-HoangTrungKhai-2A202602947/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/kah/vinai/K4-DAY07-HoangTrungKhai-2A202602947
plugins: anyio-4.15.1
collected 42 items                                                                              

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED     [  2%]
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED              [  4%]
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED       [  7%]
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED        [  9%]
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED             [ 11%]
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED [ 14%]
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED   [ 16%]
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED    [ 19%]
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED  [ 21%]
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED                    [ 23%]
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED    [ 26%]
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED               [ 28%]
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED           [ 30%]
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED                     [ 33%]
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED [35%]
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED [ 38%]
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED[ 40%]
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED [ 42%]
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED                    [ 45%]
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED      [ 47%]
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED        [ 50%]
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED              [ 52%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED   [ 54%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED     [ 57%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED [ 59%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED      [ 61%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED               [ 64%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED              [ 66%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED         [ 69%]
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED     [ 71%]
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED [ 73%]
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED    [ 76%]
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED          [ 78%]
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED    [ 80%]
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED [ 83%]
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED [ 85%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED [ 88%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED [ 90%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED [ 92%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED [ 95%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED [ 97%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED [100%]

====================================== 42 passed in 1.39s =======================================

```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | "GPA tối thiểu để duy trì học bổng toàn phần là 3.6/4.0." | "Để không bị cắt học bổng 100%, sinh viên phải giữ điểm tổng kết từ 3.6 trở lên." | cao | 0.89 | Có|
| 2 | "Mức hỗ trợ của học bổng Vượt Khó là 2.000.000 VNĐ mỗi tháng." | "Hạn chót nộp hồ sơ xin xác nhận vay vốn ngân hàng là ngày 15/10." | thấp | 0.58 | Không|
| 3 | "Học bổng Khuyến khích học tập dành cho sinh viên năm nhất." | "Học bổng Khuyến khích học tập không dành cho sinh viên năm nhất." | cao | 0.93 | Có |
| 4 | "Sinh viên thuộc diện hộ nghèo sẽ được hỗ trợ toàn bộ học phí." | "Nhà trường miễn 100% học phí cho các bạn có hoàn cảnh đặc biệt khó khăn." | cao | 0.83 | Có |
| 5 | "Sinh viên vi phạm kỷ luật sẽ bị tước quyền xét học bổng." | "Quyền xét học bổng của sinh viên sẽ bị tước nếu vi phạm kỷ luật." | cao | 0.98 | Có |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> *Viết 2-3 câu:*
> Câu 2: Dù gần như có vẻ không liên quan đến nhau nhưng consine similariity lại khá cao.
> Câu 3: Không bất ngờ nhưng đáng nói là dù hai câu có ý nghĩa trái ngược nhau hoàn toàn về mặt logic (phủ định bằng từ "không") nhưng điểm Cosine Similarity lại cực kỳ cao. Có thể giải thích bằng việc gần như toàn bộ nộ dung gần giống nhau, hay phản ánh rõ ràng rằng Embedding đang có xu hướng biểu diễn topic hoặc lexical overlap tốt hơn là biểu diễn logic ngữ nghĩa thực tế.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. (Áp dụng chiến lược `MarkdownHeadingChunker` và có gán `metadata_filter`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Mức hỗ trợ tài chính hàng tháng cao nhất dành cho chương trình tài năng theo NĐ 179 tại ĐHKHTN là bao nhiêu? | `## Mức hỗ trợ tài chính`... Mức hỗ trợ tài chính hàng tháng cao nhất là 5.500.000 đồng/tháng dành riêng cho sinh viên... | **2** | Có | Mức hỗ trợ tài chính hàng tháng cao nhất là 5.500.000 đồng/tháng. |
| 2 | Sinh viên VNU-IS cần đáp ứng tiêu chuẩn chung nào để được đăng ký các học bổng ngắn hạn? | `## Tiêu chuẩn chung học bổng ngắn hạn`... GPA đạt loại Giỏi trở lên (>= 3.2), điểm rèn luyện loại Tốt... | **2** | Có | Cần có GPA đạt từ 3.2 trở lên (loại Giỏi), rèn luyện loại Tốt và không bị kỷ luật. |
| 3 | Điều kiện về điểm thi THPT để nhận Học bổng NĐ 179/2026 tại ĐHKHTN là gì? | `## Điều kiện điểm thi THPT`... Tổng điểm môn Toán và 2 môn khác đạt từ 22,50/30 điểm trở lên... | **1** | Có | Yêu cầu tổng điểm Toán và 2 môn tổ hợp đạt từ 22,50/30 trở lên và lọt top 30% điểm cao nhất. |
| 4 | Quỹ Thắp sáng niềm tin trong Cẩm nang VNU-ULIS trao tặng bao nhiêu tiền cho mỗi suất học bổng? | `## Quỹ học bổng Thắp sáng niềm tin`... Quỹ học bổng trao 12.000.000 VNĐ/học bổng cho mỗi sinh viên trúng tuyển... | **2** | Có | Quỹ trao tặng 12.000.000 VNĐ/học bổng cho mỗi sinh viên. |
| 5 | VNU-IS phân loại hệ thống học bổng dành cho sinh viên thành những nhóm nguồn chính nào? | `## Hệ thống học bổng`... Hệ thống học bổng VNU-IS gồm 3 nhóm chính: 1) NSNN; 2) Tài trợ; 3) Khó khăn... | **2** | Có | Hệ thống gồm 3 nhóm: 1) Ngân sách nhà nước, 2) Tài trợ doanh nghiệp, 3) Hỗ trợ hoàn cảnh khó khăn. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** **5** / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Qua demo so sánh với bạn Dương (dùng `SentenceChunker`), tôi nhận ra điểm yếu chí mạng của chiến lược `MarkdownHeading` của mình: Nó chỉ thực sự tỏa sáng khi tài liệu gốc được viết chuẩn định dạng Markdown. Nếu đưa vào một văn bản thuần túy (như file `.txt` không có `#`), thuật toán của tôi sẽ bị biến thành một cục text khổng lồ và đánh mất hoàn toàn khả năng chia nhỏ, trong khi `SentenceChunker` hay `RecursiveChunker` của các bạn lại xử lý rất an toàn trường hợp này. Do đó, cần có cơ chế "fallback" (dự phòng) giữa các thuật toán.
---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 9 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 4 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 9 / 10 |
| **Tổng phần cá nhân** | **/ 60** |
