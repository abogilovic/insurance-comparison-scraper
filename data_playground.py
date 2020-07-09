import pandas as pd


#df = pd.DataFrame(stores, columns=['Store Name', 'Address', 'Address 2', 'City', 'Province', 'Postal Code', 'Phone Number', 'Website'])
#df.to_csv("./output.csv", sep=',',index=False)

# df1 = pd.read_csv('./output1.csv.csv')
# df.drop(df.tail(2293).index,inplace=True)
# df.to_csv("./output1.csv", sep=',',index=False)


df = pd.read_csv('./input_data_example.csv', sep=';')
df['car_price_quote_dict'] = ""
data = [
{
    "company_image":"https://forsikringsguiden.dk/assets/images/companies/13.svg", 
    "total_price": 6257.0,
    "discounted_price": 6257.0,
    "deductible": 4500.0,
    "configuration_result": 
        {
            "is_allrisk": True, 
             "is_ext_glass": False, 
             "is_road_assistance": False, 
             "is_parking": False, 
             "is_young_driver": False, 
             "is_free_claim": False, 
             "is_driver_cov": False, 
             "is_fixed_price": True, 
             "is_leasing": False
        }, 
    "rank": 4,
    "configuration_id": 32
},
{
    "company_image":"https://forsikringsguiden.dk/assets/images/companies/44.svg", 
    "total_price": 9556.0,
    "discounted_price": 9556.0, 
    "deductible": 5950.0,
    "configuration_result":
        {
            "is_allrisk": True, 
             "is_ext_glass": False, 
             "is_road_assistance": False, 
             "is_parking": False, 
             "is_young_driver": False, 
             "is_free_claim": False, 
             "is_driver_cov": False, 
             "is_fixed_price": False, 
             "is_leasing": False
        }, 
    "rank": 5,
    "configuration_id": 32
}]

df.at[0, 'car_price_quote_dict'] = data

print(df['car_price_quote_dict'][0])
print(df['car_price_quote_dict'][0][0]['rank'])

df.to_csv("./mmm.csv", sep=';', index=False)

#df2 = pd.read_csv('./output2.csv')
#df3 = pd.read_csv('./output3.csv')
#df4 = pd.read_csv('./output4.csv')
#df5 = pd.read_csv('./output5.csv')
#df6 = pd.read_csv('./output6.csv')
#df7 = pd.read_csv('./output7.csv')
#df8 = pd.read_csv('./output8.csv')
#df9 = pd.read_csv('./output9.csv')

#df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9])
#df_clean = df1.drop_duplicates()
#df_clean.to_csv("./outputcina.csv", sep=',',index=False)
