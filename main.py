import streamlit as st

st.set_page_config(page_title="Affective Positioning System (APS)", layout="wide")

PLANE_META = {
    "p1": {
        "title": "Plane 1 · Internal State",
        "subtitle": "Perceived Need × Emotional Stability",
        "x_label": "Perceived Need",
        "y_label": "Emotional Stability",
        "quadrants": {
            "Q1": ("Role Fulfillment", "You feel needed and emotionally capable of carrying that role."),
            "Q2": ("Safe but Empty", "You feel stable, but your sense of being needed is relatively low."),
            "Q3": ("Self-Worth Fracture", "You feel neither securely needed nor internally stable."),
            "Q4": ("Collapse Risk", "You feel highly needed, but emotionally unable to sustain the pressure."),
        },
    },
    "p2": {
        "title": "Plane 2 · Power Dynamics",
        "subtitle": "How much I need the other × How much I am needed",
        "x_label": "How much I need the other",
        "y_label": "How much I am needed",
        "quadrants": {
            "Q1": ("Mutual Interdependence", "Both attachment and usefulness are relatively high."),
            "Q2": ("Power Advantage", "You are more needed than needy."),
            "Q3": ("Weak Attachment", "Neither side appears deeply dependent."),
            "Q4": ("Anxious Pursuit", "You need the other more than you are needed."),
        },
    },
    "p3": {
        "title": "Plane 3 · Motivational Structure",
        "subtitle": "How much I need the other × Material-to-Emotional Orientation",
        "x_label": "How much I need the other",
        "y_label": "Material → Emotional / Ideational",
        "quadrants": {
            "Q1": ("Deep Affective Bond", "Need is high and the tie is emotionally or ideationally oriented."),
            "Q2": ("Principled Commitment", "Need is lower, but the bond is still guided by values or care."),
            "Q3": ("Low-Need Reflective Tie", "The relationship is not heavily need-based and not strongly material."),
            "Q4": ("Pragmatic Dependence", "Need is high and materially grounded."),
        },
    },
}

def get_quadrant(x, y):
    if x >= 50 and y >= 50:
        return "Q1"
    elif x < 50 and y >= 50:
        return "Q2"
    elif x < 50 and y < 50:
        return "Q3"
    else:
        return "Q4"

def interpret_plane(plane_id, x, y):
    q = get_quadrant(x, y)
    name, desc = PLANE_META[plane_id]["quadrants"][q]
    return q, name, desc

st.title("Affective Positioning System (APS)")
st.write(
    "A relational analysis prototype that maps internal state, power dynamics, "
    "and motivational structure across three planes."
)

dual_mode = st.toggle("Enable dual-person mode", value=True)

st.markdown("---")

def person_block(label, prefix):
    st.subheader(label)

    st.markdown(f"### {PLANE_META['p1']['title']}")
    st.caption(PLANE_META["p1"]["subtitle"])
    p1x = st.slider(f"{prefix} · {PLANE_META['p1']['x_label']}", 0, 100, 70)
    p1y = st.slider(f"{prefix} · {PLANE_META['p1']['y_label']}", 0, 100, 65)

    st.markdown(f"### {PLANE_META['p2']['title']}")
    st.caption(PLANE_META["p2"]["subtitle"])
    p2x = st.slider(f"{prefix} · {PLANE_META['p2']['x_label']}", 0, 100, 55)
    p2y = st.slider(f"{prefix} · {PLANE_META['p2']['y_label']}", 0, 100, 60)

    st.markdown(f"### {PLANE_META['p3']['title']}")
    st.caption(PLANE_META["p3"]["subtitle"])
    p3x = st.slider(f"{prefix} · {PLANE_META['p3']['x_label']}", 0, 100, 60)
    p3y = st.slider(f"{prefix} · {PLANE_META['p3']['y_label']}", 0, 100, 75)

    return {
        "p1": (p1x, p1y),
        "p2": (p2x, p2y),
        "p3": (p3x, p3y),
    }

if dual_mode:
    col1, col2 = st.columns(2)
    with col1:
        a = person_block("Person A", "A")
    with col2:
        b = person_block("Person B", "B")
else:
    a = person_block("Person A", "A")
    b = None

if st.button("Generate description"):
    st.markdown("---")
    st.header("Interpretation")

    for plane_id in ["p1", "p2", "p3"]:
        q, name, desc = interpret_plane(plane_id, a[plane_id][0], a[plane_id][1])
        st.write(f"**Person A — {PLANE_META[plane_id]['title']}**")
        st.write(f"{q}: **{name}** — {desc}")

    if b:
        for plane_id in ["p1", "p2", "p3"]:
            q, name, desc = interpret_plane(plane_id, b[plane_id][0], b[plane_id][1])
            st.write(f"**Person B — {PLANE_META[plane_id]['title']}**")
            st.write(f"{q}: **{name}** — {desc}")

        st.subheader("Generated dyadic description")
        st.write(
            "This dyad can be read as a structured system rather than a single emotional category. "
            "APS suggests that the relationship may contain different levels of internal stability, "
            "dependency asymmetry, and motivational mismatch across the three planes."
        )
    else:
        st.subheader("Generated self-positioning description")
        st.write(
            "APS reads your current position as a structured relationship state rather than a simple mood. "
            "Your internal state, dependency logic, and motivational orientation together shape how this tie is experienced."
        )