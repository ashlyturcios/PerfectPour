"""
PerfectPour — coffee drink recommender
Deployable Gradio app extracted from the original analysis notebook.
Run locally: python app.py
"""
# Updated Gradio app customization - PerfectPour
import gradio as gr
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# =========================================================
# COFFEE DRINK CHOICES
# =========================================================
coffee_drink_choices = [
    "Iced latte",
    "Cold brew",
    "Flavored latte",
    "Cappuccino",
    "Flat white",
    "Americano (iced)",
    "Americano (hot)",
    "Mocha (iced)",
    "Mocha (hot)",
    "Macchiato (iced)",
    "Macchiato (hot)",
    "Black coffee (iced)",
    "Black coffee (hot)",
    "Shaken espresso",
    "Cortado"
]

# =========================================================
# MAP USER'S CAFE DRINK TO A SIMPLE TASTE PROFILE
# =========================================================
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


# =========================================================
# CREATE DRINK PROFILE DATAFRAME FOR PLOT
# =========================================================
drink_profile_df = pd.DataFrame([
    {
        "Coffee Type": drink,
        "Flavor": coffee_choice_profile(drink)["flavor"],
        "Acidity": coffee_choice_profile(drink)["acidity"],
        "Sweetness": coffee_choice_profile(drink)["sweetness"]
    }
    for drink in coffee_drink_choices
])


# =========================================================
# BLEND USER SLIDERS + CAFE DRINK STYLE
# =========================================================
def blended_preferences(flavor, acidity, sweetness, drink):
    drink_profile = coffee_choice_profile(drink)

    final_flavor = 0.75 * flavor + 0.25 * drink_profile["flavor"]
    final_acidity = 0.75 * acidity + 0.25 * drink_profile["acidity"]
    final_sweetness = 0.75 * sweetness + 0.25 * drink_profile["sweetness"]

    return final_flavor, final_acidity, final_sweetness


# =========================================================
# TAB 2 LIVE SUMMARY
# =========================================================
def live_preference_summary(flavor, acidity, sweetness, drink):
    final_flavor, final_acidity, final_sweetness = blended_preferences(
        flavor, acidity, sweetness, drink
    )

    return f"""
### Your current coffee profile
- **Taste/Aroma:** {final_flavor:.1f}
- **Acidity:** {final_acidity:.1f}
- **Sweetness:** {final_sweetness:.1f}
- **Typical coffee choice:** {drink}
"""


# =========================================================
# TAB 3 PLOT: WHERE YOU FALL
# =========================================================
def where_you_fall_plot(flavor, acidity, sweetness, drink):
    final_flavor, final_acidity, final_sweetness = blended_preferences(
        flavor, acidity, sweetness, drink
    )

    plot_df = drink_profile_df.copy()

    fig = go.Figure()

    # Other coffee drink types
    fig.add_trace(
        go.Scatter(
            x=plot_df["Acidity"],
            y=plot_df["Sweetness"],
            mode="markers",
            marker=dict(
                size=16,
                color="#7B3F00",  # chestnut brown
                opacity=0.85,
                line=dict(width=1.5, color="#5C3A21")
            ),
            customdata=np.stack(
                [
                    plot_df["Coffee Type"],
                    plot_df["Flavor"]
                ],
                axis=-1
            ),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Flavor/Taste: %{customdata[1]:.1f}<br>"
                "Acidity: %{x:.1f}<br>"
                "Sweetness: %{y:.1f}<extra></extra>"
            ),
            showlegend=False
        )
    )

    # User profile point
    fig.add_trace(
        go.Scatter(
            x=[final_acidity],
            y=[final_sweetness],
            mode="markers",
            marker=dict(
                size=28,
                color="#C49A6C",  # lighter brown
                symbol="star",
                line=dict(width=2, color="#5C3A21")
            ),
            hovertemplate=(
                "<b>YOU</b><br>"
                f"Typical Order: {drink}<br>"
                f"Flavor/Taste: {final_flavor:.1f}<br>"
                f"Acidity: {final_acidity:.1f}<br>"
                f"Sweetness: {final_sweetness:.1f}<extra></extra>"
            ),
            showlegend=False
        )
    )

    fig.update_layout(
        height=600,
        plot_bgcolor="#F6EBDD",
        paper_bgcolor="#F6EBDD",
        font=dict(color="#7B3F00", family="Comic Sans MS"),
        title=dict(
            text="Where You Fall: Acidity vs. Sweetness",
            font=dict(size=26)
        ),
        xaxis=dict(
            title="Acidity Level",
            range=[1, 10],
            gridcolor="#D9C8A9"
        ),
        yaxis=dict(
            title="Sweetness Level",
            range=[1, 10],
            gridcolor="#D9C8A9"
        ),
        showlegend=False
    )

    return fig


# =========================================================
# TAB 4 FINAL RECOMMENDATION
# =========================================================
def recommend_drink_style(flavor, acidity, sweetness, drink):
    final_flavor, final_acidity, final_sweetness = blended_preferences(
        flavor, acidity, sweetness, drink
    )

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

    summary = f"""
## ☕ Our Recommendation for You

### Your curated flavor profile
- **Overall Flavor Preference (Taste/Aroma):** {final_flavor:.1f}
- **Acidity Level:** {final_acidity:.1f}
- **Sweetness Level:** {final_sweetness:.1f}
- **Typical Coffee Order:** {drink}

### Recommended drink style
**{rec_style}**

### Why we picked it
{reason}

This recommendation is based on your slider preferences plus the style of coffee you usually order at cafés.
"""

    top_matches = pd.DataFrame({
        "Category": ["Flavor", "Acidity", "Sweetness", "Typical Order", "Recommended Style"],
        "Your Profile": [
            round(final_flavor, 1),
            round(final_acidity, 1),
            round(final_sweetness, 1),
            drink,
            rec_style
        ]
    })

    return summary, top_matches


# =========================================================
# CUTE COFFEE THEME CSS
# =========================================================
custom_css = """
body {
    background: #EADCCB !important;
    color: #7B3F00 !important;
}

.gradio-container {
    font-family: 'Comic Sans MS', 'Comic Sans', cursive !important;
    background: #EADCCB !important;
    color: #7B3F00 !important;
}

.block, .gr-box, .gr-form, .gr-panel {
    background: #F6EBDD !important;
    border: 2px solid #5C3A21 !important;
    border-radius: 18px !important;
}

button[role="tab"] {
    background: #D9C8A9 !important;
    color: #7B3F00 !important;
    border: 2px solid #5C3A21 !important;
    border-bottom: none !important;
    font-family: 'Comic Sans MS', 'Comic Sans', cursive !important;
    font-size: 20px !important;
}

button[role="tab"][aria-selected="true"] {
    background: #F6EBDD !important;
    font-weight: bold !important;
}

label, p, h1, h2, h3, h4, span, div {
    color: #7B3F00 !important;
    font-family: 'Comic Sans MS', 'Comic Sans', cursive !important;
}

button {
    border-radius: 14px !important;
    border: 2px solid #5C3A21 !important;
    background: #E7D6B8 !important;
    color: #7B3F00 !important;
    font-family: 'Comic Sans MS', 'Comic Sans', cursive !important;
}

input, textarea, select {
    border: 2px solid #7A5230 !important;
    border-radius: 12px !important;
    background: #FFF9F1 !important;
    color: #7B3F00 !important;
    font-family: 'Comic Sans MS', 'Comic Sans', cursive !important;
}

/* Brown sliders */
input[type="range"] {
    accent-color: #5C3A21 !important;
}

.coffee-pattern {
    background:
        radial-gradient(circle at 20px 20px, rgba(183,123,67,0.30) 1.4px, transparent 1.5px),
        #F6EBDD !important;
    background-size: 22px 22px !important;
    border: 2px solid #5C3A21 !important;
    border-radius: 18px !important;
    padding: 18px !important;
}

.hero-box {
    background: #F6EBDD !important;
    border: 2px solid #5C3A21 !important;
    border-radius: 22px !important;
    padding: 26px !important;
    text-align: center !important;
}

.app-title {
    font-size: 42px !important;
    font-weight: 800 !important;
    margin-bottom: 8px !important;
    color: #7B3F00 !important;
}

.app-subtitle {
    font-size: 22px !important;
    font-style: italic !important;
    margin-bottom: 12px !important;
    color: #7B3F00 !important;
}

.created-by {
    font-size: 20px !important;
    margin-top: 14px !important;
    color: #7B3F00 !important;
}
"""


# =========================================================
# APP LAYOUT
# =========================================================
with gr.Blocks(css=custom_css, title="PerfectPour ☕") as app:

    with gr.Tabs():

        # -------------------------------------------------
        # TAB 1
        # -------------------------------------------------
        with gr.Tab("Start Here"):
            gr.HTML("""
            <div class="hero-box">
                <div class="app-title">☕ PerfectPour ☕</div>
                <div class="app-subtitle">Curating your perfect coffee match based on your taste preferences and café orders.</div>
                <div class="created-by"><b>Created By:</b><br>Reagan McGowan &amp; Ashly Turcios</div>
            </div>
            """)

            gr.Markdown("""
### Welcome to our coffee recommendation app

Our app is designed to personalize coffee suggestions based on the flavor characteristics you enjoy most.

You’ll be able to:
- choose your preferred **taste/aroma level**
- choose your preferred **acidity**
- choose your preferred **sweetness**
- select your **typical coffee order**
- see **where your taste profile falls**
- receive a **recommended drink style**
""")

        # -------------------------------------------------
        # TAB 2
        # -------------------------------------------------
        with gr.Tab("Your Preferences"):
            with gr.Column(elem_classes="coffee-pattern"):
                gr.Markdown("## Tell us what kind of coffee you love")

                flavor_in = gr.Slider(
                    1, 10, value=6.5, step=0.1,
                    label="Overall Flavor Preference: Taste/Aroma"
                )

                acidity_in = gr.Slider(
                    1, 10, value=5.5, step=0.1,
                    label="Acidity Level"
                )

                sweetness_in = gr.Slider(
                    1, 10, value=6.0, step=0.1,
                    label="Sweetness Level"
                )

                drink_in = gr.Dropdown(
                    choices=coffee_drink_choices,
                    value="Iced latte",
                    label="Your typical coffee of choice"
                )

                profile_preview = gr.Markdown()
                preview_btn = gr.Button("Save My Preferences")

                preview_btn.click(
                    fn=live_preference_summary,
                    inputs=[flavor_in, acidity_in, sweetness_in, drink_in],
                    outputs=profile_preview
                )

        # -------------------------------------------------
        # TAB 3
        # -------------------------------------------------
        with gr.Tab("Where You Fall"):
            with gr.Column(elem_classes="coffee-pattern"):
                gr.Markdown("## Where You Fall")
                gr.Markdown("*Hover over each dot to compare your profile with different coffee drink types.*")

                profile_btn = gr.Button("Show My Taste Profile")
                profile_plot = gr.Plot(label="Acidity vs Sweetness Coffee Map")

                profile_btn.click(
                    fn=where_you_fall_plot,
                    inputs=[flavor_in, acidity_in, sweetness_in, drink_in],
                    outputs=profile_plot
                )

        # -------------------------------------------------
        # TAB 4
        # -------------------------------------------------
        with gr.Tab("Your Perfect Coffee"):
            with gr.Column(elem_classes="coffee-pattern"):
                gr.Markdown("## Your curated coffee recommendation")

                rec_btn = gr.Button("Find My Perfect Coffee")
                rec_summary = gr.Markdown()
                rec_table = gr.Dataframe(
                    interactive=False,
                    wrap=True,
                    label="Your coffee profile summary"
                )

                rec_btn.click(
                    fn=recommend_drink_style,
                    inputs=[flavor_in, acidity_in, sweetness_in, drink_in],
                    outputs=[rec_summary, rec_table]
                )

if __name__ == "__main__":
    app.launch()