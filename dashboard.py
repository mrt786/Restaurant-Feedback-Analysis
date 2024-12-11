import json
import streamlit as st
from itertools import zip_longest  # to iterate in the uneven length of dicts

st.title("RESTAURANT FEEDBACK ANALYSIS")
# Function to load data from a JSON file
def loadDataFromJson(restaurantName):
    with open(f'{restaurantName}.json', 'r') as file:
        loadData = json.load(file)
    return loadData

def editColorOfSentiment(senitment):
    style = ""
    imageTag = ""
    if senitment == "positive":
        style = "<span style='color:#4CAF50 ;font-weight: bold'>"
        imageTag = '<img src="happy.png" width="50" height="50" alt="positive sentiment" />'

    elif senitment == "negative":
        style = "<span style='color:#F44336;font-weight: bold'>"
        imageTag = '<img src="sad.png" width="50" height="50" alt="negative sentiment" />'
    elif senitment == "neutral":
        style = "<span style='color:#333333;font-weight: bold'>"
        imageTag = '<img src="neutral.png" width="50" height="50" alt="Neutral sentiment" />'
    return style, imageTag

# Define functions for each page
def reviews_page(restaurantName="FANG"):
    reviews_per_page = 10

    # Load data once and store in session state
    st.subheader(f"Restaurant Name: {restaurantName}")
    st.html(f"<h3> Original Reviews Page </h3>")
    if "originalReviews" not in st.session_state:
        st.session_state.originalReviews = loadDataFromJson(restaurantName)
    originalReviews = st.session_state.originalReviews

    total_reviews = len(originalReviews)
    total_pages = (total_reviews // reviews_per_page) + (1 if total_reviews % reviews_per_page != 0 else 0)
    

    # Select current page
    current_page = st.number_input("Select Page:", min_value=1, max_value=total_pages, value=1, step=1)

    # Calculate the range of reviews to show
    start_idx = max((current_page - 1) * reviews_per_page, 0)
    end_idx = min(start_idx + reviews_per_page, total_reviews)
    current_reviews = list(originalReviews.items())[start_idx:end_idx]

    st.write(f"Page {current_page} of {total_pages}")

    # Display Reviews
    for key, review2 in current_reviews:
        date = review2.get("Date", "No date is present")
        reviewText = review2.get("Review", "No Information for the review is present")
        Overall = review2.get("Overall", 0)
        food = review2.get("Food", 0)
        service = review2.get("Service", 0)
        ambience = review2.get("Ambience", 0)
        
        highlighted_review = f"""
        <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <p><strong><span style="font-weight: bold;color: black;">Dined on </strong><span style='color:black;'>{date}.</span></p>
            <p><span style="font-weight: bold;color: black;">Overall {Overall}. Food {food}. Ambience {ambience}. Service {service}.</span></p>
            <p><strong><span style="font-weight: bold;color: black;">Original Review: </strong><span style='color:black;'>{reviewText}.</span></p>
        </div>
        """

        st.markdown(f'{key}: ', unsafe_allow_html=True)
        st.markdown(highlighted_review, unsafe_allow_html=True)

def food_page(restaurantName = "FANG"):
    reviews_per_page = 10
    # Load data once and store in session state
    st.subheader(f"Restaurant Name: {restaurantName}")
    st.html(f"<h3> Analysis of Reviews</h3>")
    if "foodReviews" not in st.session_state:
        st.session_state.originalReviews = loadDataFromJson(restaurantName)
        st.session_state.foodReviews = loadDataFromJson(f'{restaurantName}Sentiment')

    originalReviews = st.session_state.originalReviews
    foodReviews = st.session_state.foodReviews
    total_reviews = len(originalReviews)
    total_pages = (total_reviews // reviews_per_page) + (1 if total_reviews % reviews_per_page != 0 else 0)
    # Select the current page
    current_page = st.number_input("Select Page:", min_value=1, max_value=total_pages, value=1, step=1)

    # Calculate the range of reviews to show
    start_idx = (current_page - 1) * reviews_per_page
    end_idx = start_idx + reviews_per_page

    # Slice the reviews for the current page
    current_reviews = list(zip_longest(foodReviews.items(), originalReviews.items(), fillvalue=None))[start_idx:end_idx]

    # Display analyzedReviews for the current page
    if current_reviews:
        st.write(f"Page {current_page} of {total_pages}")
        for (key, review), (key2, review2) in current_reviews:
            # Extract data
            food_quality = review.get("food_quality", "No information available.")
            date = review2.get("Date", "No date is present")
            reviewText = review2.get("Review", "No Information for the review is present")
            if food_quality == "":
                food_quality = "No review given by the Customer"
        
            highlighted_review = f"""
                <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <p><strong><span style="font-weight: bold;color: black;">Original Review: </strong><span style='color:black;'>{reviewText}.</span></p>
                    <p><strong><span style="font-weight: bold;color: black;">Dined on </strong><span style='color:black;'>{date}.</span></p>
                    <p><strong><span style="font-weight: bold;color: black;">Food Quality: </strong><span style="color:#333388;">  {food_quality}.</span></p>
                </div>
                """

            # Render the review with highlighted sections
            st.markdown(f'{key}: ', unsafe_allow_html=True)
            st.markdown(highlighted_review, unsafe_allow_html=True)

def service_page(restaurantName = "FANG"):
    reviews_per_page = 10
    # Load data once and store in session state
    st.subheader(f"Restaurant Name: {restaurantName}")
    st.html(f"<h3> Analysis of Service</h3>")
    if "foodReviews" not in st.session_state:
        st.session_state.originalReviews = loadDataFromJson(restaurantName)
        st.session_state.foodReviews = loadDataFromJson(f'{restaurantName}Sentiment')

    originalReviews = st.session_state.originalReviews
    foodReviews = st.session_state.foodReviews
    total_reviews = len(originalReviews)
    total_pages = (total_reviews // reviews_per_page) + (1 if total_reviews % reviews_per_page != 0 else 0)
    # Select the current page
    current_page = st.number_input("Select Page:", min_value=1, max_value=total_pages, value=1, step=1)

    # Calculate the range of reviews to show
    start_idx = (current_page - 1) * reviews_per_page
    end_idx = start_idx + reviews_per_page

    # Slice the reviews for the current page
    current_reviews = list(zip_longest(foodReviews.items(), originalReviews.items(), fillvalue=None))[start_idx:end_idx]

    # Display analyzedReviews for the current page
    if current_reviews:
        st.write(f"Page {current_page} of {total_pages}")
        for (key, review), (key2, review2) in current_reviews:
            # Extract data
            service_quality = review.get("service_quality", "No information available.")
            date = review2.get("Date", "No date is present")
            reviewText = review2.get("Review", "No Information for the review is present")
            if service_quality == "":
                service_quality = "No review given by the Customer"
            highlighted_review = f"""
                <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <p><strong><span style="font-weight: bold;color: black;">Original Review: </strong><span style='color:black;'>{reviewText}.</span></p>
                    <p><strong><span style="font-weight: bold;color: black;">Dined on </strong><span style='color:black;'>{date}.</span></p>
                    <p><strong><span style="font-weight: bold;color: black;">Service Quality: </strong><span style="color: #F59E0B;">{service_quality}.</span></p>
                </div>
            """

            # Render the review with highlighted sections
            st.markdown(f'{key}: ', unsafe_allow_html=True)
            st.markdown(highlighted_review, unsafe_allow_html=True)

    
    else:
        st.write("No analyzed Reviews found for this restaurant.")

def restaurant_sentiment_page(restaurantName = "FANG"):
    reviews_per_page = 10
    # Load data once and store in session state
    st.subheader(f"Restaurant Name: {restaurantName}")
    st.html(f"<h3> Analysis of Reviews</h3>")
    if "analyzedReviews" not in st.session_state:
        st.session_state.originalReviews = loadDataFromJson(restaurantName)
        st.session_state.analyzedReviews = loadDataFromJson(f'{restaurantName}Sentiment')

    originalReviews = st.session_state.originalReviews
    analyzedReviews = st.session_state.analyzedReviews
    total_reviews = len(originalReviews)
    total_pages = (total_reviews // reviews_per_page) + (1 if total_reviews % reviews_per_page != 0 else 0)
    # Select the current page
    current_page = st.number_input("Select Page:", min_value=1, max_value=total_pages, value=1, step=1)

    # Calculate the range of reviews to show
    start_idx = (current_page - 1) * reviews_per_page
    end_idx = start_idx + reviews_per_page

    # Slice the reviews for the current page
    current_reviews = list(zip_longest(analyzedReviews.items(), originalReviews.items(), fillvalue=None))[start_idx:end_idx]

    # Display analyzedReviews for the current page
    if current_reviews:
        st.write(f"Page {current_page} of {total_pages}")
        for (key, review), (key2, review2) in current_reviews:
            # Extract data
            food_quality = review.get("food_quality", "No information available.")
            service_quality = review.get("service_quality", "No information available.")
            overall_sentiment = review.get("overall_sentiment", "No sentiment available.")
            date = review2.get("Date", "No date is present")
            reviewText = review2.get("Review", "No Information for the review is present")
            style = ""
            if overall_sentiment == "" and food_quality == "" and service_quality == "":
                highlighted_review = f"""
                <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <p><strong><span style="font-weight: bold;color: black;">Original Review: </strong><span style='color:black;'>{reviewText}.</span></p>
                    <p><strong><span style="font-weight: bold;color: black;">Dined on </strong><span style='color:black;'>{date}.</span></p>
                    <p><strong><span style="font-weight: bold;color: black;">Due to API issue the response cannot be extracted. </strong></p>
                </div>
            """
            else:
                if food_quality == "":
                    food_quality = "No review given by the Customer"
                if service_quality == "":
                    service_quality = "No review given by the Customer"
                if overall_sentiment != "":
                    style, imageTag = editColorOfSentiment(overall_sentiment)
            
                highlighted_review = f"""
                    <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <p><strong><span style="font-weight: bold;color: black;">Original Review: </strong><span style='color:black;'>{reviewText}.</span></p>
                        <p><strong><span style="font-weight: bold;color: black;">Dined on </strong><span style='color:black;'>{date}.</span></p>
                        <p><strong><span style="font-weight: bold;color: black;">Food Quality: </strong><span style="color:#333388;">  {food_quality}.</span></p>
                        <p><strong><span style="font-weight: bold;color: black;">Service Quality: </strong><span style="color: #F59E0B;">{service_quality}.</span></p>
                        <p><strong><span style="font-weight: bold;color: black;">Overall Sentiment: </strong>{style}{overall_sentiment.capitalize()}</span></p>
                    </div>
                """

            # Render the review with highlighted sections
            st.markdown(f'{key}: ', unsafe_allow_html=True)
            st.markdown(highlighted_review, unsafe_allow_html=True)

    
    else:
        st.write("No analyzed Reviews found for this restaurant.")

# Main app logic
def main():
    st.sidebar.title("REVIEW SIDEBAR")  # Add a sidebar for better UI
    st.sidebar.write("Choose a page to navigate:")
    # Dropdown for additional options
    option = st.sidebar.selectbox(
        "More Options",
        ("Select a page", "Food Reviews", "Service Reviews", "Restaurant Sentiment","Scrapped Reviews")
    )

    if option == "Food Reviews":
        food_page()
    elif option == "Service Reviews":
        service_page()
    elif option == "Restaurant Sentiment":
        restaurant_sentiment_page()
    else:
        reviews_page()


# Run the app
if __name__ == "__main__":
    main()
