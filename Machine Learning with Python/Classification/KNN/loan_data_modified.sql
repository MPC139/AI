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

ALTER TABLE loan_data ALTER COLUMN term SET DATA TYPE text;
ALTER TABLE loan_data ALTER COLUMN annual_inc SET DATA TYPE int;

COPY loan_data
FROM '/Users/matiaspormi/Documents/AI/Machine Learning with Python/Classification/KNN/loan_data.csv'
WITH (FORMAT CSV, HEADER);

SELECT * FROM loan_data;

SELECT DISTINCT status FROM loan_data;
SELECT DISTINCT outcome FROM loan_data;
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
