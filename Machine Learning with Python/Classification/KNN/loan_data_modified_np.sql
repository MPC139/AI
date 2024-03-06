-- Primero creamos una tabla donde volcaremos los datos de nuestra base de datos.
-- Creamos la tabla y definimos las columnas con su tipo de datos.
-- Como el archivo no tenia indice, le agregamos la columna index
CREATE TABLE loan_data_np (
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

SELECT * FROM loan_data_np;

ALTER TABLE loan_data ALTER COLUMN term SET DATA TYPE text;
ALTER TABLE loan_data ALTER COLUMN annual_inc SET DATA TYPE int;

-- copia los datos de la tabla loan_data a la tabla creada loan_data_np.
-- la pasamos a la carpeta tmp por un tema de permisos.
COPY loan_data_np
FROM '/tmp/loan_data.csv'
WITH (FORMAT CSV, HEADER);

-- Ahora pasamos los datos en forma de texto a numericos.
-- Los booleanos los ponemos en 1 y en 0 segun corresponda, para evitar inconvenientes cuando se pase a python.
-- la columna purpose, al ser muy variada, la dejamos en texto
-- vemos que hay columnas repetidas, a modo didactico para trabajarlas con python las dejamos.
SELECT DISTINCT status FROM loan_data_np;
SELECT DISTINCT term FROM loan_data_np;
SELECT DISTINCT purpose, purpose_ FROM loan_data_np;
SELECT DISTINCT home_ownership, home_ FROM loan_data_np;
SELECT DISTINCT outcome FROM loan_data_np;
SELECT DISTINCT emp_len_ FROM loan_data_np;
SELECT DISTINCT delinq_2yrs_zero FROM loan_data_np;
SELECT DISTINCT pub_rec_zero FROM loan_data_np;

UPDATE loan_data_np
SET status = '0'
WHERE status = 'Default';

UPDATE loan_data_np
SET status = '1'
WHERE status = 'Fully Paid';

UPDATE loan_data_np
SET status = '2'
WHERE status = 'Charged Off';

UPDATE loan_data_np
SET term = '0'
WHERE term = '36 months';

UPDATE loan_data_np
SET term = '1'
WHERE term = '60 months';

UPDATE loan_data_np
SET home_ownership = '0'
WHERE home_ownership = 'MORTGAGE'

UPDATE loan_data_np
SET home_ownership = '1'
WHERE home_ownership = 'RENT'

UPDATE loan_data_np
SET home_ownership = '2'
WHERE home_ownership = 'OTHER'

UPDATE loan_data_np
SET home_ownership = '3'
WHERE home_ownership = 'OWN'

UPDATE loan_data_np
SET outcome = '0'
WHERE outcome = 'default'

UPDATE loan_data_np
SET outcome = '1'
WHERE outcome = 'paid off'

UPDATE loan_data_np
SET emp_len_ = '0'
WHERE emp_len_ = ' < 1 Year'

UPDATE loan_data_np
SET emp_len_ = '1'
WHERE emp_len_ = ' > 1 Year'

UPDATE loan_data_np
SET delinq_2yrs_zero = '0'
WHERE delinq_2yrs_zero = 'false'

UPDATE loan_data_np
SET delinq_2yrs_zero = '1'
WHERE delinq_2yrs_zero = 'true'

UPDATE loan_data_np
SET pub_rec_zero = '0'
WHERE pub_rec_zero = 'false'

UPDATE loan_data_np
SET pub_rec_zero = '1'
WHERE pub_rec_zero = 'true'

ALTER TABLE loan_data_np ALTER COLUMN status TYPE integer USING status::integer;
ALTER TABLE loan_data_np ALTER COLUMN term TYPE integer USING term::integer;
ALTER TABLE loan_data_np ALTER COLUMN home_ownership TYPE integer USING home_ownership::integer;
ALTER TABLE loan_data_np ALTER COLUMN outcome TYPE integer USING outcome::integer;
ALTER TABLE loan_data_np ALTER COLUMN emp_len_ TYPE integer USING emp_len_::integer;
ALTER TABLE loan_data_np ALTER COLUMN delinq_2yrs_zero TYPE integer USING delinq_2yrs_zero::integer;
ALTER TABLE loan_data_np ALTER COLUMN pub_rec_zero TYPE integer USING pub_rec_zero::integer;

-- Ahora que ya tenemos "procesada" nuestra base de datos, procedemos a guardar una copia.

COPY (
	SELECT index_,
		status,
		loan_amnt,
		term,
		annual_inc,
		dti,
		payment_inc_ratio,
		revol_bal,
		revol_util,
		purpose,
		home_ownership,
		delinq_2yrs_zero,
		pub_rec_zero,
		open_acc,
		grade,
		outcome,
		emp_length,
		purpose_,
		home_,
		emp_len_,
		borrower_score
	FROM loan_data_np)
TO '/tmp/loan_data_modified_np.csv'
WITH (FORMAT CSV, HEADER);