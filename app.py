import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="포스코홀딩스 최근 실적 업로드 뷰어", layout="centered")
st.title("📊 포스코홀딩스 최근 실적 업로드 뷰어")

st.markdown(
    """
    1) 아래에 **포스코홀딩스_최근실적.xlsx** 파일을 드래그 앤 드롭 또는 'Browse files'로 선택하세요.  
    2) 여러 시트가 있으면 시트를 선택해 볼 수 있습니다.  
    3) 필요하면 CSV로 다시 내려받을 수 있습니다.
    """
)

uploaded = st.file_uploader(
    "엑셀 파일(.xlsx) 업로드", type=["xlsx"], accept_multiple_files=False
)

if uploaded is not None:
    try:
        xls = pd.read_excel(uploaded, sheet_name=None)
        sheet_names = list(xls.keys())
        sheet = st.selectbox("시트 선택", sheet_names, index=0)

        df = xls[sheet]
        st.subheader(f"시트 미리보기: {sheet}")
        st.dataframe(df, use_container_width=True)

        with st.expander("기본 통계 보기"):
            st.write(df.describe(include="all"))

        csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="현재 시트 CSV로 다운로드",
            data=csv_bytes,
            file_name=f"{sheet}.csv",
            mime="text/csv",
        )

        uploaded.seek(0)
        st.download_button(
            label="원본 엑셀 다시 다운로드",
            data=uploaded.read(),
            file_name=uploaded.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.info("엑셀 파일을 업로드하면 내용이 여기에 표시됩니다.")
