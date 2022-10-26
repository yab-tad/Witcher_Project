import numpy as np
import pandas as pd
import spacy
import networkx as nx
import matplotlib.pyplot as plt



def named_entity_relationship(file_name):
    """
    Function to process text form a text file (.txt) using Spacy.
    
    Params :
    file_name :- name of a text file as string
    
    Returns : a processed doc file using Spacy English language model
    """
    
    # Loading Spacy English language model
    NER = spacy.load("en_core_web_sm")
    book_text = open(file_name).read()
    book_doc = NER(book_text)
    
    return book_doc


def get_namedEntity_list_perSentence(book_doc):
    """
    Extract a list of entities per sentence of a Spacy document and store in a DataFrame.
    
    Params : 
    book_doc :- a Spacy processed document
    
    Returns : a DataFrame with sentences and their corresponding list of recognised entities as its components
    """
    
    sent_entity_df = []
    
    # Loop through each sentence, and store named entity list along the way
    for sent in book_doc.sents:
        entity_list = [ent.text for ent in sent.ents]
        sent_entity_df.append({"Sentence" : sent, "Entities" : entity_list})
        
    sent_entity_df = pd.DataFrame(sent_entity_df)
    
    return sent_entity_df


def filter_entity(ent_list, character_df):
    """
    Function that filters out entities recognised but don't subscribe to the character list.
    
    Params : 
    ent_list :- list of entities per each sentence.
    character_df :- DataFrame containing characters' full and first name
    
    Returns : a list of characters corresponding to each sentence, and an empty list for those entity relations that don't confirm to the list of characters' full or first name
    """
    
    return [ent for ent in ent_list
            if ent in list(character_df.character_firstName)
            or ent in list(character_df.character)]


def create_relationships(df, window_size=5):
    """
    Creates a DataFrame of relationships between characters based on the proximity of their presence in sentence within a given window size.
    
    Params : 
    df :- a filtered DataFrame containing character entities with their corresponding sentence they are located in.
    window_size :- proximity measure set for adjacent characters within a sentence viable enough to create relationship. By default set to a size of 5.
    
    Returns : a DataFrame depicting a relationship between characters and their relationship directionality by classifying them under "source" and "target" column.
    """
    
    relationship = []
    
    for i in range(df.index[-1]):
        end_window = min(i + window_size, df.index[-1])
        char_list = sum((df.loc[i:end_window].character_entities), [])
        
        # Remove duplicated characters that are next to each other
        char_unique = [char_list[i] for i in range(len(char_list))
                       if (i==0) or char_list[i] != char_list[i-1]]
        
        # Map Relationships
        if len(char_unique) > 1:
            for index, source in enumerate(char_unique[:-1]):
                target = char_unique[index + 1]
                relationship.append({"Source" : source, "Target" : target})
                
    # Making our relationship a DataFrame
    relationship_df = pd.DataFrame(relationship)
        
    # Sort by row for each column so it can help us create a weight out of the duplicated [Source -> Target] relationships
    relationship_df = pd.DataFrame(np.sort(relationship_df.values, axis=1), columns=relationship_df.columns)
        
    # Creating a 'weight' column, which we then assign a value of 1 to every relationship present, and group by the Source -> Target to get the weighted sum depicting relationships' frequency.
    relationship_df['Weight'] = 1
    relationship_df = relationship_df.groupby(["Source", "Target"], sort=False, as_index=False).sum()
        
    return relationship_df