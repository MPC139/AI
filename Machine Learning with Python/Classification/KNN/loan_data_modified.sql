CREATE TABLE loan_data (
	index_ int,
	status text,
	loan_amnt int,
	term text,
	annual_inc int,
	dti numeric(5,2),
	payment_inc_ratio numeric(8,5),
	revol_bal int,
	revol_util numeric(5,2),
	purpose text,
	home_ownership text,
	delinq_2yrs_zero bool,
	pub_rec_zero bool,
	open_acc int,
	grade numeric(5,2),
	outcome text,
	emp_length int,
	purpose_ text,
	home_ text,
	emp_len_ text,
	borrower_score numeric(4,2)
);

SELECT * FROM loan_data;

ALTER TABLE loan_data ALTER COLUMN term SET DATA TYPE text;
ALTER TABLE loan_data ALTER COLUMN annual_inc SET DATA TYPE int;

COPY loan_data
FROM '/tmp/loan_data.csv'
WITH (FORMAT CSV, HEADER);

SELECT status, term FROM loan_data;

SELECT DISTINCT status FROM loan_data;
SELECT DISTINCT outcome FROM loan_data;
SELECT DISTINCT emp_len_ FROM loan_data;
SELECT DISTINCT emp_length FROM loan_data ORDER BY emp_length DESC;
SELECT DISTINCT term FROM loan_data;

UPDATE loan_data
SET emp_len_ = '1'
WHERE emp_len_ = ' > 1 Year';

UPDATE loan_data
SET emp_len_ = '0'
WHERE emp_len_ = ' < 1 Year';

ALTER TABLE loan_data ALTER COLUMN emp_len_ SET DATA TYPE bool USING emp_len_::boolean;

UPDATE loan_data
SET term = '1'
WHERE term = '60 months';

UPDATE loan_data
SET term = 'false'
WHERE term = '36 months';

ALTER TABLE loan_data ALTER COLUMN term SET DATA TYPE bool USING term::boolean;

SELECT * FROM loan_data;
SELECT loan_amnt FROM loan_data;
SELECT loan_amnt FROM loan_data WHERE loan_amnt > 5000;
SELECT loan_amnt FROM loan_data WHERE loan_amnt > 5000 ORDER BY loan_amnt;
SELECT loan_amnt FROM loan_data WHERE loan_amnt > 5000 ORDER BY loan_amnt DESC;
SELECT loan_amnt FROM loan_data WHERE loan_amnt > 5000 ORDER BY loan_amnt DESC LIMIT 20;

SELECT borrower_score
FROM loan_data
WHERE outcome NOT IN ('default')
ORDER BY borrower_score;

SELECT loan_amnt,
		annual_inc,
		dti,
		payment_inc_ratio,
		revol_bal,
		revol_util,
		open_acc,
		grade,
		borrower_score,
		outcome
FROM loan_data;

COPY ( 
	SELECT loan_amnt,
			annual_inc,
			dti,
			payment_inc_ratio,
			revol_bal,
			revol_util,
			open_acc,
			grade,
			borrower_score,
			outcome
	FROM loan_data)
TO '/Users/matiaspormi/Documents/AI/Machine Learning with Python/Classification/KNN/copy_loan_data.csv'
WITH (FORMAT CSV,HEADER);

SELECT 	status,
	loan_amnt,
	term,
	annual_inc,
	dti,
	payment_inc_ratio ,
	revol_bal ,
	revol_util,
	home_ownership,
	grade,
	outcome,
	emp_length,
	emp_len_,
	borrower_score
FROM loan_data;


COPY (
	SELECT 	status,
		loan_amnt,
		term,
		annual_inc,
		dti,
		payment_inc_ratio ,
		revol_bal ,
		revol_util,
		home_ownership,
		grade,
		outcome,
		emp_length,
		emp_len_,
		borrower_score
	FROM loan_data)
TO '/tmp/loan_data_modified2.csv'
WITH (FORMAT CSV, HEADER);









CREATE TABLE test(
	id int,
	name_ text,
	cp int
);

INSERT INTO test 
VALUES
	(0, 'nico', 1650),
	(1, 'mati', 1651),
	(2, 'carla', 1452);

SELECT * FROM test;

ALTER TABLE test ALTER COLUMN cp SET DATA TYPE text;

UPDATE test
SET cp ='B1650'
WHERE cp = '1650';


UPDATE test
SET cp ='B1651'
WHERE name_ = 'mati';

UPDATE test
SET cp ='B1421'
WHERE name_ = 'carla';


