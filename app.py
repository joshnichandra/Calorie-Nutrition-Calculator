import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NutriGlow - Calorie Calculator",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(255, 193, 7, 0.15), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(0, 188, 212, 0.15), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(156, 39, 176, 0.12), transparent 30%),
        #f7f9fc;
}


/* Main title */

.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 0px;
    background: linear-gradient(
        90deg,
        #ff6f61,
        #ffb300,
        #00acc1,
        #7e57c2
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #667085;
    font-size: 17px;
    margin-bottom: 30px;
}


/* Cards */

.info-card {
    padding: 22px;
    border-radius: 20px;
    background: white;
    box-shadow: 0 8px 25px rgba(0,0,0,0.07);
    border: 1px solid rgba(0,0,0,0.04);
    margin-bottom: 18px;
}

.card-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
}


/* Metric cards */

.metric-card {
    padding: 22px;
    border-radius: 20px;
    color: white;
    text-align: center;
    min-height: 125px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.metric-icon {
    font-size: 28px;
}

.metric-value {
    font-size: 28px;
    font-weight: 800;
}

.metric-label {
    font-size: 14px;
    opacity: 0.9;
}


/* Food item */

.food-card {
    background: white;
    border-radius: 16px;
    padding: 15px;
    margin: 8px 0;
    border-left: 5px solid #00acc1;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}


/* Section */

.section-title {
    font-size: 26px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 15px;
}


/* Buttons */

.stButton > button {
    border-radius: 12px;
    border: none;
    font-weight: 700;
    padding: 10px 20px;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
}


/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #172554,
        #312e81,
        #4c1d95
    );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}


/* Footer */

.footer {
    text-align: center;
    color: #7a7f87;
    padding: 30px 0 10px 0;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FOOD DATABASE
# Values are approximate per standard serving
# ============================================================

foods = {
    "🍚 Rice": {
        "category": "Grains",
        "serving": "1 cup",
        "calories": 205,
        "protein": 4.3,
        "carbs": 44.5,
        "fat": 0.4
    },

    "🥚 Egg": {
        "category": "Protein",
        "serving": "1 egg",
        "calories": 78,
        "protein": 6.3,
        "carbs": 0.6,
        "fat": 5.3
    },

    "🍗 Chicken": {
        "category": "Protein",
        "serving": "100 g",
        "calories": 165,
        "protein": 31.0,
        "carbs": 0,
        "fat": 3.6
    },

    "🥛 Milk": {
        "category": "Dairy",
        "serving": "1 cup",
        "calories": 122,
        "protein": 8.0,
        "carbs": 12.0,
        "fat": 4.8
    },

    "🍎 Apple": {
        "category": "Fruit",
        "serving": "1 medium",
        "calories": 95,
        "protein": 0.5,
        "carbs": 25.0,
        "fat": 0.3
    },

    "🍌 Banana": {
        "category": "Fruit",
        "serving": "1 medium",
        "calories": 105,
        "protein": 1.3,
        "carbs": 27.0,
        "fat": 0.4
    },

    "🥕 Carrot": {
        "category": "Vegetable",
        "serving": "1 medium",
        "calories": 25,
        "protein": 0.6,
        "carbs": 6.0,
        "fat": 0.1
    },

    "🥔 Potato": {
        "category": "Vegetable",
        "serving": "1 medium",
        "calories": 130,
        "protein": 3.0,
        "carbs": 30.0,
        "fat": 0.2
    },

    "🥣 Oatmeal": {
        "category": "Grains",
        "serving": "1 bowl",
        "calories": 150,
        "protein": 5.0,
        "carbs": 27.0,
        "fat": 3.0
    },

    "🍞 Bread": {
        "category": "Grains",
        "serving": "1 slice",
        "calories": 75,
        "protein": 3.0,
        "carbs": 13.0,
        "fat": 1.0
    },

    "🥜 Peanut Butter": {
        "category": "Protein",
        "serving": "1 tbsp",
        "calories": 94,
        "protein": 4.0,
        "carbs": 3.0,
        "fat": 8.0
    },

    "🥗 Salad": {
        "category": "Vegetable",
        "serving": "1 bowl",
        "calories": 80,
        "protein": 3.0,
        "carbs": 12.0,
        "fat": 2.0
    },

    "🧀 Cheese": {
        "category": "Dairy",
        "serving": "1 slice",
        "calories": 113,
        "protein": 7.0,
        "carbs": 1.0,
        "fat": 9.0
    },

    "🍊 Orange": {
        "category": "Fruit",
        "serving": "1 medium",
        "calories": 62,
        "protein": 1.2,
        "carbs": 15.4,
        "fat": 0.2
    },

    "🥛 Yogurt": {
        "category": "Dairy",
        "serving": "1 cup",
        "calories": 150,
        "protein": 8.5,
        "carbs": 11.0,
        "fat": 8.0
    }
}


# ============================================================
# SESSION STATE
# ============================================================

if "food_log" not in st.session_state:
    st.session_state.food_log = []


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🥗 NutriGlow</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'A colorful and simple Calorie & Nutrition Calculator'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🌈 NutriGlow")

    st.write("Build your food log and explore its nutrition.")

    st.markdown("---")

    st.markdown("### 📌 How to use")

    st.write("1️⃣ Select a meal")
    st.write("2️⃣ Choose a food")
    st.write("3️⃣ Select the quantity")
    st.write("4️⃣ Add it to your food log")
    st.write("5️⃣ View your nutrition summary")

    st.markdown("---")

    st.markdown("### ℹ️ Note")

    st.write(
        "Nutrition values shown here are approximate "
        "and can vary by food type, preparation and serving size."
    )


# ============================================================
# FOOD ENTRY
# ============================================================

st.markdown(
    '<div class="section-title">🍽️ Add Food</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1.2, 2, 1])

with col1:

    meal = st.selectbox(
        "Meal",
        [
            "🌅 Breakfast",
            "☀️ Lunch",
            "🌆 Dinner",
            "🍿 Snack"
        ]
    )

with col2:

    selected_food = st.selectbox(
        "Food",
        list(foods.keys())
    )

with col3:

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=10,
        value=1,
        step=1
    )


food_info = foods[selected_food]

st.markdown(
    f"""
    <div class="food-card">
        <b>{selected_food}</b><br>
        Serving: {food_info['serving']} |
        🔥 {food_info['calories']} kcal |
        💪 Protein: {food_info['protein']} g |
        🍞 Carbs: {food_info['carbs']} g |
        🥑 Fat: {food_info['fat']} g
    </div>
    """,
    unsafe_allow_html=True
)


add_col, clear_col = st.columns([3, 1])

with add_col:

    if st.button(
        "➕ Add Food to My Log",
        use_container_width=True
    ):

        item = {
            "Meal": meal,
            "Food": selected_food,
            "Quantity": quantity,
            "Calories": food_info["calories"] * quantity,
            "Protein": food_info["protein"] * quantity,
            "Carbs": food_info["carbs"] * quantity,
            "Fat": food_info["fat"] * quantity
        }

        st.session_state.food_log.append(item)

        st.success(f"Added {quantity} × {selected_food} to your food log! 🎉")


with clear_col:

    if st.button(
        "🗑️ Clear All",
        use_container_width=True
    ):

        st.session_state.food_log = []

        st.rerun()


# ============================================================
# SUMMARY
# ============================================================

if st.session_state.food_log:

    df = pd.DataFrame(st.session_state.food_log)

    total_calories = df["Calories"].sum()
    total_protein = df["Protein"].sum()
    total_carbs = df["Carbs"].sum()
    total_fat = df["Fat"].sum()

    st.markdown(
        '<div class="section-title">✨ Nutrition Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="metric-card"
                 style="background: linear-gradient(135deg,#ff6f61,#ff8a65);">
                <div class="metric-icon">🔥</div>
                <div class="metric-value">{total_calories:.0f}</div>
                <div class="metric-label">Total Calories</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="metric-card"
                 style="background: linear-gradient(135deg,#00acc1,#26c6da);">
                <div class="metric-icon">💪</div>
                <div class="metric-value">{total_protein:.1f} g</div>
                <div class="metric-label">Protein</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="metric-card"
                 style="background: linear-gradient(135deg,#7e57c2,#ab47bc);">
                <div class="metric-icon">🍞</div>
                <div class="metric-value">{total_carbs:.1f} g</div>
                <div class="metric-label">Carbohydrates</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="metric-card"
                 style="background: linear-gradient(135deg,#43a047,#66bb6a);">
                <div class="metric-icon">🥑</div>
                <div class="metric-value">{total_fat:.1f} g</div>
                <div class="metric-label">Fat</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # FOOD LOG
    # ========================================================

    st.markdown(
        '<div class="section-title">📋 My Food Log</div>',
        unsafe_allow_html=True
    )

    display_df = df.copy()

    display_df["Calories"] = display_df["Calories"].round(1)
    display_df["Protein"] = display_df["Protein"].round(1)
    display_df["Carbs"] = display_df["Carbs"].round(1)
    display_df["Fat"] = display_df["Fat"].round(1)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # CHARTS
    # ========================================================

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.markdown(
            "### 🍽️ Calories by Meal"
        )

        meal_data = (
            df.groupby("Meal")["Calories"]
            .sum()
            .reset_index()
        )

        fig_meal = px.bar(
            meal_data,
            x="Meal",
            y="Calories",
            color="Meal",
            text_auto=".0f",
            title="Meal-wise Calorie Distribution"
        )

        fig_meal.update_layout(
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_meal,
            use_container_width=True
        )


    with chart_col2:

        st.markdown(
            "### 🥑 Macronutrients"
        )

        macro_df = pd.DataFrame({
            "Nutrient": [
                "Protein",
                "Carbohydrates",
                "Fat"
            ],
            "Amount": [
                total_protein,
                total_carbs,
                total_fat
            ]
        })

        fig_macro = px.pie(
            macro_df,
            names="Nutrient",
            values="Amount",
            hole=0.45,
            title="Macro Distribution"
        )

        fig_macro.update_layout(
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_macro,
            use_container_width=True
        )


    # ========================================================
    # INSIGHTS
    # ========================================================

    st.markdown(
        '<div class="section-title">💡 Nutrition Summary</div>',
        unsafe_allow_html=True
    )

    insight1, insight2, insight3 = st.columns(3)

    with insight1:

        st.info(
            f"🔥 Your food log contains approximately "
            f"**{total_calories:.0f} kcal**."
        )

    with insight2:

        st.info(
            f"💪 Your logged foods provide approximately "
            f"**{total_protein:.1f} g protein**."
        )

    with insight3:

        st.info(
            f"🍎 You have logged **{len(df)} food entries**."
        )


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    report = f"""
NUTRIGLOW - CALORIE & NUTRITION REPORT
======================================

Generated: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}

TOTAL NUTRITION
---------------
Calories       : {total_calories:.1f} kcal
Protein        : {total_protein:.1f} g
Carbohydrates  : {total_carbs:.1f} g
Fat            : {total_fat:.1f} g

FOOD LOG
--------

"""

    for _, row in df.iterrows():

        report += (
            f"{row['Meal']} | "
            f"{row['Food']} | "
            f"Quantity: {row['Quantity']} | "
            f"Calories: {row['Calories']:.1f} kcal\n"
        )

    report += """

NOTE
----
Nutrition values are approximate and may vary based
on food type, preparation and serving size.
This calculator is for educational purposes.
"""

    st.download_button(
        "📥 Download Nutrition Report",
        data=report,
        file_name="NutriGlow_Nutrition_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

else:

    st.markdown(
        """
        <div class="info-card">
            <div class="card-title">🌟 Your nutrition dashboard is ready!</div>
            <p>
            Select a meal and food above, choose the quantity,
            and click <b>Add Food to My Log</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🥗 NutriGlow • Calorie & Nutrition Calculator<br>
        Built with Python + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)