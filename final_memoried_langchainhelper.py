#from langchain_community.llms import GooglePalm
from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector, MaxMarginalRelevanceExampleSelector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.prompts import FewShotPromptTemplate
import os
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
from few_shots import examples,examples_two,examples_three
import os
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.globals import set_verbose, set_debug
set_debug(True)
set_verbose(True)
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda


def get_chain(history=None,google_api_key= os.environ["GOOGLE_API_KEY"]):
    instruction = '''"You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.\nUnless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.\nNever query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.\nPay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. NEVER EVER inlude 'AI :' within the query if it happens to be present remove it before querying. NEVER EVER use  'IN' within the query as it is not supported, use a join instead this is very important. Also, pay attention to which column is in which table.\nPay attention to use CURDATE() function to get the current date, if the question involves "today".\n\nUse the following format:\n\nQuestion: Question here\nSQLQuery: SQL Query to run\nSQLResult: Result of the SQLQuery\nAnswer: Final answer here\n\n'"'''
    db_user = "root"
    db_password = "0650"
    db_host="localhost"
    db_name = "mkbhdscripts"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=10) #specifies database, host, password etc
    llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=google_api_key, temperature=0.1)
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    to_vectorize = [" ".join(example.values()).replace("\n", " ") for example in examples_three]
    vectorstore_input_query_answers = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples_three) #find actrual exampoles

    generate_query = create_sql_query_chain(llm, db)
    execute_query = QuerySQLDataBaseTool(db=db)
    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question in a friendly, grammatically correct full sentence that addresses the user question.

    input: {question}
    query: {query}
    SQL Result: {result}
    Answer: """
    )

    rephrase_answer = answer_prompt | llm | StrOutputParser()

    chain = (
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}\nSQLQuery:"),
            ("ai", "{query}"),
        ]
    )

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples_three,#examples,#examples_two,
        embeddings,
        vectorstore_input_query_answers,
        k=4,
        input_keys=["input"],
    )
    #print(example_selector.select_examples({"input": "what phone has the best camera?"}))

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        example_selector=example_selector,
        input_variables=["input","top_k"],
    )

    #print(few_shot_prompt.format(input="What phone has the best camera?"))
    instruction='''"You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.This is very very important, NEVER include "AI:" within the SQL query if it appears ignore it.\nUnless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL.Here is the relevant table info: {table_info}. You can order the results to return the most informative data in the database.\nNever query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.\nPay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. NEVER EVER use  'IN' within the query as it is not supported, use a join instead this is very important. Also, pay attention to which column is in which table.\nPay attention to use CURDATE() function to get the current date, if the question involves "today".\n\n Never include "AI :" within the query. \n\nUse the following format:\n\nQuestion: input here\query: SQL Query to run\nSQLResult: Result of the SQLQuery\nAnswer: Final answer here .\n\nBelow are a number of examples of questions and their corresponding SQL queries.  Those examples are just for reference and should be considered while answering follow up questions. if ever you don't know a question respond 'please phrease your question differently''"'''

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", instruction),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )
    #print(final_prompt.format(input="How many products are there?",table_info="some table info"))
    generate_query = create_sql_query_chain(llm, db,final_prompt)
    chain = (
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
    )

    history = ChatMessageHistory()
    memory = ConversationBufferMemory(return_messages=True)

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", instruction),
            few_shot_prompt,
            MessagesPlaceholder(variable_name="messages"),
            ("human", "{input}"),
        ]
    )
    generate_query = create_sql_query_chain(llm, db,final_prompt)

    chain = (
    RunnablePassthrough.assign(query=generate_query).assign(
        history = RunnableLambda(lambda x: memory.load_memory_variables(x)["history"]),
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
    )
    return chain








