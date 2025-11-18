import streamlit as st

# -------------------------------------------------
# Helper: display the current friend list as a table
# -------------------------------------------------
def show_friends(friends):
    if friends:
        st.table(
            [{"Name": n, "Phone": p, "City": c} for n, p, c in friends]
        )
    else:
        st.info("No friends yet.")

# -------------------------------------------------
# Session state initialisation
# -------------------------------------------------
if "friends" not in st.session_state:
    st.session_state.friends = []          # list of tuples (name, phone, city)

# -------------------------------------------------
# 1. Add the first three friends
# -------------------------------------------------
st.header("1. Add three friends")
with st.form("initial_friends_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        name1 = st.text_input("Friend 1 – Name", key="n1")
        name2 = st.text_input("Friend 2 – Name", key="n2")
        name3 = st.text_input("Friend 3 – Name", key="n3")
    with col2:
        phone1 = st.number_input("Friend 1 – Phone", format="%d", key="p1")
        phone2 = st.number_input("Friend 2 – Phone", format="%d", key="p2")
        phone3 = st.number_input("Friend 3 – Phone", format="%d", key="p3")
    with col3:
        city1 = st.text_input("Friend 1 – City", key="c1")
        city2 = st.text_input("Friend 2 – City", key="c2")
        city3 = st.text_input("Friend 3 – City", key="c3")

    submitted = st.form_submit_button("Save initial friends")
    if submitted:
        # clear any previous initial friends
        st.session_state.friends = [
            (name1, int(phone1), city1),
            (name2, int(phone2), city2),
            (name3, int(phone3), city3),
        ]
        st.success("Three friends saved!")

# -------------------------------------------------
# Show current list (always visible after step 1)
# -------------------------------------------------
if st.session_state.friends:
    st.subheader("Current friend list")
    show_friends(st.session_state.friends)

# -------------------------------------------------
# 2. Add a new friend
# -------------------------------------------------
st.header("2. Add a new friend")
with st.form("add_friend_form"):
    new_name = st.text_input("New friend – Name")
    new_phone = st.number_input("New friend – Phone", format="%d")
    new_city = st.text_input("New friend – City")
    add_btn = st.form_submit_button("Add friend")

    if add_btn:
        st.session_state.friends.append((new_name, int(new_phone), new_city))
        st.success(f"{new_name} added!")

# -------------------------------------------------
# 3. Remove a friend
# -------------------------------------------------
st.header("3. Remove a friend")
if st.session_state.friends:
    with st.form("remove_friend_form"):
        # Build a selectbox from the current list
        options = [f"{n} – {p} – {c}" for n, p, c in st.session_state.friends]
        chosen = st.selectbox("Select friend to delete", options)
        remove_btn = st.form_submit_button("Delete selected friend")

        if remove_btn:
            idx = options.index(chosen)
            removed = st.session_state.friends.pop(idx)
            st.success(f"Removed: {removed[0]}")
else:
    st.info("Add friends first before trying to remove.")

# -------------------------------------------------
# 4. Summary & unique cities
# -------------------------------------------------
if st.session_state.friends:
    st.subheader("Summary")
    st.write(f"**Total friends:** {len(st.session_state.friends)}")

    # extract cities (including the last added one if any)
    cities = {city for _, _, city in st.session_state.friends}
    st.write("**Unique cities:**", ", ".join(sorted(cities)))
    st.write(f"**Number of unique cities:** {len(cities)}")