#from langchain_community.llms import GooglePalm
from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector, MaxMarginalRelevanceExampleSelector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
_mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.prompts import FewShotPromptTemplate
import os
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
from few_shots import examples
import os
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
from langchain.chains import create_sql_query_chain


#llm = GoogleGenerativeAI(google_api_key = os.environ["GOOGLE_API_KEY"], temperature=0.1)

x='''"You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.\nUnless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.\nNever query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.\nPay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. NEVER EVER use  'IN' within the query as it is not supported, use a join instead this is very important. Also, pay attention to which column is in which table.\nPay attention to use CURDATE() function to get the current date, if the question involves "today".\n\nUse the following format:\n\nQuestion: Question here\nSQLQuery: SQL Query to run\nSQLResult: Result of the SQLQuery\nAnswer: Final answer here\n\n'"'''

def get_few_shot_db_chain():
    db_user = "root"
    db_password = "0650"
    db_host="localhost"
    db_name = "mkbhdscripts"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=10) #specifies database, host, password etc
    llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key= os.environ["GOOGLE_API_KEY"], temperature=0.1)
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    #to_vectorize = [" ".join(example.values()) for example in few_shots]
    to_vectorize = [" ".join(example.values()).replace("\n", " ") for example in examples]
    vectorstore1 = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples) #find actrual exampoles
    
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore1,
        k=3,
    )

    example_prompt = PromptTemplate(
    input_variables = ["Question", "SQLQuery", "SQLResult", "Answer",],
    template= "\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",)
    
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix= x,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],
    )

    #chain = SQLDatabaseChain.from_llm(llm,db,verbose=True, prompt=few_shot_prompt)
    from langchain.memory import ChatMessageHistory
    history = ChatMessageHistory()

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate
    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", f"{x}"),
            few_shot_prompt,
            MessagesPlaceholder(variable_name="messages"),
            ("human", "{input}"),
        ]
    )
    #print(final_prompt.format(input="How many products are there?",table_info="some table info",messages=[]))
    chain = SQLDatabaseChain.from_llm(llm,db,verbose=True, prompt=final_prompt,messages=[])
    return chain

if __name__ == "__main__":
    chain = get_few_shot_db_chain()
    print(chain.run("What phone has the best camera?"))



