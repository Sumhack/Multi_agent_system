import sqlite3
import pandas as pd

# Step 1: Load CSV file using pandas
csv_file = 'csv_file_path'  # replace with your CSV file path
data = pd.read_csv(csv_file)

print(data.columns)

# Step 2: Create a connection to the SQLite database (it will create a new file if it doesn't exist)
db_file = 'local_databases.db'  # name of your SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Step 3: Create table schema (based on your CSV columns)
# Assume your CSV contains 'Column Name', 'Data Type', 'Description' as headers
table_name = 'column_data'
create_table_query = f'''
CREATE TABLE IF NOT EXISTS {table_name} (
    date  DATE ,
sales  float ,
sales_from_finance  float ,
total_ad_spend  float ,
corp_Google_DISCOVERY_spend  float ,
corp_Google_DISPLAY_spend  float ,
corp_Google_PERFORMANCE_MAX_spend  float ,
corp_Google_SEARCH_spend  float ,
corp_Google_SHOPPING_spend  float ,
corp_Google_VIDEO_spend  float ,
corp_Horizon_VIDEO_TIER_1_spend  float ,
corp_Horizon_VIDEO_TIER_2_spend  float ,
corp_Horizon_VIDEO_TIER_3_spend  float ,
corp_Horizon_VIDEO_TIER_BC_spend  float ,
corp_Horizon_VIDEO_TIER_HISP_spend  float ,
corp_Horizon_VIDEO_TIER_NA_spend  float ,
corp_Horizon_VIDEO_TIER_OTT_spend  float ,
corp_Horizon_VIDEO_TIER_SYND_spend  float ,
corp_Impact_AFFILIATE_spend  float ,
corp_Meta_SOCIAL_spend  float ,
corp_Microsoft_AUDIENCE_spend  float ,
corp_Microsoft_SEARCH_CONTENT_spend  float ,
corp_Microsoft_SHOPPING_spend  float ,
local_Google_DISPLAY_spend  float ,
local_Google_LOCAL_spend  float ,
local_Google_PERFORMANCE_MAX_spend  float ,
local_Google_SEARCH_spend  float ,
local_Google_SHOPPING_spend  float ,
local_Meta_SOCIAL_spend  float ,
local_Simpli_fi_GEO_OPTIMIZED_DISPLAY_spend  float ,
local_Simpli_fi_GEO_OPTIMIZED_VIDEO_spend  float ,
local_Simpli_fi_SEARCH_DISPLAY_spend  float ,
local_Simpli_fi_SEARCH_VIDEO_spend  float ,
local_Simpli_fi_SITE_RETARGETING_DISPLAY_spend  float ,
local_Simpli_fi_SITE_RETARGETING_VIDEO_spend  float ,
stock_market_index  float ,
dollar_to_pound  float ,
interest_rates  float
)
'''
cursor.execute(create_table_query)

# Step 4: Insert data into the table
for _, row in data.iterrows():
    cursor.execute(f'''
        INSERT INTO {table_name} (date,	sales,	sales_from_finance,	total_ad_spend,	corp_Google_DISCOVERY_spend,	corp_Google_DISPLAY_spend,	corp_Google_PERFORMANCE_MAX_spend,	corp_Google_SEARCH_spend,	corp_Google_SHOPPING_spend,	corp_Google_VIDEO_spend,	corp_Horizon_VIDEO_TIER_1_spend,	corp_Horizon_VIDEO_TIER_2_spend,	corp_Horizon_VIDEO_TIER_3_spend,	corp_Horizon_VIDEO_TIER_BC_spend,	corp_Horizon_VIDEO_TIER_HISP_spend,	corp_Horizon_VIDEO_TIER_NA_spend,	corp_Horizon_VIDEO_TIER_OTT_spend,	corp_Horizon_VIDEO_TIER_SYND_spend,	corp_Impact_AFFILIATE_spend,	corp_Meta_SOCIAL_spend,	corp_Microsoft_AUDIENCE_spend,	corp_Microsoft_SEARCH_CONTENT_spend,	corp_Microsoft_SHOPPING_spend,	local_Google_DISPLAY_spend,	local_Google_LOCAL_spend,	local_Google_PERFORMANCE_MAX_spend,	local_Google_SEARCH_spend,	local_Google_SHOPPING_spend,	local_Meta_SOCIAL_spend,	local_Simpli_fi_GEO_OPTIMIZED_DISPLAY_spend,	local_Simpli_fi_GEO_OPTIMIZED_VIDEO_spend,	local_Simpli_fi_SEARCH_DISPLAY_spend,	local_Simpli_fi_SEARCH_VIDEO_spend,	local_Simpli_fi_SITE_RETARGETING_DISPLAY_spend,	local_Simpli_fi_SITE_RETARGETING_VIDEO_spend,	stock_market_index,	dollar_to_pound,interest_rates)
        VALUES (?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?)''', (row['date'],	row['sales'],	row['sales_from_finance'],	row['total_ad_spend'],	row['corp_Google_DISCOVERY_spend'],	row['corp_Google_DISPLAY_spend'],	row['corp_Google_PERFORMANCE_MAX_spend'],	row['corp_Google_SEARCH_spend'],	row['corp_Google_SHOPPING_spend'],	row['corp_Google_VIDEO_spend'],	row['corp_Horizon_VIDEO_TIER_1_spend'],	row['corp_Horizon_VIDEO_TIER_2_spend'],	row['corp_Horizon_VIDEO_TIER_3_spend'],	row['corp_Horizon_VIDEO_TIER_BC_spend'],	row['corp_Horizon_VIDEO_TIER_HISP_spend'],	row['corp_Horizon_VIDEO_TIER_NA_spend'],	row['corp_Horizon_VIDEO_TIER_OTT_spend'],	row['corp_Horizon_VIDEO_TIER_SYND_spend'],	row['corp_Impact_AFFILIATE_spend'],	row['corp_Meta_SOCIAL_spend'],	row['corp_Microsoft_AUDIENCE_spend'],	row['corp_Microsoft_SEARCH_CONTENT_spend'],	row['corp_Microsoft_SHOPPING_spend'],	row['local_Google_DISPLAY_spend'],	row['local_Google_LOCAL_spend'],	row['local_Google_PERFORMANCE_MAX_spend'],	row['local_Google_SEARCH_spend'],	row['local_Google_SHOPPING_spend'],	row['local_Meta_SOCIAL_spend'],	row['local_Simpli_fi_GEO_OPTIMIZED_DISPLAY_spend'],	row['local_Simpli_fi_GEO_OPTIMIZED_VIDEO_spend'],	row['local_Simpli_fi_SEARCH_DISPLAY_spend'],	row['local_Simpli_fi_SEARCH_VIDEO_spend'],	row['local_Simpli_fi_SITE_RETARGETING_DISPLAY_spend'],	row['local_Simpli_fi_SITE_RETARGETING_VIDEO_spend'],	row['stock_market_index'],	row['dollar_to_pound'],	row['interest_rates']))

# Step 5: Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Database '{db_file}' has been created with the table '{table_name}'.")
