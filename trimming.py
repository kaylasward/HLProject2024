import lingpy.align
import lingrex.trimming
from read_tab_files import TabFileReader
from lingpy.align.multiple import mult_align
import lingpy
import lingrex
import numpy as np


def trim(cog_set,threshold:float,strategy:str):
    """aligns cognate set by lingpy's multi_align, and then trims items of the
    set if the percent of members missing a position exceeds the threshold.
    Trims from ends or all members depending on given strategy.

    Args:
        cog_set: set of words to be aligned and trimmed.
        df: dataframe to be altered
        threshold (float): percentage of members needed for index to be trimmed
        strategy (str): valid values "gap-oriented" or "core-oriented"
    Returns:
        pd.DataFrame: dataframe with all items trimmed.
    """
    dense_cog = cog_set[cog_set != ''].to_list()
    
    aligned_dense = mult_align(dense_cog)
    
    s = lingrex.trimming.Sites(aligned_dense)
    trim_site = s.trimmed(strategy=strategy,threshold=threshold)
    trimmed_words = []
    for i in range(len(trim_site[0])):
        trimmed_words.append(''.join(site[i] for site in trim_site if site and site[i] !="-"))
        
    return trimmed_words
    
    

def trim_all(form_data_frame, threshold=.5, strategy='core-oriented'):
    """dataframe iterator for trimming.

    Args:
        form_data_frame (_type_): dataframe of IPA forms of language columns by concept rows
        threshold (float, optional): percentage of members needed for index to be trimmed. Defaults to .5.
        strategy (str, optional): valid values "gap-oriented" or "core-oriented". Defaults to 'core-oriented'.

    Returns:
        pd.DataFrame: dataframe with all items trimmed.
    """
    #Replaces apostrophes in input with primary stress marker in IPA (lingpy breaks without this)
    form_df_fixed = form_data_frame.replace("'","ˈ",regex=True)
    form_df_fixed = form_df_fixed.replace(":","ː",regex=True) #same but for length
    #other items that throw errors, not sure how to handle this in a principled way since 
    #I can't find their function in IPA, so just removing them.
    df = form_df_fixed.replace("[;\(\)\[\]]","",regex=True)  
    
    for i, row in df.iterrows():
        if i>0:
            trimmed_words = trim(row[1:],threshold,strategy)
            iter_trim_words = iter(trimmed_words)
            for item in row[1:]:            #start after concept
                if item != "":
                    added = next(iter_trim_words)
                    df = df.where(df != item, added)
    
    return df
            
    
def main():#
    """
    tests for trim function 
    
    """
    #Barbacoan data
    barb_cognacy = TabFileReader.tab_reader(               
        "chl2024_barbacoandata/chl2023_barbacoan_cognacy.tab"
        )
    barb_forms = TabFileReader.tab_reader(                  
        "chl2024_barbacoandata/chl2023_barbacoan_forms.tab"
        )
    #Eastern-Austronesian data
    eau_cognacy = TabFileReader.tab_reader(
        "chl2024_eastern-austronesiandata/chl2023_eastern-austronesian_cognacy.tab"
        )
    eau_forms = TabFileReader.tab_reader(
        "chl2024_eastern-austronesiandata/chl2023_eastern-austronesian_forms.tab"
        )
    #Indo-European data
    ie_cognacy = TabFileReader.tab_reader(
        "chl2024_iedata/chl2023_iedata_cognacy.tab"
        )
    ie_forms = TabFileReader.tab_reader(
        "chl2024_iedata/chl2023_iedata_forms.tab"
        )
    
    new_df = trim_all(ie_forms)
    
    from clustering import Clustering
    ie_clusters = Clustering(ie_forms, ie_cognacy, threshold=0.8)
    trimmed_ie_clusters = Clustering(new_df, ie_cognacy, threshold=0.8)
    print("Indo-European        .8  ", ie_clusters.score())
    print("trimmed Indo-European.8  ", trimmed_ie_clusters.score())
    
    barb_trim_df = trim_all(barb_forms)
    
    barb_clusters = Clustering(barb_forms, barb_cognacy, threshold=0.8)
    trimmed_barb_clusters = Clustering(barb_trim_df, barb_cognacy, threshold=0.8)
    print("Barbacoan            .8  ", barb_clusters.score())
    print("trimmed Barbacoan    .8  ", trimmed_barb_clusters.score())
    
    eau_trim_df = trim_all(eau_forms)
    
    eau_clusters = Clustering(eau_forms, eau_cognacy, threshold=0.6)
    trimmed_eau_clusters = Clustering(eau_trim_df, eau_cognacy, threshold=0.6)
    print("Eastern Austronesian .6  ", eau_clusters.score())
    print("Eastern Austronesian .6  ", trimmed_eau_clusters.score())
    
    #tests for what became the above functions.
    #print(ie_forms.iloc[32]) 
    ie_fixed = ie_forms.replace("'","ˈ",regex=True)
    #for row in ie_fixed.iterrows():
        #contents = row[1][1:]
    row = ie_fixed.iloc[1][1:]
    print()
    print(row)
    no_empty = row[row != ''].to_list()
    print (no_empty)
    
    aligned_no_empty = mult_align(no_empty)
    
    s = lingrex.trimming.Sites(aligned_no_empty)
    print(s)
    trim_site = s.trimmed(strategy='gap-oriented')
    print(list(trim_site))
    trimmed_words = []
    for i in range(len(trim_site[0])):
        trimmed_words.append(''.join(site[i] for site in trim_site if site and site[i] !="-"))
    print(trimmed_words)
    iter_trim_words = iter(trimmed_words)
    for item in row[1:]:            #start after concept
        if item != "":
            added = next(iter_trim_words)
            ie_fixed = ie_fixed.where(ie_fixed != item, added)
    
    print(ie_fixed.iloc[1])
    
    

if __name__ == "__main__":
    main()