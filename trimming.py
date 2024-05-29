import lingpy.align
import lingrex.trimming
from read_tab_files import TabFileReader
from lingpy.align.multiple import mult_align
import lingpy
import lingrex
import numpy as np
import pandas as pd


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
    
    #scoring stuff
    new_df = trim_all(ie_forms,.75)
    
    from clustering import Clustering
    #ie_clusters = Clustering(ie_forms, ie_cognacy, threshold=0.8)
    #trimmed_ie_clusters = Clustering(new_df, ie_cognacy, threshold=0.8)
    #print("Indo-European        .8  ", ie_clusters.score())
    #print("trimmed Indo-European.8  ", trimmed_ie_clusters.score())
    
    #barb_trim_df = trim_all(barb_forms,.75)
    
    #barb_clusters = Clustering(barb_forms, barb_cognacy, threshold=0.8)
    #trimmed_barb_clusters = Clustering(barb_trim_df, barb_cognacy, threshold=0.8)
    #print("Barbacoan            .8  ", barb_clusters.score())
    #print("trimmed Barbacoan    .8  ", trimmed_barb_clusters.score())
    
    #eau_trim_df = trim_all(eau_forms)
    
    #eau_clusters = Clustering(eau_forms, eau_cognacy, threshold=0.6)
    #trimmed_eau_clusters = Clustering(eau_trim_df, eau_cognacy, threshold=0.6)
    #print("Eastern Austronesian .6  ", eau_clusters.score())
    #print("Eastern Austronesian .6  ", trimmed_eau_clusters.score())
    
    from Threshold_Optimizing_Plot import get_score_lists, plot
    
    thresholds = [0,.1,.2,.3,.4,.5,.6,.7,.8,.9, 1]
    
    ie_score_df = pd.DataFrame(columns=thresholds)
    barb_score_df = pd.DataFrame(columns=thresholds)
    eau_score_df = pd.DataFrame(columns=thresholds)
    
    ie_gap_score_df = pd.DataFrame(columns=thresholds)
    barb_gap_score_df = pd.DataFrame(columns=thresholds)
    eau_gap_score_df = pd.DataFrame(columns=thresholds)
    
    for i in thresholds:
        new_df = trim_all(ie_forms,i)
        barb_trim_df = trim_all(barb_forms,i)
        eau_trim_df = trim_all(eau_forms,i)

        barb_precisions, barb_recalls, barb_fscores = get_score_lists(
            barb_trim_df, barb_cognacy, thresholds)
        eau_precisions, eau_recalls, eau_fscores = get_score_lists(
            eau_trim_df, eau_cognacy, thresholds)
        ie_precisions, ie_recalls, ie_fscores = get_score_lists(
            new_df, ie_cognacy, thresholds)
        barb_score_df.loc[i]=barb_fscores
        ie_score_df.loc[i]=ie_fscores
        eau_score_df.loc[i]=eau_fscores
        
        new_gap_df = trim_all(ie_forms,i)
        barb_gap_trim_df = trim_all(barb_forms,i)
        eau_gap_trim_df = trim_all(eau_forms,i)

        barb_precisions, barb_recalls, barb_gap_fscores = get_score_lists(
            barb_gap_trim_df, barb_cognacy, thresholds)
        eau_precisions, eau_recalls, eau_gap_fscores = get_score_lists(
            eau_gap_trim_df, eau_cognacy, thresholds)
        ie_precisions, ie_recalls, ie_gap_fscores = get_score_lists(
            new_gap_df, ie_cognacy, thresholds)
        barb_gap_score_df.loc[i]=barb_gap_fscores
        ie_gap_score_df.loc[i]=ie_gap_fscores
        eau_gap_score_df.loc[i]=eau_gap_fscores
        break
    print("barb")
    print(barb_score_df)
    print(barb_gap_score_df)
    print("ie")
    print(ie_score_df)
    print(ie_gap_score_df)
    print("eau")
    print(eau_score_df)
    print(eau_gap_score_df)
    
    
    #plot(ie_precisions, ie_recalls, ie_fscores, "Indo-European-trimmed")
    #plot(barb_precisions, barb_recalls, barb_fscores, "Barbacoan-trimmed")
    #plot(eau_precisions, eau_recalls, eau_fscores, "Eastern Austronesian-trimmed")
    
    #tests for what became the above functions.
    #print(ie_forms.iloc[32]) 
    ie_fixed = ie_forms.replace("'","ˈ",regex=True)
    #for row in ie_fixed.iterrows():
        #contents = row[1][1:]
    idx = 32
    row = ie_fixed.iloc[idx][1:]
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
    
    print(ie_fixed.iloc[idx])
    
    

if __name__ == "__main__":
    main()