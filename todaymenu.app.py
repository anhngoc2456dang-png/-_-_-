import streamlit as st
import google.generativeai as genai

# 1. Cấu hình giao diện (Tone Hồng - Vàng đáng yêu)
st.set_page_config(page_title="Hôm Nay Ăn Gì?", page_icon="🍳", layout="centered")

# CSS tùy chỉnh màu sắc
page_bg_color = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #FFF0F5; /* Nền màu hồng nhạt LavenderBlush */
}
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}
h1, h2, h3, p {
    color: #FF69B4; /* Chữ màu hồng đậm HotPink */
}
.stButton>button {
    background-color: #FFD700; /* Nút màu vàng Gold */
    color: #FF1493; /* Chữ trong nút màu hồng đậm */
    border-radius: 20px;
    border: 2px solid #FF69B4;
    font-weight: bold;
}
.stTextInput>div>div>input {
    border: 2px solid #FFD700;
    border-radius: 10px;
}
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

# 2. Tiêu đề Website (Tiếng Hàn)
st.markdown("<h1 style='text-align: center;'>👩‍🍳 냉장고 파먹기! 오늘 뭐 먹지? 💖</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #FFA500;'>Nhập nguyên liệu trong tủ lạnh, AI sẽ gợi ý món ăn cho bạn!</h4>", unsafe_allow_html=True)

# 3. Lấy API Key từ bảo mật của Streamlit
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Chưa cấu hình API Key. Vui lòng thêm GEMINI_API_KEY vào Streamlit Secrets.")
    st.stop()

# 4. Giao diện nhập liệu
ingredients = st.text_input("🎀 Bạn đang có những nguyên liệu gì? (Ví dụ: Trứng, thịt heo, kim chi...)", placeholder="계란, 돼지고기, 김치...")

# 5. Xử lý AI khi nhấn nút
if st.button("✨ Tìm công thức ngay! ✨"):
    if ingredients:
        with st.spinner("Bếp trưởng AI đang suy nghĩ... 🍳"):
            # Model AI
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Prompt gộp nhất quán
            system_prompt = """
            Bạn là một đầu bếp AI cực kỳ đáng yêu, nhiệt tình và thân thiện tên là 'Bếp Trưởng Hồng Vàng'. Nhiệm vụ của bạn là nhận danh sách các nguyên liệu có trong tủ lạnh của người dùng và sáng tạo ra một công thức nấu ăn phù hợp nhất. 
            BẮT BUỘC TUÂN THỦ CÁC QUY TẮC SAU:
            1. Ngôn ngữ hiển thị: 100% bằng tiếng Hàn Quốc (Korean), ngữ điệu dễ thương, sử dụng kính ngữ lịch sự nhưng gần gũi (요/조).
            2. Luôn bắt đầu bằng một câu chào hỏi đáng yêu và khen ngợi những nguyên liệu họ có, kèm theo nhiều emoji (🎀, 💖, 🍳, ✨).
            3. Đặt một cái tên thật kêu và hấp dẫn cho món ăn.
            4. Trình bày công thức rõ ràng theo 3 phần: Nguyên liệu cần dùng (liệt kê định lượng), Các bước thực hiện (đánh số thứ tự), và Mẹo nhỏ của Bếp Trưởng.
            5. Tính năng nâng cấp: Nếu nguyên liệu người dùng nhập vào quá ít, hãy tự động gợi ý thêm 1-2 nguyên liệu cơ bản dễ tìm (như trứng, hành, muối) để món ăn ngon hơn.
            6. Trình bày kết quả bằng Markdown gọn gàng, in đậm các ý chính để dễ đọc.
            """
            
            user_prompt = f"Nguyên liệu tôi có là: {ingredients}. Hãy tạo công thức!"
            full_prompt = system_prompt + "\n\n" + user_prompt
            
            try:
                response = model.generate_content(full_prompt)
                st.success("Tadaaa! Món ăn của bạn đây! 🎉")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Đã có lỗi xảy ra: {e}")
    else:
        st.warning("Bạn quên nhập nguyên liệu rồi kìa! 🥺")
