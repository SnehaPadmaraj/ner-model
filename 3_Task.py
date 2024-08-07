import streamlit as st
import pandas as pd
import spacy
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import seaborn as sns
from sklearn.decomposition import PCA
from collections import defaultdict
from sklearn.decomposition import LatentDirichletAllocation as LDA
from wordcloud import WordCloud


#set up page config
st.set_page_config(page_title="Task", page_icon="", layout="centered", initial_sidebar_state="expanded")

nlp = spacy.load('en_core_web_sm')

#preprocessing function to extract header info and body
def extract_entities(text):
    persons = []
    orgs = []
    locations = []
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            persons.append(ent.text)
        elif ent.label_ == "ORG":
            orgs.append(ent.text)
        elif ent.label_ == "GPE":
            locations.append(ent.text)
    return persons, orgs, locations

def parse_email(message):
    headers, body = message.split('\n\n', 1)
    headers = dict([line.split(': ', 1) for line in headers.split('\n') if ': ' in line])
    return headers, body

#load the dataset
emails = pd.read_csv('./dataset/emails_sample.csv')
emails['parsed'] = emails['message'].apply(parse_email)
emails['headers'] = emails['parsed'].apply(lambda x: x[0])
emails['body'] = emails['parsed'].apply(lambda x: x[1])
emails[['persons', 'orgs', 'locations']] = pd.DataFrame(emails['body'].apply(extract_entities).tolist(), index=emails.index)

def create_scatter_plot(data, title):
    #TF-IDF matrix for entities 
    data_str = data.apply(lambda x: ' '.join(x))
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data_str)

    #K-means clustering
    kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
    clusters = kmeans.labels_

    #dimensionality reduction with PCA 
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X.toarray())

    plt.figure(figsize=(12, 12))
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap=plt.cm.jet, alpha=0.6)
    plt.title(title)
    plt.xlabel('Entity Feature 1')
    plt.ylabel('Entity Feature 2')
    cluster_labels = [f'Cluster {i+1}' for i in range(len(set(clusters)))]
    plt.legend(handles=scatter.legend_elements()[0], labels=cluster_labels, title="Clusters")
    st.pyplot(plt)

def lda_topic_modeling(entities):
    #preparing the data for LDA
    data_str = entities.apply(lambda x: ' '.join(x))
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data_str)

    #LDA
    lda = LDA(n_components=5, random_state=0)
    lda.fit(X)

    #display the topics
    topics = defaultdict(list)
    for idx, topic in enumerate(lda.components_):
        topic_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]]
        topics[f'Topic {idx+1}'] = topic_words

    return topics


def visualize_topics(topics):
    st.subheader("LDA Topics Visualization")
    for topic, words in topics.items():
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(topic)
        st.pyplot(plt)

def task():
    st.title('Task')
    st.write("### Visualize which email addresses co-occur with which entities in the text.")

    #entity tag selector
    entity_tag = st.selectbox("Select entity tag", ["PERSON", "ORG", "GPE"])

    #filtering the entities based on the selected tag
    if entity_tag == "PERSON":
        entities = emails['persons']
    elif entity_tag == "ORG":
        entities = emails['orgs']
    elif entity_tag == "GPE":
        entities = emails['locations']

    #most common entities 
    entity_counts = {}
    for ents in entities:
        for ent in ents:
            if ent not in entity_counts:
                entity_counts[ent] = 0
            entity_counts[ent] += 1

    sorted_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)
    top_entities = sorted_entities[:10]

    entity_names = [entity[0] for entity in top_entities]
    entity_values = [entity[1] for entity in top_entities]

  #network of popular entities and email addresses 
    st.subheader("Connections Between Popular Entities and Email Addresses")
    plt.figure(figsize=(12, 12))
    G = nx.Graph()

    for entity, _ in top_entities:
        G.add_node(entity, type='entity')
        for i, row in emails.iterrows():
            from_addr = row['headers'].get('From', '')
            if entity in row['persons'] or entity in row['locations'] or entity in row['orgs']:
                G.add_edge(from_addr, entity)

    pos = nx.spring_layout(G, k=0.5)
    node_colors = ['skyblue' if G.nodes[node].get('type') != 'entity' else 'orange' for node in G.nodes()]
    node_sizes = [500 if G.nodes[node].get('type') != 'entity' else 1000 for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=10, font_color="black", font_weight="bold")
    plt.title("Connections Between Popular Entities and Email Addresses")
    st.pyplot(plt)

    #plot bar graph for most popular entities 
    st.subheader("Top 10 Most Popular Entities")
    plt.figure(figsize=(12, 6))
    sns.barplot(x=entity_names, y=entity_values)
    plt.title(f"Top 10 Most Popular {entity_tag}s")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    #scatter plot of email addresses based on the selected entity tag
    st.subheader(f"Clustering Based on {entity_tag}s Mentioned")
    create_scatter_plot(entities, f"Email Senders Clustering Based on {entity_tag}s Mentioned")

  #Bonus Task: LDA Word Cloud Topic Modeling
    st.subheader("Bonus Task: Topic Modeling with Word Cloud")
    topics = lda_topic_modeling(entities)
    visualize_topics(topics)

# Call the task function
task()