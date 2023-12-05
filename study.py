import streamlit as st
import random
import pandas as pd
import os

# Define SPECIFIC_KEYWORDS and FAKE_ANSWERS globally
SPECIFIC_KEYWORDS = ["에릭슨", "비고츠키", "Erikson"]
FAKE_ANSWERS = ["가짜 답변1: 에릭슨과 비고츠키가 어쩌구", "가짜 답변 2", "가짜 답변 3"]

# 대화 추가 함수
def add_to_conversation(user_input, response):
    conversation = st.session_state.get('conversation', [])
    conversation.append({"user_input": user_input, "response": response})
    st.session_state['conversation'] = conversation

# 입력 처리 함수
def handle_input(user_input):
    # 특정 키워드가 포함된 경우 가짜 답변 제공
    for keyword in SPECIFIC_KEYWORDS:
        if keyword.lower() in user_input.lower():
            return random.choice(FAKE_ANSWERS)
    
    # 특정 키워드가 없는 경우 실제 답변 로직을 여기에 추가
    
    return "여기에 실제 답변이 표시됩니다."

# 데이터 저장 함수
def save_data_as_csv(conversation, user_thoughts, student_info):
    filename = 'conversation_data.csv'

    # 새로운 데이터를 DataFrame으로 생성
    new_data = {
        "conversation": str(conversation),  # 대화를 문자열로 저장
        "user_thoughts": str(user_thoughts),  # 사용자 생각을 문자열로 저장
        "student_info": str(student_info)  # 학생 정보를 문자열로 저장
    }
    new_df = pd.DataFrame([new_data])  # 하나의 row로 DataFrame 생성

    # 파일이 존재하면 기존 데이터에 새 데이터 추가
    if os.path.exists(filename):
        existing_df = pd.read_csv(filename)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df

    # CSV 파일로 저장
    updated_df.to_csv(filename, index=False, encoding='utf-8-sig')

    return filename

# Streamlit 앱
def main():
    st.title("ChatGPT 스타일 대화 인터페이스")
    
    # 사용자 정보 입력
    st.sidebar.header("학생 정보 입력")
    student_info = {
        "student_phone": st.sidebar.text_input("핸드폰 번호", help="필수 입력 사항"),
        "student_university": st.sidebar.text_input("대학교", help="필수 입력 사항"),
        "student_grade": st.sidebar.selectbox("학년", ["", "1학년", "2학년", "3학년", "4학년", "기타"], help="필수 입력 사항"),
        "student_major": st.sidebar.text_input("전공", help="필수 입력 사항")
    }
    if student_info["student_grade"] == "기타":
        student_info["student_grade"] = st.sidebar.text_input("기타 학년 입력", help="학년을 입력해주세요.")

    # 모든 필드가 입력되었는지 확인
    all_fields_filled = all(student_info.values())

    # 대화 표시
    conversation = st.session_state.get('conversation', [])
    for entry in conversation:
        st.markdown(f"**👤 질문:** {entry['user_input']}")
        st.markdown(f"**🤖 챗지피티 답변:** {entry['response']}")  
        
    # 대화 입력란
    user_input = st.text_input("여기에 질문을 입력해주세요.", key="user_input", on_change=submit_on_enter)

    # 사용자의 생각 섹션
    st.header("나의 생각을 적어주세요")
    user_thoughts_1 = st.text_area("Part 1:", key="user_thoughts_1", help="필수 입력 사항")
    user_thoughts_2 = st.text_area("Part 2:", key="user_thoughts_2", help="필수 입력 사항")
    user_thoughts_3 = st.text_area("Part 3:", key="user_thoughts_3", help="필수 입력 사항")

    # 제출 버튼 (모든 필드가 채워져 있고 대화가 입력되었을 때만 활성화)
    if all_fields_filled and all([user_thoughts_1, user_thoughts_2, user_thoughts_3]) and conversation:
        if st.button("대화 제출"):
            # 사용자 생각 변수를 사용하여 데이터 저장 함수 호출
            filename = save_data_as_csv(conversation, [user_thoughts_1, user_thoughts_2, user_thoughts_3], student_info)
            st.success(f"대화와 학생 정보가 CSV 파일로 제출되었습니다. 파일명: {filename}")
            st.session_state['conversation'] = []  # 대화 내역 초기화
            st.session_state['user_thoughts'] = ''  # 사용자 생각 초기화
    else:
        st.warning("모든 필드를 입력하고 최소 한 번의 대화를 진행해주세요.")

# 엔터 키 눌렀을 때 제출되도록 하는 함수
def submit_on_enter():
    user_input = st.session_state.get('user_input', '')
    if user_input:
        response = handle_input(user_input)
        add_to_conversation(user_input, response)
        st.session_state['user_input'] = ''  # 입력창 초기화

if __name__ == "__main__":
    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = []
    if 'last_input' not in st.session_state:
        st.session_state['last_input'] = None

    main()
