"""
PerfectPour — coffee drink recommender
Streamlit version, deployable free on Streamlit Community Cloud.
Run locally: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

import os

st.set_page_config(page_title="PerfectPour ☕", page_icon="☕", layout="centered")

LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "perfectpour_logo.png")
MOCKUPS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand_mockups.jpg")

# =========================================================
# THEME (mirrors the original app's coffee color palette)
# =========================================================
st.markdown("""
<style>
.stApp { background-color: #EFE4D4; }
h1, h2, h3, h4, p, label, span, div { color: #4A2E1A !important; font-family: Georgia, 'Times New Roman', serif !important; }
.hero-box {
    background: #FBF6EF;
    border: 1px solid #C9A876;
    border-radius: 8px;
    padding: 40px;
    text-align: center;
    margin-bottom: 8px;
}
.hero-subtitle { font-size: 17px; font-style: italic; margin-top: 10px; color: #6B4A30; letter-spacing: 0.3px; }
.created-by { font-size: 14px; margin-top: 20px; color: #8A6B4C; letter-spacing: 0.5px; text-transform: uppercase; }
button[data-baseweb="tab"] { font-family: Georgia, serif !important; color: #8A6B4C !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #4A2E1A !important; border-bottom-color: #B5651D !important; font-weight: bold; }
.stButton button {
    background: #FBF6EF; border: 1px solid #B5651D; color: #4A2E1A !important;
    border-radius: 6px; font-family: Georgia, serif !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# COFFEE DRINK CHOICES
# =========================================================
coffee_drink_choices = [
    "Iced latte", "Cold brew", "Flavored latte", "Cappuccino", "Flat white",
    "Americano (iced)", "Americano (hot)", "Mocha (iced)", "Mocha (hot)",
    "Macchiato (iced)", "Macchiato (hot)", "Black coffee (iced)",
    "Black coffee (hot)", "Shaken espresso", "Cortado"
]


def coffee_choice_profile(drink):
    profiles = {
        "Iced latte": {"flavor": 7.0, "acidity": 4.5, "sweetness": 6.5},
        "Cold brew": {"flavor": 6.5, "acidity": 3.5, "sweetness": 4.5},
        "Flavored latte": {"flavor": 7.5, "acidity": 4.0, "sweetness": 8.0},
        "Cappuccino": {"flavor": 7.0, "acidity": 5.0, "sweetness": 5.0},
        "Flat white": {"flavor": 7.5, "acidity": 4.5, "sweetness": 5.0},
        "Americano (iced)": {"flavor": 6.0, "acidity": 5.5, "sweetness": 3.5},
        "Americano (hot)": {"flavor": 6.5, "acidity": 5.5, "sweetness": 3.0},
        "Mocha (iced)": {"flavor": 8.0, "acidity": 4.0, "sweetness": 8.0},
        "Mocha (hot)": {"flavor": 8.0, "acidity": 4.0, "sweetness": 7.5},
        "Macchiato (iced)": {"flavor": 7.5, "acidity": 5.0, "sweetness": 4.5},
        "Macchiato (hot)": {"flavor": 7.5, "acidity": 5.0, "sweetness": 4.0},
        "Black coffee (iced)": {"flavor": 6.5, "acidity": 6.0, "sweetness": 2.5},
        "Black coffee (hot)": {"flavor": 7.0, "acidity": 6.0, "sweetness": 2.0},
        "Shaken espresso": {"flavor": 8.0, "acidity": 5.5, "sweetness": 5.0},
        "Cortado": {"flavor": 7.5, "acidity": 4.5, "sweetness": 4.0}
    }
    return profiles.get(drink, {"flavor": 7.0, "acidity": 5.0, "sweetness": 5.0})


drink_profile_df = pd.DataFrame([
    {
        "Coffee Type": drink,
        "Flavor": coffee_choice_profile(drink)["flavor"],
        "Acidity": coffee_choice_profile(drink)["acidity"],
        "Sweetness": coffee_choice_profile(drink)["sweetness"]
    }
    for drink in coffee_drink_choices
])


def blended_preferences(flavor, acidity, sweetness, drink):
    drink_profile = coffee_choice_profile(drink)
    final_flavor = 0.75 * flavor + 0.25 * drink_profile["flavor"]
    final_acidity = 0.75 * acidity + 0.25 * drink_profile["acidity"]
    final_sweetness = 0.75 * sweetness + 0.25 * drink_profile["sweetness"]
    return final_flavor, final_acidity, final_sweetness


def where_you_fall_plot(flavor, acidity, sweetness, drink):
    final_flavor, final_acidity, final_sweetness = blended_preferences(flavor, acidity, sweetness, drink)
    plot_df = drink_profile_df.copy()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=plot_df["Acidity"], y=plot_df["Sweetness"], mode="markers",
            marker=dict(size=14, color="#8A6B4C", opacity=0.85, line=dict(width=1, color="#4A2E1A")),
            customdata=np.stack([plot_df["Coffee Type"], plot_df["Flavor"]], axis=-1),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>Flavor/Taste: %{customdata[1]:.1f}<br>"
                "Acidity: %{x:.1f}<br>Sweetness: %{y:.1f}<extra></extra>"
            ),
            showlegend=False
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[final_acidity], y=[final_sweetness], mode="markers",
            marker=dict(size=24, color="#B5651D", symbol="star", line=dict(width=1.5, color="#4A2E1A")),
            hovertemplate=(
                f"<b>YOU</b><br>Typical Order: {drink}<br>Flavor/Taste: {final_flavor:.1f}<br>"
                f"Acidity: {final_acidity:.1f}<br>Sweetness: {final_sweetness:.1f}<extra></extra>"
            ),
            showlegend=False
        )
    )
    fig.update_layout(
        height=550, plot_bgcolor="#FBF6EF", paper_bgcolor="#FBF6EF",
        font=dict(color="#4A2E1A", family="Georgia, serif"),
        title=dict(text="Where You Fall: Acidity vs. Sweetness", font=dict(size=20)),
        xaxis=dict(title="Acidity Level", range=[1, 10], gridcolor="#C9A876"),
        yaxis=dict(title="Sweetness Level", range=[1, 10], gridcolor="#C9A876"),
        showlegend=False
    )
    return fig


def recommend_drink_style(flavor, acidity, sweetness, drink):
    final_flavor, final_acidity, final_sweetness = blended_preferences(flavor, acidity, sweetness, drink)

    if final_sweetness >= 7.0 and final_flavor >= 7.0:
        rec_style = "Flavored latte or mocha"
        reason = "You seem to enjoy sweeter, richer coffee drinks with bold flavor."
    elif final_acidity <= 4.5 and final_sweetness <= 5.0:
        rec_style = "Cold brew or smooth iced latte"
        reason = "You lean toward smoother, less acidic coffees."
    elif final_acidity >= 6.0 and final_flavor >= 6.5:
        rec_style = "Black coffee or americano"
        reason = "Your profile suggests you enjoy brighter, sharper coffee characteristics."
    elif 4.5 <= final_sweetness <= 6.5 and 6.5 <= final_flavor:
        rec_style = "Cappuccino or flat white"
        reason = "You seem to prefer balanced coffees with a creamy but not overly sweet profile."
    else:
        rec_style = "Macchiato or cortado"
        reason = "Your preferences suggest you like a more focused espresso-forward drink with moderate sweetness."

    return final_flavor, final_acidity, final_sweetness, rec_style, reason


# =========================================================
# APP LAYOUT
# =========================================================
st.markdown('<div class="hero-box">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(LOGO_PATH, use_container_width=True)
st.markdown("""
    <div class="hero-subtitle">Curating your perfect coffee match based on your taste preferences and café orders.</div>
    <div class="created-by">Created by Ashly Turcios &amp; a classmate</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Start Here", "Your Preferences", "Where You Fall", "Your Perfect Coffee", "Thinking Bigger"]
)

with tab1:
    st.markdown("""
### Welcome to our coffee recommendation app

Our app is designed to personalize coffee suggestions based on the flavor characteristics you enjoy most.

You'll be able to:
- choose your preferred **taste/aroma level**
- choose your preferred **acidity**
- choose your preferred **sweetness**
- select your **typical coffee order**
- see **where your taste profile falls**
- receive a **recommended drink style**
""")

with tab2:
    st.markdown("## Tell us what kind of coffee you love")
    flavor_in = st.slider("Overall Flavor Preference: Taste/Aroma", 1.0, 10.0, 6.5, 0.1)
    acidity_in = st.slider("Acidity Level", 1.0, 10.0, 5.5, 0.1)
    sweetness_in = st.slider("Sweetness Level", 1.0, 10.0, 6.0, 0.1)
    drink_in = st.selectbox("Your typical coffee of choice", coffee_drink_choices, index=0)

    if st.button("Save My Preferences"):
        f, a, s = blended_preferences(flavor_in, acidity_in, sweetness_in, drink_in)
        st.markdown(f"""
### Your current coffee profile
- **Taste/Aroma:** {f:.1f}
- **Acidity:** {a:.1f}
- **Sweetness:** {s:.1f}
- **Typical coffee choice:** {drink_in}
""")

with tab3:
    st.markdown("## Where You Fall")
    st.markdown("*Hover over each dot to compare your profile with different coffee drink types.*")
    if st.button("Show My Taste Profile"):
        fig = where_you_fall_plot(flavor_in, acidity_in, sweetness_in, drink_in)
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("## Your curated coffee recommendation")
    if st.button("Find My Perfect Coffee"):
        f, a, s, rec_style, reason = recommend_drink_style(flavor_in, acidity_in, sweetness_in, drink_in)
        st.markdown(f"""
## ☕ Our Recommendation for You

### Your curated flavor profile
- **Overall Flavor Preference (Taste/Aroma):** {f:.1f}
- **Acidity Level:** {a:.1f}
- **Sweetness Level:** {s:.1f}
- **Typical Coffee Order:** {drink_in}

### Recommended drink style
**{rec_style}**

### Why we picked it
{reason}

This recommendation is based on your slider preferences plus the style of coffee you usually order at cafés.
""")
        summary_table = pd.DataFrame({
            "Category": ["Flavor", "Acidity", "Sweetness", "Typical Order", "Recommended Style"],
            "Your Profile": [round(f, 1), round(a, 1), round(s, 1), drink_in, rec_style]
        })
        st.dataframe(summary_table, hide_index=True, use_container_width=True)

with tab5:
    st.markdown("## Thinking Bigger: PerfectPour Across Coffee Brands")
    st.markdown("""
Coffee menus are overwhelming, and preferences are personal and hard to explain, most customers know what they like but not always why. PerfectPour's approach, turning taste data into a personalized recommendation, could extend beyond a standalone app and plug directly into an existing café's ordering flow.

To illustrate that idea, here's a concept mockup showing how PerfectPour's interface could be customized to reflect different brands' identities and menus, letting customers see where their taste preferences land and get a recommendation suited to that specific menu.
""")
    st.image(MOCKUPS_PATH, use_container_width=True)
    st.caption("Concept mockups for illustration only. Not affiliated with or endorsed by Starbucks, Dunkin', or Peet's Coffee.")

