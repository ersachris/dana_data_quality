WITH parsed_date AS(
  SELECT  
    PARSE_DATE("%Y%m%d", CAST(date AS STRING)) as date
  FROM `dana-quality-test.dana_quality_test.USW00093084_temperature_degreeF`
)
SELECT 
  date,
  EXTRACT(DAY FROM date) AS day,
  EXTRACT(MONTH FROM date) AS month,
  EXTRACT(YEAR FROM date) AS year,
  EXTRACT(WEEK FROM date) AS week,
  EXTRACT(DAYOFWEEK FROM date) AS day_of_week,
  EXTRACT(DAYOFYEAR FROM date) AS day_of_year,
  EXTRACT(QUARTER FROM date) AS quarter,
FROM parsed_date