import streamlit as st
from PIL import Image
from io import BytesIO
from collections import Counter
import colorsys

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="CHARA:VERSE",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# STYLE
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Noto+Sans+KR:wght@400;500;600;700&display=swap');

    :root {
        --bg: #101116;
        --panel: #191a22;
        --panel-light: #22232d;
        --border: #353541;
        --text: #f1f0f7;
        --muted: #9293a5;
        --accent: #c77dff;
    }

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 15% 0%, #272038 0%, transparent 36%),
            #101116;
        color: var(--text);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--text);
    }

    .brand {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.7rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: #f6f1ff;
    }

    .brand span {
        color: var(--accent);
    }

    .eyebrow {
        color: var(--accent);
        font-family: 'Orbitron', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 0.18em;
        margin-bottom: 0.5rem;
    }

    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(2.2rem, 5vw, 4.2rem);
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.04em;
        margin: 0;
    }

    .hero-title span {
        color: var(--accent);
    }

    .subtitle {
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.8;
        margin-top: 1rem;
    }

    .section-label {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.75rem;
        letter-spacing: 0.14em;
        color: var(--accent);
        margin-bottom: 0.5rem;
    }

    .panel {
        background: linear-gradient(145deg, #1b1c25, #15161d);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    .panel-title {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.85rem;
        color: #f5f2ff;
    }

    .tag {
        display: inline-block;
        border: 1px solid #63417d;
        color: #dfb7ff;
        background: #2a2035;
        border-radius: 4px;
        padding: 0.25rem 0.55rem;
        margin: 0.15rem 0.2rem 0.15rem 0;
        font-size: 0.75rem;
    }

    .quote {
        color: #d6c4e9;
        border-left: 3px solid var(--accent);
        padding: 0.6rem 0.9rem;
        background: #201b29;
        font-style: italic;
    }

    .small-muted {
        color: var(--muted);
        font-size: 0.8rem;
    }

    .divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1.5rem 0;
    }

    div[data-testid="stFileUploader"] {
        background: #191a22;
        border: 1px dashed #51435f;
        border-radius: 8px;
        padding: 0.7rem;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 5px;
        font-weight: 700;
        min-height: 2.8rem;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background: #191a22;
        color: #f1f0f7;
        border-color: #353541;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background: #191a22;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# HELPERS
# -----------------------------
def extract_accent(image: Image.Image) -> str:
    """이미지에서 대표 색상을 추출한다."""
    sample = image.convert("RGB")
    sample.thumbnail((100, 100))

    colors = sample.quantize(colors=8).convert("RGB").getcolors(10000)

    if not colors:
        return "#C77DFF"

    # 지나치게 어둡거나 밝은 색상을 제외한다.
    candidates = []

    for count, rgb in colors:
        r, g, b = [v / 255 for v in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        if 0.18 < v < 0.92 and s > 0.18:
            candidates.append((count, rgb))

    if not candidates:
        return "#C77DFF"

    _, chosen = max(candidates, key=lambda item: item[0])

    return "#{:02X}{:02X}{:02X}".format(*chosen)


# -----------------------------
# HEADER
# -----------------------------
header_left, header_right = st.columns([3, 2])

with header_left:
    st.markdown(
        '<div class="brand">CHARA<span>:</span>VERSE</div>',
        unsafe_allow_html=True,
    )
    st.caption("CHARACTER DATABASE  /  WORLD-BUILDING SYSTEM")

with header_right:
    menu1, menu2, menu3 = st.columns(3)

    with menu1:
        st.markdown(
            '<div class="small-muted">01 / CREATE</div>',
            unsafe_allow_html=True,
        )
    with menu2:
        st.markdown(
            '<div class="small-muted">02 / DATABASE</div>',
            unsafe_allow_html=True,
        )
    with menu3:
        st.markdown(
            '<div class="small-muted">03 / WORLD</div>',
            unsafe_allow_html=True,
        )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# -----------------------------
# HERO
# -----------------------------
st.markdown(
    '<div class="eyebrow">YOUR UNIVERSE STARTS HERE</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 class="hero-title">CREATE YOUR<br><span>OWN UNIVERSE.</span></h1>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p class="subtitle">
    캐릭터를 기록하고, 설정을 확장하고, 나만의 세계관을 구축하세요.<br>
    당신의 상상 속 인물이 하나의 데이터베이스가 됩니다.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# -----------------------------
# MAIN CONTENT
# -----------------------------
left, right = st.columns([1, 1.15], gap="large")

with left:
    st.markdown(
        '<div class="section-label">01 / VISUAL DATA</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### CHARACTER IMAGE")
    st.markdown(
        '<p class="small-muted">캐릭터 이미지를 업로드하세요.</p>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "캐릭터 이미지 선택",
        type=["png", "jpg", "jpeg", "webp"],
        help="PNG, JPG, JPEG, WEBP 파일을 지원합니다.",
    )

    character_image = None
    accent_color = "#C77DFF"

    if uploaded_file is not None:
        try:
            character_image = Image.open(uploaded_file).convert("RGB")
            accent_color = extract_accent(character_image)

            st.image(
                character_image,
                use_container_width=True,
            )

            st.markdown(
                f"""
                <div class="panel">
                    <div class="panel-title">VISUAL ANALYSIS</div>
                    <span class="small-muted">DETECTED ACCENT COLOR</span><br>
                    <div style="
                        display:flex;
                        align-items:center;
                        gap:12px;
                        margin-top:10px;
                    ">
                        <div style="
                            width:32px;
                            height:32px;
                            border-radius:5px;
                            background:{accent_color};
                            border:1px solid #ffffff55;
                        "></div>
                        <span>{accent_color}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        except Exception:
            st.error("이미지를 읽을 수 없습니다. 다른 파일을 선택해 주세요.")

    else:
        st.markdown(
            """
            <div class="panel" style="
                min-height:280px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                text-align:center;
                border-style:dashed;
            ">
                <div style="font-size:3rem;color:#71617f;">✦</div>
                <div class="panel-title">NO IMAGE DETECTED</div>
                <div class="small-muted">
                    업로드한 이미지가 이곳에 표시됩니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with right:
    st.markdown(
        '<div class="section-label">02 / CHARACTER DATA</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### CHARACTER PROFILE")
    st.markdown(
        '<p class="small-muted">기본 정보를 입력해 프로필을 구성하세요.</p>',
        unsafe_allow_html=True,
    )

    with st.form("character_form"):
        character_name = st.text_input(
            "캐릭터 이름 *",
            placeholder="예: NOCT",
        )

        codename = st.text_input(
            "별명 / 코드네임",
            placeholder="예: 기억 수집자",
        )

        col1, col2 = st.columns(2)

        with col1:
            age = st.text_input(
                "나이",
                placeholder="예: 24",
            )

        with col2:
            species = st.text_input(
                "종족",
                placeholder="예: 인간",
            )

        personality = st.text_input(
            "성격 키워드",
            placeholder="예: 냉소적, 신중함, 관찰력이 좋음",
        )

        col3, col4 = st.columns(2)

        with col3:
            affiliation = st.text_input(
                "소속",
                placeholder="예: 방랑자 집단",
            )

        with col4:
            occupation = st.text_input(
                "직업 / 역할",
                placeholder="예: 정찰병",
            )

        genre = st.selectbox(
            "세계관 장르",
            [
                "Cyberpunk",
                "Post-Apocalyptic",
                "Sci-Fi",
                "Dark Fantasy",
                "Modern",
                "Other",
            ],
        )

        background = st.text_area(
            "배경 이야기",
            placeholder="이 캐릭터는 어떤 삶을 살아왔나요?",
            height=100,
        )

        goal = st.text_input(
            "목표",
            placeholder="캐릭터가 이루고 싶은 것은?",
        )

        abilities = st.text_input(
            "능력 / 특기",
            placeholder="캐릭터가 잘하는 것",
        )

        weakness = st.text_input(
            "약점",
            placeholder="캐릭터가 가진 한계",
        )

        quote = st.text_input(
            "대표 대사",
            placeholder="캐릭터를 가장 잘 나타내는 한마디",
        )

        submitted = st.form_submit_button(
            "GENERATE CHARACTER PROFILE",
            type="primary",
            use_container_width=True,
        )

# -----------------------------
# PROFILE PREVIEW
# -----------------------------
if submitted:
    if not character_name.strip():
        st.error("캐릭터 이름을 입력해 주세요.")

    elif character_image is None:
        st.error("캐릭터 이미지를 업로드해 주세요.")

    else:
        st.session_state["current_character"] = {
            "name": character_name.strip(),
            "codename": codename.strip(),
            "age": age.strip(),
            "species": species.strip(),
            "personality": personality.strip(),
            "affiliation": affiliation.strip(),
            "occupation": occupation.strip(),
            "genre": genre,
            "background": background.strip(),
            "goal": goal.strip(),
            "abilities": abilities.strip(),
            "weakness": weakness.strip(),
            "quote": quote.strip(),
            "accent_color": accent_color,
        }

        buffer = BytesIO()
        character_image.save(buffer, format="PNG")

        st.session_state["current_image_bytes"] = buffer.getvalue()

        st.session_state["profile_ready"] = True

if st.session_state.get("profile_ready", False):
    character = st.session_state["current_character"]
    image_bytes = st.session_state["current_image_bytes"]
    accent = character["accent_color"]

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">03 / CHARACTER DOSSIER</div>',
        unsafe_allow_html=True,
    )
    st.markdown("## GENERATED PROFILE")

    profile_left, profile_right = st.columns([0.9, 1.4], gap="large")

    with profile_left:
        st.image(image_bytes, use_container_width=True)

        st.markdown(
            f"""
            <div class="panel" style="border-top:3px solid {accent};">
                <div class="eyebrow">CHARACTER IDENTIFIED</div>
                <div style="
                    font-size:2rem;
                    font-weight:800;
                    line-height:1.2;
                    overflow-wrap:anywhere;
                ">{character["name"]}</div>
                <div style="color:#aaa3b8;margin-top:8px;">
                    {character["codename"] or "UNREGISTERED CODENAME"}
                </div>
                <hr class="divider">
                <div class="quote">
                    {character["quote"] or "기록된 대표 대사가 없습니다."}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with profile_right:
        def info_panel(title, value):
            safe_value = value if value else "NOT SPECIFIED"

            st.markdown(
                f"""
                <div class="panel" style="border-left:3px solid {accent};">
                    <div class="eyebrow">{title}</div>
                    <div style="overflow-wrap:anywhere;white-space:pre-wrap;">
                        {safe_value}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        info1, info2 = st.columns(2)

        with info1:
            info_panel(
                "BASIC INFO",
                f"AGE: {character['age'] or '-'}\n"
                f"SPECIES: {character['species'] or '-'}",
            )
            info_panel(
                "PERSONALITY",
                character["personality"],
            )
            info_panel(
                "ABILITIES",
                character["abilities"],
            )

        with info2:
            info_panel(
                "AFFILIATION",
                f"{character['affiliation'] or '-'}\n"
                f"ROLE: {character['occupation'] or '-'}",
            )
            info_panel(
                "WORLD SETTING",
                character["genre"],
            )
            info_panel(
                "WEAKNESS",
                character["weakness"],
            )

        info_panel(
            "BACKGROUND / LORE",
            character["background"],
        )

        info_panel(
            "CURRENT OBJECTIVE",
            character["goal"],
        )

    export_data = dict(character)

    st.download_button(
        "DOWNLOAD CHARACTER DATA (JSON)",
        data=__import__("json").dumps(
            export_data,
            ensure_ascii=False,
            indent=2,
        ),
        file_name=f"{character['name']}_profile.json",
        mime="application/json",
        use_container_width=True,
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align:center;padding:1rem 0;">
        <div class="brand" style="font-size:1.1rem;">
            CHARA<span>:</span>VERSE
        </div>
        <div class="small-muted" style="margin-top:0.5rem;">
            CHARACTER CREATION & WORLD-BUILDING SYSTEM
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
