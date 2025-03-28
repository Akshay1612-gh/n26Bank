CREATE TABLE nbank (
    customer_name VARCHAR2(128),
    customer_review CLOB NOT NULL,
    n26_response CLOB,
    date_of_experience DATE,
    date_of_review DATE,
    rating_out_of_5 VARCHAR2(26),
    difference_in_days NUMBER(38),
    year NUMBER(38),
    sentiment VARCHAR2(26),
    month NUMBER(38)
);


select * from nbank;


-- rating for each month in the year 2024--

SELECT TO_CHAR(date_of_review, 'Month') AS review_month, rating_out_of_5, 
COUNT(*) AS rating_count
FROM nbank
WHERE EXTRACT(YEAR FROM date_of_review) = 2024
GROUP BY TO_CHAR(date_of_review, 'Month'), rating_out_of_5
ORDER BY TO_DATE(TO_CHAR(date_of_review, 'Month'), 'Month'), rating_count DESC;

--analyze sentiment changes over months in 2024--

SELECT TO_CHAR(date_of_review, 'Month') AS review_month, 
sentiment, 
COUNT(*) AS sentiment_count
FROM nbank
WHERE EXTRACT(YEAR FROM date_of_review) = 2024
GROUP BY TO_CHAR(date_of_review, 'Month'), sentiment
ORDER BY TO_DATE(TO_CHAR(date_of_review, 'Month'), 'Month'), sentiment_count DESC;

--Reviews Submitted Per Day (2024)--

SELECT TRUNC(date_of_review) AS review_date, 
COUNT(*) AS reviews_per_day
FROM nbank
WHERE EXTRACT(YEAR FROM date_of_review) = 2024
GROUP BY TRUNC(date_of_review)
ORDER BY review_date ;

--Longest Delays Between Experience and Review--

SELECT customer_name, 
difference_in_days, 
rating_out_of_5
FROM nbank
ORDER BY difference_in_days DESC
FETCH FIRST 10 ROWS ONLY;


SELECT TO_CHAR(date_of_review, 'Month') AS review_month, sentiment, 
COUNT(*) AS sentiment_count
FROM nbank
WHERE EXTRACT(YEAR FROM date_of_review) = 2024
GROUP BY TO_CHAR(date_of_review, 'Month'), sentiment
ORDER BY TO_DATE(TO_CHAR(date_of_review, 'Month'), 'Month'), sentiment_count DESC;


--Monthly Positive Review Growth Rate--

SELECT TO_CHAR(date_of_review, 'Month') AS review_month, 
COUNT(*) AS total_positive_reviews,
COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY MIN(date_of_review)) AS growth_rate
FROM nbank
WHERE sentiment = 'Positive' 
AND EXTRACT(YEAR FROM date_of_review) = 2024
GROUP BY TO_CHAR(date_of_review, 'Month')
ORDER BY MIN(date_of_review);

--Monthly Positive Review Growth Rate--

SELECT TO_CHAR(date_of_review, 'Month') AS review_month, 
COUNT(*) AS total_negative_reviews,
COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY MIN(date_of_review)) AS growth_rate
FROM nbank
WHERE sentiment = 'Negative' 
AND EXTRACT(YEAR FROM date_of_review) = 2024
GROUP BY TO_CHAR(date_of_review, 'Month')
ORDER BY MIN(date_of_review);
