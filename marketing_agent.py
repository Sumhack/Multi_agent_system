import os
import google.generativeai as genai
import sqlite3

# Connect to the local SQLite database
conn = sqlite3.connect('local_databases.db')
cursor = conn.cursor()


# Configure Gemini API key (replace 'gemini-api-key' with your actual key)
genai.configure(api_key= 'gemini-api-key')


model = genai.GenerativeModel(
        model_name='gemini-1.5-flash')
def prompt_template(input_question):
    """
    Constructs a prompt that provides the table schema and asks Gemini to generate SQL
    based on the user’s natural language question.

    Args:
        input_question (str): The user's question.

    Returns:
        Gemini response object containing the generated SQL.
    """


    prompt = f'''
    Below is the schema for the column_data table
    Column Name	Data Type	Description
date	date	Date of the sales and advertising data.
sales	float	Total sales value for the specified date.
sales_from_finance	float	Sales value reported from the finance department.
total_ad_spend	float	Total advertising spend across all platforms.
corp_Google_DISCOVERY_spend	float	Corporate ad spend on Google Discovery campaigns.
corp_Google_DISPLAY_spend	float	Corporate ad spend on Google Display Network.
corp_Google_PERFORMANCE_MAX_spend	float	Corporate ad spend on Google Performance Max campaigns.
corp_Google_SEARCH_spend	float	Corporate ad spend on Google Search campaigns.
corp_Google_SHOPPING_spend	float	Corporate ad spend on Google Shopping campaigns.
corp_Google_VIDEO_spend	float	Corporate ad spend on Google Video campaigns.
corp_Horizon_VIDEO_TIER_1_spend	float	Corporate ad spend on Horizon Tier 1 video campaigns.
corp_Horizon_VIDEO_TIER_2_spend	float	Corporate ad spend on Horizon Tier 2 video campaigns.
corp_Horizon_VIDEO_TIER_3_spend	float	Corporate ad spend on Horizon Tier 3 video campaigns.
corp_Horizon_VIDEO_TIER_BC_spend	float	Corporate ad spend on Horizon BC video campaigns.
corp_Horizon_VIDEO_TIER_HISP_spend	float	Corporate ad spend on Horizon Hispanic video campaigns.
corp_Horizon_VIDEO_TIER_NA_spend	float	Corporate ad spend on Horizon North American video campaigns.
corp_Horizon_VIDEO_TIER_OTT_spend	float	Corporate ad spend on Horizon OTT (Over-The-Top) video campaigns.
corp_Horizon_VIDEO_TIER_SYND_spend	float	Corporate ad spend on Horizon syndicated video campaigns.
corp_Impact_AFFILIATE_spend	float	Corporate ad spend on Impact Affiliate campaigns.
corp_Meta_SOCIAL_spend	float	Corporate ad spend on Meta (Facebook/Instagram) social campaigns.
corp_Microsoft_AUDIENCE_spend	float	Corporate ad spend on Microsoft Audience campaigns.
corp_Microsoft_SEARCH_CONTENT_spend	float	Corporate ad spend on Microsoft Search and Content Network campaigns.
corp_Microsoft_SHOPPING_spend	float	Corporate ad spend on Microsoft Shopping campaigns.
local_Google_DISPLAY_spend	float	Local ad spend on Google Display Network campaigns.
local_Google_LOCAL_spend	float	Local ad spend on Google Local campaigns.
local_Google_PERFORMANCE_MAX_spend	float	Local ad spend on Google Performance Max campaigns.
local_Google_SEARCH_spend	float	Local ad spend on Google Search campaigns.
local_Google_SHOPPING_spend	float	Local ad spend on Google Shopping campaigns.
local_Meta_SOCIAL_spend	float	Local ad spend on Meta (Facebook/Instagram) social campaigns.
local_Simpli_fi_GEO_OPTIMIZED_DISPLAY_spend	float	Local ad spend on Simpli.fi geo-optimized display campaigns.
local_Simpli_fi_GEO_OPTIMIZED_VIDEO_spend	float	Local ad spend on Simpli.fi geo-optimized video campaigns.
local_Simpli_fi_SEARCH_DISPLAY_spend	float	Local ad spend on Simpli.fi search display campaigns.
local_Simpli_fi_SEARCH_VIDEO_spend	float	Local ad spend on Simpli.fi search video campaigns.
local_Simpli_fi_SITE_RETARGETING_DISPLAY_spend	float	Local ad spend on Simpli.fi site retargeting display campaigns.
local_Simpli_fi_SITE_RETARGETING_VIDEO_spend	float	Local ad spend on Simpli.fi site retargeting video campaigns.
stock_market_index	float	Stock market index value on the specified date.
dollar_to_pound	float	Exchange rate from US dollars to British pounds on the specified date.
interest_rates	float	Interest rates on the specified date.

Can you provide the SQL for {input_question}? Consider only SQL syntax



    '''

    response = model.generate_content(prompt)

    return response


def final_outputs(input_question,final_output):
    """
    Uses the model to summarize the SQL result into a business-friendly answer.

    Args:
        input_question (str): Original user query.
        final_output (str): Raw SQL output (e.g., data frame as string or raw model output).

    Returns:
        Gemini response object with a natural language summary of the output.
    """
    prompt = f'''
    Instructions: You are marketing data agent for a telecom company.

    For this given
     Question : {input_question}
     This is the answer :{final_output}
    Provide summarised answer for the question with the above information


    '''
    response = model.generate_content(prompt)

    return response



def user_query(input_question):
    """
    Orchestrates the flow: takes a question, generates SQL, runs it, summarizes the result.

    Args:
        input_question (str): User's natural language query.

    Returns:
        Tuple[str, str]: A business-friendly summarized answer, and the source (hardcoded).
    """

    # Step 1: Get SQL from Gemini model
    response = prompt_template(input_question)
    pq = response.text
    

    try:
       cleaned_text = pq.replace('sql', '').replace('', '').strip()
       df = pd.read_sql_query(cleaned_text, conn)
       final_output = df.to_string(index=False)

    except Exception as e:
       final_output = pq







    ps = final_outputs(input_question, final_output)

    source = "data_file_path"

    return ps.text, source
