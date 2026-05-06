import streamlit as st

def render_titulo():
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500&display=swap" rel="stylesheet">

    <style>
      .title-wrapper {
        text-align: center;
        padding: 1.5rem 1rem 0.5rem;
      }

      .title-main {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: clamp(2rem, 5vw, 3.2rem);
        line-height: 1.15;
        letter-spacing: -0.02em;
        background: linear-gradient(
          90deg,
          #ff6a00 0%,
          #ff9a3c 30%,
          #ffcc70 55%,
          #ff9a3c 75%,
          #ff6a00 100%
        );
        background-size: 250% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 3s linear infinite, fadeSlideIn 0.8s ease-out both;
        margin: 0;
      }

      .title-sub {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: clamp(0.75rem, 1.5vw, 0.9rem);
        color: rgba(255, 160, 60, 0.55);
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-top: 0.4rem;
        animation: fadeSlideIn 0.8s ease-out 0.3s both;
      }

      .comma {
        -webkit-text-fill-color: rgba(255, 150, 50, 0.45);
      }

      .dot-pulse {
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #ff8c00;
        margin-left: 5px;
        vertical-align: middle;
        margin-bottom: 3px;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 0 8px #ff8c00, 0 0 16px #ff6a0066;
      }

      .title-line {
        display: block;
        height: 3px;
        background: linear-gradient(90deg, #ff6a00, #ffcc70);
        border-radius: 99px;
        margin: 0.7rem auto 0;
        animation: expandLine 0.8s ease-out 0.5s both;
      }

      @keyframes shimmer {
        0%   { background-position: 0% center; }
        100% { background-position: 250% center; }
      }

      @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
      }

      @keyframes pulse {
        0%, 100% { transform: scale(1);   opacity: 1; }
        50%       { transform: scale(1.45); opacity: 0.55; }
      }

      @keyframes expandLine {
        from { width: 0; opacity: 0; }
        to   { width: 60px; opacity: 1; }
      }
    </style>

    <div class="title-wrapper">
      <h1 class="title-main">
        Smartstream<span class="comma">,</span><br>
        seu assistente que aprende<span class="dot-pulse"></span>
      </h1>
      <span class="title-line" style="width:60px;"></span>
      <p class="title-sub">Desenvolvido por Armando Monsão · Analista de sistemas</p>
    </div>
    """, unsafe_allow_html=True)