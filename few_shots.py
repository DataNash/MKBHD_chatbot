examples = [
    {
        "Question": "What topic does MKBHD talk about the most?",
        "SQLQuery": "SELECT pillar, count(*) total_sentences FROM mkbhdscripts.mkbhd_fulldata WHERE pillar != 'Unknown' GROUP BY pillar ORDER BY total_sentences DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Camera" 
    }, 
    {
        "Question": "What is MKBHD's favorite phone?",
        "SQLQuery": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment FROM mkbhdscripts.mkbhd_fulldata GROUP BY videoId) SELECT MD.videoId, MD.Phone, SN.average_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId ORDER BY average_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Samsung S3"
    },
    {
        "Question": "Which brand is MKBHD's favorite?",
        "SQLQuery": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment FROM mkbhdscripts.mkbhd_fulldata GROUP BY videoId) SELECT MD.videoId, MD.Brand, SN.average_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId WHERE MD.Brand = 'Samsung' ORDER BY average_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Samsung" 
    },
    {
        "Question": "Does he prefer Android or iOS?",
        "SQLQuery": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment FROM mkbhdscripts.mkbhd_fulldata GROUP BY videoId) SELECT MD.OS, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.OS ORDER BY avg_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Android" 
    },
    {
        "Question": "What year was the Samsung S9 released?",
        "SQLQuery": "SELECT YEAR(STR_TO_DATE(MD.publishedAt, '%d/%m/%Y')) as year, MD.Phone FROM mkbhdscripts.metadata MD WHERE MD.Phone = 'Samsung S9'",
        "SQLResult": "Result of the SQL query",
        "Answer": "2018" 
    },
    {
        "Question": "Which device has the worst screen according to MKBHD?",
        "SQLQuery": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Screen or Display' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Asus ZenFone 6"
    },
    {
        "Question": "What are the top 5 cameras reviewed by MKBHD?",
        "SQLQuery": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Camera' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment DESC LIMIT 5",
        "SQLResult": "Result of the SQL query",
        "Answer": "'iPhone 8', 'OnePlus OnePlus 2','Samsung S3', 'iPhone 6','Asus ROG Phone'"
    },
    {
        "Question": "Which device reviewed by MKBHD has the best build quality?",
        "SQLQuery": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Build quality' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Samsung S4" 
    },
    {
        "Question": "What is the best part about Asus phones?",
        "SQLQuery": "WITH sentiment_number AS (SELECT videoId, Sentiment_Number, pillar, sentence FROM mkbhdscripts.mkbhd_fulldata) SELECT MD.Phone, SN.Sentiment_Number, pillar, sentence FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId WHERE MD.Brand = 'Asus' AND pillar != 'Unknown' ORDER BY Sentiment_Number DESC LIMIT 10",
        "SQLResult": "Result of the SQL query",
        "Answer": ""
    },
    {
        "Question": "Which phone has the best camera according to MKBHD?",
        "SQLQuery": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Camera' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment, pillar FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone, pillar ORDER BY avg_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "iPhone 8" 
    },
    {
        "Question": "Which phone has the best battery life according to MKBHD?",
        "SQLQuery": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar LIKE '%attery%' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment, pillar FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone, pillar ORDER BY avg_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Samsung S3"
    },
    {
        "Question": "How does MKBHD rate the display quality of the latest iPhone?",
        "SQLQuery": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar LIKE '%isplay%' GROUP BY videoId, pillar) SELECT MD.Phone, MAX(STR_TO_DATE(MD.publishedAt, '%d/%m/%Y')) AS DatePub, AVG(SN.average_sentiment) AS avg_sentiment, pillar FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId WHERE MD.Phone LIKE '%iPhone%' GROUP BY MD.Phone, pillar ORDER BY DatePub DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "3.20000000"
    },
    {
        "Question": "Which phone came out later, ZenFone 6 or ROG Phone 3",
        "SQLQuery": "with target_phones as (select * from mkbhdscripts.metadata where Make = 'ZenFone 6' or Make = 'ROG Phone 3') select Phone from target_phones order by STR_TO_DATE(publishedAt, '%d/%m/%Y') desc limit 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Asus ROG Phone 3"
    },    
    {
        "Question": "Which phone came out later, Samsung s8 or iPhone 8",
        "SQLQuery": "with target_phones as (select * from mkbhdscripts.metadata where Phone = 'Samsung s8' or Phone = 'iPhone 8') select Phone from target_phones order by STR_TO_DATE(publishedAt, '%d/%m/%Y') desc limit 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "iPhone 8"
    },    
    {
        "Question": "When did the Pixel 6 Pro come out?",
        "SQLQuery": "SELECT STR_TO_DATE(MD.publishedAt, '%d/%m/%Y') as year, MD.Phone FROM mkbhdscripts.metadata MD WHERE MD.Phone = 'Pixel 6 Pro'",
        "SQLResult": "Result of the SQL query",
        "Answer": "2021-10-27" 
    },
    {
        "Question": "What phone has the best camera?",
        "SQLQuery": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Camera' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "iPhone 8" 
    },    
]

examples_two = [
    {
        "input": "What topic does MKBHD talk about the most?",
        "query": "SELECT pillar, count(*) total_sentences FROM mkbhdscripts.mkbhd_fulldata WHERE pillar != 'Unknown' GROUP BY pillar ORDER BY total_sentences DESC LIMIT 1"
    }, 
    {
        "input": "What is MKBHD's favorite phone?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment FROM mkbhdscripts.mkbhd_fulldata GROUP BY videoId) SELECT MD.videoId, MD.Phone, SN.average_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId ORDER BY average_sentiment DESC LIMIT 1"
    },
    {
        "input": "Which brand is MKBHD's favorite?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment FROM mkbhdscripts.mkbhd_fulldata GROUP BY videoId) SELECT MD.videoId, MD.Brand, SN.average_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId WHERE MD.Brand = 'Samsung' ORDER BY average_sentiment DESC LIMIT 1"
    },
    {
        "input": "Does he prefer Android or iOS?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment FROM mkbhdscripts.mkbhd_fulldata GROUP BY videoId) SELECT MD.OS, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.OS ORDER BY avg_sentiment DESC LIMIT 1"
    },
    {
        "input": "What year was the Samsung S9 released?",
        "query": "SELECT YEAR(STR_TO_DATE(MD.publishedAt, '%d/%m/%Y')) as year, MD.Phone FROM mkbhdscripts.metadata MD WHERE MD.Phone = 'Samsung S9'"
    },
    {
        "input": "Which device has the worst screen according to MKBHD?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Screen or Display' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment"
    },
    {
        "input": "What are the top 5 cameras reviewed by MKBHD?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Camera' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment DESC LIMIT 5"
    },
    {
        "input": "Which device reviewed by MKBHD has the best build quality?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Build quality' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment DESC LIMIT 1"
    },
    {
        "input": "What is the best part about Asus phones?",
        "query": "WITH sentiment_number AS (SELECT videoId, Sentiment_Number, pillar, sentence FROM mkbhdscripts.mkbhd_fulldata) SELECT MD.Phone, SN.Sentiment_Number, pillar, sentence FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId WHERE MD.Brand = 'Asus' AND pillar != 'Unknown' ORDER BY Sentiment_Number DESC LIMIT 10"
    },
    {
        "input": "Which phone has the best camera according to MKBHD?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Camera' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment, pillar FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone, pillar ORDER BY avg_sentiment DESC LIMIT 1"
    },
    {
        "input": "Which phone has the best battery life according to MKBHD?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar LIKE '%attery%' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment, pillar FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone, pillar ORDER BY avg_sentiment DESC LIMIT 1"
    },
    {
        "input": "How does MKBHD rate the display quality of the latest iPhone?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar LIKE '%isplay%' GROUP BY videoId, pillar) SELECT MD.Phone, MAX(STR_TO_DATE(MD.publishedAt, '%d/%m/%Y')) AS DatePub, AVG(SN.average_sentiment) AS avg_sentiment, pillar FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId WHERE MD.Phone LIKE '%iPhone%' GROUP BY MD.Phone, pillar ORDER BY DatePub DESC LIMIT 1"
    },
    {
        "input": "Which phone came out later, ZenFone 6 or ROG Phone 3",
        "query": "WITH target_phones AS (SELECT * FROM mkbhdscripts.metadata WHERE Make = 'ZenFone 6' OR Make = 'ROG Phone 3') SELECT Phone FROM target_phones ORDER BY STR_TO_DATE(publishedAt, '%d/%m/%Y') DESC LIMIT 1"
    },
    {
        "input": "Which phone came out later, Samsung s8 or iPhone 8",
        "query": "WITH target_phones AS (SELECT * FROM mkbhdscripts.metadata WHERE Phone = 'Samsung s8' OR Phone = 'iPhone 8') SELECT Phone FROM target_phones ORDER BY STR_TO_DATE(publishedAt, '%d/%m/%Y') DESC LIMIT 1"
    },
    {
        "input": "When did the Pixel 6 Pro come out?",
        "query": "SELECT STR_TO_DATE(MD.publishedAt, '%d/%m/%Y') AS year, MD.Phone FROM mkbhdscripts.metadata MD WHERE MD.Phone = 'Pixel 6 Pro'"
    },
    {
        "input": "What phone has the best camera?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Camera' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment DESC LIMIT 1"
    }
],
examples_three = [
    {
        "input": "What topic does MKBHD talk about the most?",
        "query": "SELECT pillar, count(*) total_sentences FROM mkbhdscripts.mkbhd_fulldata WHERE pillar != 'Unknown' GROUP BY pillar ORDER BY total_sentences DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Camera"
    },
    {
        "input": "What is MKBHD's favorite phone?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment FROM mkbhdscripts.mkbhd_fulldata GROUP BY videoId) SELECT MD.videoId, MD.Phone, SN.average_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId ORDER BY average_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Samsung S3"
    },
    {
        "input": "Which brand is MKBHD's favorite?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment FROM mkbhdscripts.mkbhd_fulldata GROUP BY videoId) SELECT MD.videoId, MD.Brand, SN.average_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId WHERE MD.Brand = 'Samsung' ORDER BY average_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Samsung"
    },
    {
        "input": "Does he prefer Android or iOS?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment FROM mkbhdscripts.mkbhd_fulldata GROUP BY videoId) SELECT MD.OS, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.OS ORDER BY avg_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Android"
    },
    {
        "input": "What year was the Samsung S9 released?",
        "query": "SELECT YEAR(STR_TO_DATE(MD.publishedAt, '%d/%m/%Y')) as year, MD.Phone FROM mkbhdscripts.metadata MD WHERE MD.Phone = 'Samsung S9'",
        "SQLResult": "Result of the SQL query",
        "Answer": "2018"
    },
    {
        "input": "Which device has the worst screen according to MKBHD?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Screen or Display' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment",
        "SQLResult": "Result of the SQL query",
        "Answer": "Asus ZenFone 6"
    },
    {
        "input": "What are the top 5 cameras reviewed by MKBHD?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Camera' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment DESC LIMIT 5",
        "SQLResult": "Result of the SQL query",
        "Answer": "'iPhone 8', 'OnePlus OnePlus 2', 'Samsung S3', 'iPhone 6', 'Asus ROG Phone'"
    },
    {
        "input": "Which device reviewed by MKBHD has the best build quality?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Build quality' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Samsung S4"
    },
    {
        "input": "What is the best part about Asus phones?",
        "query": "WITH sentiment_number AS (SELECT videoId, Sentiment_Number, pillar, sentence FROM mkbhdscripts.mkbhd_fulldata) SELECT MD.Phone, SN.Sentiment_Number, pillar, sentence FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId WHERE MD.Brand = 'Asus' AND pillar != 'Unknown' ORDER BY Sentiment_Number DESC LIMIT 10",
        "SQLResult": "Result of the SQL query",
        "Answer": ""
    },
    {
        "input": "Which phone has the best camera according to MKBHD?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Camera' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment, pillar FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone, pillar ORDER BY avg_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "iPhone 8"
    },
    {
        "input": "Which phone has the best battery life according to MKBHD?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar LIKE '%attery%' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment, pillar FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone, pillar ORDER BY avg_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Samsung S3"
    },
    {
        "input": "How does MKBHD rate the display quality of the latest iPhone?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar LIKE '%isplay%' GROUP BY videoId, pillar) SELECT MD.Phone, MAX(STR_TO_DATE(MD.publishedAt, '%d/%m/%Y')) AS DatePub, AVG(SN.average_sentiment) AS avg_sentiment, pillar FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId WHERE MD.Phone LIKE '%iPhone%' GROUP BY MD.Phone, pillar ORDER BY DatePub DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "3.20000000"
    },
    {
        "input": "Which phone came out later, ZenFone 6 or ROG Phone 3",
        "query": "WITH target_phones AS (SELECT * FROM mkbhdscripts.metadata WHERE Make = 'ZenFone 6' OR Make = 'ROG Phone 3') SELECT Phone FROM target_phones ORDER BY STR_TO_DATE(publishedAt, '%d/%m/%Y') DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "Asus ROG Phone 3"
    },
    {
        "input": "Which phone came out later, Samsung s8 or iPhone 8",
        "query": "WITH target_phones AS (SELECT * FROM mkbhdscripts.metadata WHERE Phone = 'Samsung s8' OR Phone = 'iPhone 8') SELECT Phone FROM target_phones ORDER BY STR_TO_DATE(publishedAt, '%d/%m/%Y') DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "iPhone 8"
    },
    {
        "input": "When did the Pixel 6 Pro come out?",
        "query": "SELECT STR_TO_DATE(MD.publishedAt, '%d/%m/%Y') AS year, MD.Phone FROM mkbhdscripts.metadata MD WHERE MD.Phone = 'Pixel 6 Pro'",
        "SQLResult": "Result of the SQL query",
        "Answer": "2021-10-27"
    },
    {
        "input": "What phone has the best camera?",
        "query": "WITH sentiment_number AS (SELECT videoId, AVG(Sentiment_Number) AS average_sentiment, pillar FROM mkbhdscripts.mkbhd_fulldata WHERE pillar = 'Camera' GROUP BY videoId, pillar) SELECT MD.Phone, AVG(SN.average_sentiment) AS avg_sentiment FROM sentiment_number SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId GROUP BY MD.Phone ORDER BY avg_sentiment DESC LIMIT 1",
        "SQLResult": "Result of the SQL query",
        "Answer": "iPhone 8"
    },
    {
    "input": "How good is the iPhone 8's battery life?",
    "query": "SELECT MD.Phone, AVG(SN.sentiment) AS avg_sentiment, SN.pillar FROM mkbhdscripts.mkbhd_fulldata SN JOIN mkbhdscripts.metadata MD ON MD.videoId = SN.videoId WHERE MD.Phone LIKE '%iPhone 8%' AND SN.pillar LIKE '%attery%' GROUP BY MD.Phone, SN.pillar ORDER BY avg_sentiment DESC LIMIT 1;",
    "SQLResult": "Result of the SQL query",
    "Answer": "3.23"}

]

