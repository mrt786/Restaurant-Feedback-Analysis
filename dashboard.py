import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta
from itertools import zip_longest  # to iterate in the uneven length of dictsfrom
from dataScrapping import*
from sentimentAnalysis import*

st.title("RESTAURANT FEEDBACK ANALYSIS")
# Function to load data from a JSON file
def loadDataFromJson(restaurantName):
    try:
        with open(f'{restaurantName}.json', 'r') as file:
            loadData = json.load(file)
            return loadData,restaurantName
    except Exception as e:
        st.warning(f"Error in loading file is: {e}, Loading data from the FANG.json")
        with open('FANG.json', 'r') as file:
            loadData = json.load(file)
            return loadData,"FANG"

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

def performSentimentAnalysis():
    st.html(f"<h3 style= 'text-align: center'> Perform Sentiment Analysis </h3>")
    resturantName = st.text_input("Enter name of the Restaurant")
    reviewsStore,resturantName = loadDataFromJson(resturantName)
    i = 0
    temp = {}
    for reviewDict in reviewsStore:
        try:
            response = returnLLMResponse(reviewsStore[reviewDict]['Review'])
            # convert into a dict format from string i.e first it is a dict present in string '{}'
            response =  json.loads(response)
            temp[f"Response{i}"] = response
        except Exception as e:
                print(f"Error: {e}")
                temp2 = {}
                temp2["food_quality"] = ""
                temp2["service_quality"] = ""
                temp2["overall_sentiment"] = ""
                temp[f"Response{i}"] = temp2
        i += 1
                        
    with open(f"{resturantName}Sentiment.json",'w') as file:
            json.dump(temp,file,indent = 5)

# Define functions for each page
def reviews_page(restaurantName="FANG"):
    reviews_per_page = 10

    # Load data once and store in session state
    st.html(f"<h3 style= 'text-align: center'> Original Reviews Page </h3>")
    if "originalReviews" not in st.session_state:
        st.session_state.originalReviews,restaurantName = loadDataFromJson(restaurantName)
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
    st.html(f"<h3 style= 'text-align: center'> Analysis of Food Reviews</h3>")
    if "foodReviews" not in st.session_state:
        st.session_state.originalReviews,restaurantName = loadDataFromJson(restaurantName)
        st.session_state.foodReviews,temp = loadDataFromJson(f'{restaurantName}Sentiment')

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
    st.html(f"<h3 style= 'text-align: center'> Analysis of Service Reviews</h3>")
    if "foodReviews" not in st.session_state:
        st.session_state.originalReviews,restaurantName = loadDataFromJson(restaurantName)
        st.session_state.foodReviews,temp = loadDataFromJson(f'{restaurantName}Sentiment')

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
    st.html(f"<h3 style= 'text-align: center'> Analysis of Reviews</h3>")
    if "analyzedReviews" not in st.session_state:
        st.session_state.originalReviews,restaurantName = loadDataFromJson(restaurantName)
        st.session_state.analyzedReviews,temp = loadDataFromJson(f'{restaurantName}Sentiment')

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

def formatatData(dataFrame):
    formatted_data = []
    for index, (key, review) in enumerate(dataFrame.items(), start=1):
        formatted_record = {
            "Record": index,  # Sequential numbering
            "Date": review.get("Date", ""),
            "Review": review.get("Review", ""),
            "Overall": review.get("Overall", ""),
            "Food": review.get("Food", ""),
            "Service": review.get("Service", ""),
            "Ambience": review.get("Ambience", ""),
        }
        formatted_data.append(formatted_record)
    return formatted_data


def convert_date(date_str):
    try:
        # Check if the date is already in correct format
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        return parsed_date.strftime("%B %d, %Y")
    except ValueError:
        # Handle relative dates
        today = datetime.today()
        if date_str == "today":
            return today.strftime("%B %d, %Y")
        elif "ago" in date_str:
            days_ago = int(date_str.split(" ")[0])
            target_date = today - timedelta(days=days_ago)
            return target_date.strftime("%B %d, %Y")
        else:
            # If the format is unrecognized, return as is
            return date_str

# Apply conversion only to rows with incorrect formats

def compiteterAnalysis():
    st.html("<h3 style= 'text-align: center'>Compiteter Analysis VIA Ratings</h3>")
    compiteterName = ""
    yourRestName = ""
    with st.form("Compiteter Scrapping Form", clear_on_submit=True):
        compiteterUrl = st.text_input("Paste Url of Compiteter", key="compiteter_url_input")
        yourResturantUrl = st.text_input("Your Restaurant Url", key="your_restaurant_url_input")
        submit = st.form_submit_button("Scrap")
        if submit and compiteterUrl and yourResturantUrl:
            compiteterName = scrapData(compiteterUrl)
            yourRestName = scrapData(yourResturantUrl)
        elif submit:
            st.warning("Please enter valid URL's!!!")
            return
        st.write(f"Compiteter Name: {compiteterName}")
        st.write(f"Your Restaurant: {yourRestName}")
        
    # compiteterName = "AKIKOS"
    # yourRestName = "FANG"
    if compiteterName != "" and yourRestName != "" and yourRestName != compiteterName:
        compDf,_ = loadDataFromJson(f'{compiteterName}')
        yourDf,_ = loadDataFromJson(f'{yourRestName}')
        compDf = pd.DataFrame(data = formatatData(compDf)) 
        compDf.set_index("Record", inplace=True)
        yourDf  = pd.DataFrame(data =formatatData(yourDf))
        yourDf.set_index("Record", inplace=True)
        yourDf["Date"] = yourDf["Date"].apply(
            lambda x: convert_date(x) if "ago" in x or x == "today" else x
        )
        compDf["Date"] = compDf["Date"].apply(
            lambda x: convert_date(x) if "ago" in x or x == "today" else x
        )


        temp = pd.to_datetime(yourDf['Date'], format="%B %d, %Y")
        # extract the day , month , year
        yourDf['Day'] = temp.dt.day
        yourDf["Month"] = temp.dt.month_name()
        yourDf["Year"] = temp.dt.year
        

        temp = pd.to_datetime(compDf['Date'], format="%B %d, %Y")
        compDf['Day'] = temp.dt.day
        compDf["Month"] = temp.dt.month_name()
        compDf["Year"] = temp.dt.year        

        colsToConvert = ['Food', 'Service', 'Overall', 'Ambience', 'Year']
        # Use pd.to_numeric with errors='coerce' to handle invalid data gracefully
        for column in colsToConvert:
            compDf[column] = pd.to_numeric(compDf[column], errors='coerce')
            yourDf[column] = pd.to_numeric(yourDf[column], errors='coerce')

        st.write(f"Some records of {compiteterName}",compDf.sample(6))
        st.write(f"Some records of {yourRestName}",yourDf.sample(6))
        def generateTimeGraph(typeOfRating):
            st.write(f"{yourRestName}: SkyBlue")
            st.write(f"{compiteterName}: Red")
            yourRatings = yourDf.groupby("Year")[typeOfRating].mean()
            compiteterRating = compDf.groupby("Year")[typeOfRating].mean()
            fig = plt.figure(figsize=(10, 6))
            yourRatings.plot(kind='line', color='skyblue',marker = 'o')
            compiteterRating.plot(kind='line', color='red',marker = 'o')
            plt.title(f'{typeOfRating} Ratings by Year')
            plt.xlabel('Year')
            plt.ylabel('Average Rating')
            plt.grid(True,alpha = 1)
            plt.legend(title="Categories", fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

        generateTimeGraph("Overall")
        generateTimeGraph("Food")
        generateTimeGraph("Service")
        generateTimeGraph("Ambience")

    
def main():
    st.sidebar.html("<h1 style = 'text-align: center'>Restaurant Name: FANG</h1>")
    st.sidebar.write("Choose a page to navigate:")
    # Dropdown for additional options
    option = st.sidebar.selectbox(
        "Options",
        ("Select a page", "Food Reviews", "Service Reviews", "Restaurant Sentiment","Scrapped Reviews","Compiteter Analysis","Perform Sentiment Analysis")
    )

    if option == "Food Reviews":
        food_page()
    elif option == "Service Reviews":
        service_page()
    elif option == "Restaurant Sentiment":
        restaurant_sentiment_page()
    elif option == "Compiteter Analysis":
        compiteterAnalysis()
    elif option == "Perform Sentiment Analysis":
        performSentimentAnalysis()
    else:
        reviews_page()

# Run the app
if __name__ == "__main__":
    main()
