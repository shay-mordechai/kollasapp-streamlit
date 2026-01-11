import streamlit as st

def render_tagging_form(recording_data):
    """
    Renders the metadata input form.

    Args:
        recording_data (pd.Series or dict): The current data of the recording being identified.

    Returns:
        dict or None: Returns a dictionary of form data if submitted, None otherwise.
    """

    # Pre-defined options for the Cochin Community
    ORIGINS = ["Unknown", "Ernakulam", "Parur", "Cochin (Jew Town)", "Chendamangalam", "Mala"]
    CANTORS = ["Unknown", "Moshe", "Yosef Hai", "Elias", "Other (Type Name)"]

    with st.form(key=f"tag_form_{recording_data['recording_id']}"):
        st.markdown("### 📝 What do you hear?")

        col1, col2 = st.columns(2)

        with col1:
            # Cantor Selection
            selected_cantor = st.selectbox(
                "Who is singing? (Cantor)",
                options=CANTORS,
                index=0,
                help="Select the main singer"
            )

            # Dynamic input if 'Other' is selected
            custom_cantor = ""
            if selected_cantor == "Other (Type Name)":
                custom_cantor = st.text_input("Enter Cantor Name")

        with col2:
            # Origin Selection
            origin = st.selectbox(
                "Tradition / Origin",
                options=ORIGINS,
                index=0,
                help="Which synagogue tradition is this?"
            )

        # Piyyut Name
        piyyut_name = st.text_input(
            "Piyyut Name (Title)",
            value=recording_data.get('file_name', ''), # Default to filename if empty
            help="Name of the song in Hebrew or English"
        )

        # Additional Notes
        notes = st.text_area(
            "Memories / Lyrics / Notes",
            placeholder="Example: This was recorded at the 1980 wedding...",
            height=100
        )

        st.markdown("---")

        # Action Buttons
        submit_col, skip_col = st.columns([3, 1])

        with submit_col:
            submit_clicked = st.form_submit_button("✅ Submit Information", type="primary", use_container_width=True)

        # Note: Skip is handled outside the form usually, but if inside, it just submits without processing

    if submit_clicked:
        # Construct the feedback payload
        final_cantor = custom_cantor if selected_cantor == "Other (Type Name)" else selected_cantor

        return {
            "recording_id": recording_data['recording_id'],
            "suggested_cantor": final_cantor,
            "suggested_origin": origin,
            "suggested_piyyut": piyyut_name,
            "comments": notes
        }

    return None
