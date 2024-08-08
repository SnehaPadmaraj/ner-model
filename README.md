# ner-model
README.md 

What the app does 
This is a Streamlit application which extracts entities from the Enron email dataset. It will list out the entities and the entity types present in individual emails. The app also makes use of a network algorithm to visualize which email addresses co-occur with which entities in the text. It also makes use of a simple LDA Topic visualization which will group entities based on their common themes.

Email Visualization: View and analyze entities in individual emails, including named entities such as people, organizations, and locations.
Entity Clustering: Cluster entities into topics and visualize their occurrences.
Network Visualization: Display connections between popular entities and email addresses.

Design of solution and rationale 

Problem statement
Create a Streamlit app to analyze a subset of the Enron email corpus by extracting entities (e.g., People, Organizations, Countries, Dates) using SpaCy's Named Entity Recognition (NER). The app should visualize which email addresses co-occur with these entities. Additionally, prototype a method to cluster these entities into meaningful topics or groups, such as grouping entities related to "Latin American entities" or "Enron Executives."

User Needs and Goals:
1. Easy Extraction and Visualization: Users need a straightforward method to extract named entities from emails and visualize their relationships.
2. Interactive Analysis: Users want an interactive interface to explore entities and their co-occurrences.
3. Insightful Visualizations: Clear and informative visualizations to aid in understanding the data.

Solution
We utilized Streamlit’s spaCy tool for NER. It will extract the entities from the email and provide interactive visualizations. 
spaCy is an open-source library for advanced Natural Language Processing (NLP) in Python. Its en_core_web_sm model is specifically designed for various NLP tasks, including Named Entity Recognition (NER).
Installing spaCy requires installing the dependencies that come with it.This is done by using ‘pip install streamlit spacy’ and we can download spaCy’s pre-trained model by using python -m spacy download en_core_web_sm. This model is then loaded into the Streamlit app.

The Streamlit app has 4 main parts to it:
1. app.py - This is the main interface of the app where the user can understand how to navigate it. We have a sidebar which is used to navigate the app and select different pages you would like to go to. 
2. sample.py - Since the dataset is too large, we sampled a small subset of the dataset and saved this into a new csv file. We used the model on this particular subset of the data. By using random sampling, we sampled 0.02% of the data. This returns 103 rows.
3. emailvisualiser.py - This is the part where the app will take in the selected email and extract and output the entities present in it.  We have a drop down functionality which will allow the user to select an index number. Each of these index numbers are correlated to the emails in our subset. Once the user selects a particular index number, it will display the corresponding email. There is also an option to view the header information of the email so the user can understand more about the selected email.  Below this, we have a small check box that says “Show NER visualisation”. If we click on it, the app visualizes the email entities and also returns a dataframe of the entities present in the selected email. 
4. task.py - This part uses a network graph to visualize which email addresses co-occur with which entities in the emails. It also includes entity clustering by using word clouds to show how the entities are clustered into specific groups or topics based on their similarities. The user will be allowed to select an entity tag from the dropdown functionality at the beginning of the page. Based on the chosen entity tag, the visualizations will differ. For example, if the user selects “PERSON” entity tag, the network graph will display the relationship between the most popular people mentioned in the emails and the email addresses they are related to. The bar graph will show us a visualization of the 10 most popular people mentioned in the emails.
5. suggestions.py - A suggestions page for the user where they can enter in any suggestions they have for the app into a text box. 

Bonus Task:
Create a word count using LDA. LDA will help us extract important topics from a given corpus. We can identify topics using LDA. Then, by using word cloud, we can group the words that frequently occur together under the specific topics together. 

What Works Well and Future Improvements
What works well:
1. Clean UI - The app has a clean and intuitive user interface which makes it easy for users to navigate through.
2. Pre Trained spaCy model - spaCy already has a pre-trained NER model which comes ready to use and this model allowed me to quickly and accurately extract named entities from email dataset without the need for extensive training or customization.
3. Use of network graphs for visualizations - The network graphs are a good way to visualize the relationships and interactions between entities and email addresses. We are able to see how frequently certain individuals communicate or how different entities are connected through shared email threads.
4. Use of LDA with Word Cloud - The Word Cloud is also a great way of showcasing how different entities are put into clusters based on their similarities. It is easy to code and is a great visualization tool. 
Future Improvements:
1. Larger pre trained model for better accuracy - spaCy offers more pre-trained models that include different types of entities. For the app, I used the “en_core_web_sm” model which is the smallest model it has. If I had a better system with more RAM and GPU, I would use the larger model (en_core_web_lg) which is known to recognize a broader range of entity types and handle more complex contexts due to its richer feature representations. It will also provide more accurate results. 
2. Enhanced clustering techniques - I would try to use the K-means algorithm to cluster entities into topics/groups to understand which topics co-occur with these emails. I would improve it by using techniques like the Elbow Method to determine the optimal number of clusters. By choosing the number of clusters, we will be able to group the data in a more detailed and effective manner. It will provide us with customized analysis. I would also use the Silhouette Score to then assess the quality of the model and to see how similar an entity is to its own cluster. 
I had initially tried coding a simple K-means algorithm but the graph was not as clear as I wanted it to be. There were some issues with labeling the clusters and understanding which entities were shown in the graph. This is a topic I would have to study more in depth.
3. Enhanced LDA model - Currently, the LDA model clusters the most commonly occurred words together into “Topics”. However, it does not assign descriptive names for the topics. In the future, I would try to assign names to the topics that encapsulate the themes represented by the words in each topic better. 
4. Improve the speed of the app - I would try to use Parquet files instead of csv files as they are known for efficient data storage. The data would be stored in columns which will make it more efficient for read-heavy operations. It will be able to load the data much faster. I could also make use of multithreading to process the data faster. 
5. Alternatives to spaCy - BERT and Hugging Face provide advanced models that often outperform spaCy in accuracy for  NER. These models can be fine-tuned for specific needs and offer versatile NLP capabilities, but they require more computational resources. I would test these out as they are strong alternatives and they are proven to have better accuracy than spaCy’s models.
6. Save the suggestions to a text file - Since this was a mockup of the app, I have not created a way to save the suggestions entered by the user to an actual file. In the future, I would implement this code so that we will be able to see the suggestions and enhancements given by the users.
   
Instructions on running the app
To host the app locally:
1. Download the code files from the GitHub folder and make sure it's stored in a working directory you can access. 
2. Open your terminal. 
3. Use ‘conda activate streamlit’. This is done so that we switch to a specific Conda environment and so any Python packages we download will be confined to this specific environment. 
4. Use ‘pip install streamlit pandas spacy spacy-streamlit networkx matplotlib seaborn scikit-learn scipy’ to download all the necessary packages. 
5. Use ‘python -m spacy download en_core_web_sm’ to download spaCy’s NER model.
6. Run the command ‘streamit run app.py’.
This should set up a local host in your system.

Navigating the App:
Sidebar Navigation - Use the sidebar to select the page you want to visit.
Email Visualizer Page - Choose an email by selecting an index number. Click “Show NER Visualization” to extract and display entities from the selected email.
Task Page - Select an entity tag from the dropdown menu. Visualizations will update to show the most popular entities based on your selected tag.
Suggestions Page - Enter your suggestions for the app in the box provided.

Dataset used:
I have taken a random sample of 0.02% of the Enron Email dataset. This has returned around 103 rows of emails. 

