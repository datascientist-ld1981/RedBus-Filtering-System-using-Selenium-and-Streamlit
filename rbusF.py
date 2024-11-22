import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px
from datetime import datetime


def connect_to_database():
    """
    Establishes and returns a connection to the MySQL database.

    Returns:
        connection: The database connection object.
    """
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="guvi",
    )


def format_time(time_value):
    """
    Formats the MySQL TIME value into a readable HH:MM:SS format.

    Args:
        time_value (str or None): The MySQL TIME value as a string.

    Returns:
        str: The formatted time as HH:MM:SS, or "N/A" if the value is None.
    """
    if time_value is None or time_value == "":
        return "N/A"

    try:
        return datetime.strptime(str(time_value), "%H:%M:%S.%f").strftime("%H:%M:%S")
    except ValueError:
        return str(time_value)


def fetch_redbus_data(connection, state=None, route_name=None, bus_name=None, bus_type=None, 
                      min_price=None, max_price=None, min_departing_time=None, max_departing_time=None, 
                      min_star_rating=None, max_star_rating=None):
    """
    Fetches filtered redBus data from the database based on selected filters.

    Args:
        connection: The database connection object.
        state (str, optional): Filter by state.
        route_name (str, optional): Filter by route name.
        bus_name (str, optional): Filter by bus name.
        bus_type (str, optional): Filter by bus type.
        min_price (float, optional): Minimum price filter.
        max_price (float, optional): Maximum price filter.
        min_departing_time (str, optional): Minimum departing time filter (HH:MM:SS).
        max_departing_time (str, optional): Maximum departing time filter (HH:MM:SS).
        min_star_rating (float, optional): Minimum star rating filter.
        max_star_rating (float, optional): Maximum star rating filter.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the filtered data.
        str: The SQL query used for the data fetching.
    """
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM redbus WHERE 1=1"
    params = []

    if state and state != "None":
        query += " AND state = %s"
        params.append(state)
    if route_name and route_name != "None":
        query += " AND route_name = %s"
        params.append(route_name)
    if bus_name and bus_name != "None":
        query += " AND bus_name = %s"
        params.append(bus_name)
    if bus_type and bus_type != "None":
        query += " AND bus_type = %s"
        params.append(bus_type)
    
    # Filter by price range
    if min_price is not None:
        query += " AND price >= %s"
        params.append(min_price)
    if max_price is not None:
        query += " AND price <= %s"
        params.append(max_price)
    
    # Filter by departing time
    if min_departing_time is not None:
        query += " AND departing_time >= %s"
        params.append(min_departing_time)
    if max_departing_time is not None:
        query += " AND departing_time <= %s"
        params.append(max_departing_time)
    
    # Filter by star rating
    if min_star_rating is not None:
        query += " AND star_rating >= %s"
        params.append(min_star_rating)
    if max_star_rating is not None:
        query += " AND star_rating <= %s"
        params.append(max_star_rating)

    # Exclude rows with NULL or empty fields in the key columns
    query += " AND state IS NOT NULL AND state != ''"
    query += " AND route_name IS NOT NULL AND route_name != ''"
    query += " AND bus_name IS NOT NULL AND bus_name != ''"
    query += " AND bus_type IS NOT NULL AND bus_type != ''"

    cursor.execute(query, params)
    result = cursor.fetchall()

    # If no rows are returned, return an empty DataFrame
    if not result:
        return pd.DataFrame(), query

    df = pd.DataFrame(result)

    # Format time columns
    for col in ["departing_time", "reaching_time"]:
        if col in df.columns:
            df[col] = df[col].apply(format_time)

    return df, query


def get_distinct_states(connection):
    """
    Retrieves a list of distinct states and their corresponding state names from the redbus_state_transport table.

    Args:
        connection: The database connection object.

    Returns:
        list of tuples: A list of tuples where each tuple contains (state, state_name).
    """
    cursor = connection.cursor()
    query = """
        SELECT r.state, s.state_name 
        FROM redbus r
        JOIN redbus_state_transport s ON r.state = s.state  -- Corrected foreign key relationship
        GROUP BY r.state, s.state_name
    """
    cursor.execute(query)
    return cursor.fetchall()


def get_routes_by_state(connection, state):
    """
    Retrieves a list of routes based on the selected state.

    Args:
        connection: The database connection object.
        state (str): The selected state.

    Returns:
        list: A list of route names.
    """
    cursor = connection.cursor()
    query = "SELECT DISTINCT route_name FROM redbus WHERE state = %s"
    cursor.execute(query, (state,))
    return [row[0] for row in cursor.fetchall()]


def get_bus_names_by_route(connection, route_name):
    """
    Retrieves a list of bus names based on the selected route.

    Args:
        connection: The database connection object.
        route_name (str): The selected route.

    Returns:
        list: A list of bus names.
    """
    cursor = connection.cursor()
    query = "SELECT DISTINCT bus_name FROM redbus WHERE route_name = %s"
    cursor.execute(query, (route_name,))
    return [row[0] for row in cursor.fetchall()]


def get_bus_types(connection):
    """
    Retrieves a list of distinct bus types from the database.

    Args:
        connection: The database connection object.

    Returns:
        list: A list of bus types.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT bus_type FROM redbus")
    return [row[0] for row in cursor.fetchall()]


def display_pie_chart(filtered_data):
    """
    Displays a pie chart for seat availability.

    Args:
        filtered_data (pd.DataFrame): The filtered data.
    """
    if filtered_data.empty or "seats_available" not in filtered_data.columns:
        st.write("No data available to display the pie chart.")
        return

    # Replace missing bus names with "Others"
    filtered_data["bus_name"] = filtered_data["bus_name"].fillna("Others")

    # Aggregate data for the pie chart
    pie_data = filtered_data.groupby("bus_name")["seats_available"].sum().reset_index()

    # Plot pie chart
    fig = px.pie(
        pie_data,
        names="bus_name",
        values="seats_available",
        title="Seats Available by Bus Name",
        hole=0.3,
        labels={"bus_name": "Bus Name", "seats_available": "Seats Available"},
    )
    fig.update_traces(textinfo="value+label")
    st.plotly_chart(fig)


def display_data(filtered_data):
    """
    Displays the filtered data in a table format.

    Args:
        filtered_data (pd.DataFrame): The filtered redBus data.
    """
    if filtered_data.empty:
        st.write("No data available for the selected filters.")
    else:
        st.dataframe(filtered_data)


def main():
    """
    Main function to run the Streamlit app.
    """
    st.set_page_config(
        page_title="RedBus Travel Information",
        page_icon="🚌",
        layout="wide",
    )

    st.title("RedBus Travel Information System")
    st.write("Filter and visualize interstate travel data.")

    connection = connect_to_database()

    # Step 1: Select State
    states = get_distinct_states(connection)
    state_options = [state[0] for state in states]
    state_name_dict = {state[0]: state[1] for state in states}
    state = st.sidebar.selectbox("Select State", ["None"] + state_options)

    if state and state != "None":
        state_name = state_name_dict.get(state, "Unknown")
        st.sidebar.markdown(f"**State Selected: <span style='color:red'>{state_name}</span>**", unsafe_allow_html=True)

        # Step 2: Select Route Name
        route_names = get_routes_by_state(connection, state)
        route_name = st.sidebar.selectbox("Select Route Name", ["None"] + route_names)

        if route_name and route_name != "None":
            # Step 3: Select Bus Name and Type
            bus_names = get_bus_names_by_route(connection, route_name)
            bus_name = st.sidebar.selectbox("Select Bus Name", ["None"] + bus_names)

            bus_types = get_bus_types(connection)
            bus_type = st.sidebar.selectbox("Select Bus Type", ["None"] + bus_types)

            # Add filters for price range, departing time, and star rating
            min_price, max_price = st.sidebar.slider(
                "Select Price Range", min_value=0, max_value=1000, value=(0, 1000), step=10
            )
            min_departing_time = st.sidebar.time_input("Min Departing Time", datetime(2000, 1, 1, 0, 0))
            max_departing_time = st.sidebar.time_input("Max Departing Time", datetime(2000, 1, 1, 23, 59))
            min_star_rating, max_star_rating = st.sidebar.slider(
                "Select Star Rating", min_value=1, max_value=5, value=(1, 5), step=1
            )

            # Step 4: Submit Button to fetch data and display SQL query
            if st.sidebar.button("Submit"):
                filtered_data, query = fetch_redbus_data(
                    connection, state, route_name, bus_name, bus_type,
                    min_price, max_price, min_departing_time.strftime("%H:%M:%S"), 
                    max_departing_time.strftime("%H:%M:%S"), min_star_rating, max_star_rating
                )

                # Display SQL Query
                st.sidebar.write("### SQL Query Used:")
                st.sidebar.code(query)

                # Display pie chart and data
                display_pie_chart(filtered_data)
                display_data(filtered_data)
        else:
            st.write("Please select a route name to proceed.")
    else:
        st.write("Please select a state to proceed.")

    connection.close()


if __name__ == "__main__":
    main()
