
# Data Science Job Skill Extractor

<p align="center">
  <img src="reports/figures/data-science-skills.jpg" alt="Data Science Skills"/>
</p>


## Background
In the rapidly evolving field of data science, staying ahead of the curve with the latest skills and technologies is crucial for professionals and organizations. This project is based on my personal struggle back in the early days where I found it difficult to determine which skills I needed to master just enough to be noticed in the job market.

To address this challenge, I want to develop a Data Science Job Skill Extractor that leverages the knowledge **Web Scraping** and **Named Entity Recognition (NER)**. This platform will provide real-time insights into the current skill demands in the Data Science job market. I hope the Data Science Skill Insights Platform will be able to:

- Provide data science newcomers with real-time information on the most in-demand skills, enhancing their education and career planning.
- Assist data science instructors in designing curricula based on industry trends, ensuring relevance and market alignment.
- Aid employers in staying competitive by understanding the skill landscape and adapting their hiring strategies.
## Project Scope
For Proof-of-Concept (POC), the project scope will be:
- Job Site : **LinkedIn**
- Job Position : **Data Scientist**
- Job Location : **United States** (because Indonesia's job posting is small)

## Installation and Setup
### Resources Used
- **Code Editor:** Visual Studio Code
- **Python Version:** 3.10.13

### Python Package Used
- **General Purpose**: General purpose packages like `time, os, sys and dotenv`.
- **Web Scrapping**: Packages used for web scrapping are `selenium and beautifulsoup4`.
- **Data Manipulation and Preparation**: Packages used for handling and importing dataset such as `pandas, spacy and numpy`.
- **Data Visualization**: Packages used to plot graphs in the analysis or for understanding the data as `wordcloud, seaborn, and matplotlib`.
- **Named Entity Recognition (NER)**: Packages that were used to train customized NER model such as `spacy`.

Install libraries and dependencies are needed by creating Python environment and install all libraries with their specific versions that are available in the requirements.txt

```bash
  conda install -n <environment_name> python==3.10.13
  conda activate <environment_name>
  pip install -r requirements.txt
```
## Data
## Data Source
The data consist of 5 columns:
 - Job Title (Plain Text)
 - Job Post (Plain Text): time since the jobs posted
 - Job Description (Plain Text): job description along with the requirements
 - Job Function (Plain Text): part of the division or team in the company
 - Job Industry (Plain Text): domain industry of the company

## Data Acquisition
The dataset that we used can are scrapped from the LinkedIn jobs search.

### Data Preprocessing
We only used the `Job Description` column and to prepare it, the following these steps:
- Eliminate any HTML tags present.
- Condense multiple consecutive spaces into a single space.
- Get rid of non-standard ASCII characters.
- Convert all letters to lowercase.
- Use the Spacy model to break down word and punctuations into separate tokens. Group the words and punctuations with spaces between them.

### Data Annotation
Annotate data before training the model, the annotation will be done using a [spacy annotator tool](https://tecoholic.github.io/ner-annotator/). Shout out to [tecoholic](https://github.com/tecoholic) the tool.
### Data Preparation
Since spacy model is used, for those data that will used for training and validation must be in a [DocBin](https://spacy.io/api/docbin) format. While for testing we just need to convert it into .txt file.

## About the Model
The model is called a named entity recognition (NER) model which is specifically used for tagging named entities (data science related skills) inside texts/ documents.

## Evaluation & Results
To assess the performance of our Named Entity Recognition (NER) model, we used a straightforward method for classification, which includes the following metrics:

- **Precision**: This tells us the percentage of correctly identified data science skills out of all the skills identified by our NER model. In simple terms, it measures how accurate our model is when it claims to have found a skill.
- **Recall**: This shows the percentage of correctly identified data science skills out of the total number of skills that were actually present in the text according to our annotated ground truth. In simpler terms, it measures how well our model captures all the relevant skills.
- **F1-Score**: This is a combination of both Precision and Recall. It gives us an overall measure of the model's performance by considering both false positives and false negatives. It's a balanced way to evaluate how well our model is performing.

## Report
The results of our Named Entity Recognition (NER) model are displayed in form of a word cloud and a count plot in horizontal manner which can be accessed through this [Tableau Dashboard](https://public.tableau.com/app/profile/marcellinus.witarsah/viz/DataScienceJobSkillsPlatform/Frontpage).

## Improvement
There are 3 things that will be improved from the project:
* [ ] Perform automatic annotation by creating a dictionary of data science skills and annotated through spacy. This will save a lot a time when dealing with larger dataset.
* [ ] Apply transfer learning in a hope to improve the model performance
* [ ] Revise the web scraping script.  
