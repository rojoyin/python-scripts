# python-scripts

## Dependencies:
It is recommended to use virtualenv for this project, to avoid conflicts with 
other projects.

Located in the root folder of the project, run the following command:
```bash
pip install -r requirements.txt
```


## pre-requisites
For working with this project, you will need to setup a service account for Google Cloud Platform (GCP) 
and download the credentials file, that should be located in the root of the project and named `credentials.json`,
which will be needed for the first use case.

Create a `.env` file based on the `.env.example` file, and fill in the values for the environment variables.
To connect to LinkedIn platform, you should provide your LinkedIn credentials in the `.env` file.

## Project scripts description
This repo contains python scripts for addressing three main challenges:

1.  Natural Language Processing (NLP) of text data. 
    
    Directory: `nl-queries`. By default, the script will use the `credentials.json` file located in the root of the project 
    and will download a bunch of files with txt extension from a Google Drive shared folder which is public.

    Currently, the script is able to handle txt files only, but it can be extended to handle other file types.

    To run this:
    ```bash
    cd nl-queries
    python main.py
    ```
    For now, I have hardcoded a couple of questions as sample.


2.  Getting LinkedIn data for companies. 
    
    Directory: `companies-linkedin`.
    
    Input: a csv file with a list of company names, which should be at `companies-linkedin/data/company_names.csv`. There is a `company_names.sample.csv` file which contains test data that you can use.
       
    Output: a csv file with the LinkedIn data for each company, which will be at `companies-linkedin/data/linkedin_urls.csv`.

    To run this:
    ```bash
    cd companies-linkedin
    python main.py
    ```
    
3. Getting g2crowd data for companies. 

    Directory: `g2crowdurls`.
 
    Input: a csv file with g2crowd urls, which should be at `g2crowdurls/data/g2crowdurls.csv`. There is a `g2crowdurls.sample.csv` file which contains test data that you can use.

    Output: print statements with structured data for each company.

    To run this:
    ```bash
    cd g2crowdurls
    python main.py
    ```
