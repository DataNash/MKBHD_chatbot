-- what year is the s9 comeout
-- select Brand, Make from metadata

-- with sentiment_number as (
-- SELECT videoId, AVG(Sentiment_Number) AS average_sentiment
-- FROM mkbhd_fulldata
-- GROUP BY videoId)

-- select  MD.OS os, avg(SN.average_sentiment) avg_sentiment
-- from sentiment_number SN
-- Join
-- metadata MD
-- on MD.videoId = SN.videoId
-- group by os
-- order by avg_sentiment desc
-- limit 1;

select YEAR(STR_TO_DATE(publishedAt, '%d/%m/%Y')) Year, Phone 
from metadata
where Phone = 'Samsung s9';

select * from metadata
