1. Admin Table
Fields	Datatype	Constraints	Description
id	varchar(50)	Primary Key	Unique Admin ID
username	varchar(50)	Not Null	Admin login username
password	varchar(255)	Not Null	Hashed password
role	varchar(20)	Not Null	User role (admin)
email	varchar(100)	Not Null	Admin email
created_at	timestamp	Not Null	Account creation time

2. School (Institute) Table
Fields	Datatype	Constraints	Description
id	varchar(50)	Primary Key	Unique school identifier
name	varchar(255)	Not Null	School name
username	varchar(50)	Not Null	School login username
password	varchar(255)	Not Null	Hashed password
role	varchar(20)	Not Null	User role (school)
email	varchar(100)	Not Null	School email
location	varchar(255)	Not Null	School location
created_at	timestamp	Not Null	School registration date

3. Student Table
Fields	Datatype	Constraints	Description
id	varchar(50)	Primary Key	Unique student ID
student_id	varchar(50)	Unique, Not Null	Official student identifier
name	varchar(100)	Not Null	Student full name
school_id	varchar(50)	Foreign Key	References school table
email	varchar(100)	Not Null	Student email
password	varchar(255)	Not Null	Hashed password
role	varchar(20)	Not Null	User role (student)
created_at	timestamp	Not Null	Registration date

4. Certificate Table
Fields	Datatype	Constraints	Description
id	varchar(50)	Primary Key	Certificate ID
name	varchar(255)	Not Null	Certificate file name
hash	varchar(64)	Unique, Not Null	SHA256 hash of certificate
student_id	varchar(50)	Foreign Key	References student table
school_id	varchar(50)	Foreign Key	References school table
issuer_id	varchar(50)	Not Null	Issuing school ID
chain_hash	varchar(64)	Not Null	Blockchain hash
created_at	timestamp	Not Null	Certificate creation time
metadata	json	Optional	Certificate metadata

5. Certificate Chain Table
Fields	Datatype	Constraints	Description
id	varchar(50)	Primary Key	Chain record ID
certificate_id	varchar(50)	Foreign Key	References certificate table
hash	varchar(64)	Not Null	Certificate SHA256 hash
chain_hash	varchar(64)	Not Null	Blockchain hash
timestamp	timestamp	Not Null	Time added to blockchain
status	varchar(20)	Not Null	Chain status
verification_count	int	Default 0	Total verification attempts

6. Verification Table
Fields	Datatype	Constraints	Description
id	varchar(50)	Primary Key	Verification ID
certificate_hash	varchar(64)	Foreign Key	References certificate hash
verifier_id	varchar(50)	Foreign Key	References verifier table
result	boolean	Not Null	Verification result
ai_valid	boolean	Not Null	AI validation result
confidence	float	Not Null	AI confidence score
validation_token	varchar(50)	Not Null	AI validation token
explanation	text	Optional	Verification explanation
timestamp	timestamp	Not Null	Verification time

7. Verifier Table
Fields	Datatype	Constraints	Description
id	varchar(50)	Primary Key	Verifier ID
username	varchar(50)	Not Null	Verifier login username
password	varchar(255)	Not Null	Hashed password
role	varchar(20)	Not Null	User role (verifier)
email	varchar(100)	Not Null	Verifier email
company	varchar(255)	Optional	Company name
created_at	timestamp	Not Null	Registration time

8. Feedback Table
Fields	Datatype	Constraints	Description
id	varchar(50)	Primary Key	Feedback ID
verifier_id	varchar(50)	Foreign Key	References verifier table
message	text	Not Null	Feedback message
category	varchar(50)	Not Null	Feedback category
priority	varchar(20)	Optional	Feedback priority
timestamp	timestamp	Not Null	Feedback submission time

9. Blockchain Registry Table
Fields	Datatype	Constraints	Description
hash	varchar(64)	Primary Key	Certificate SHA256 hash
student_id	varchar(50)	Foreign Key	Student ID
school_id	varchar(50)	Foreign Key	School ID
issuer_id	varchar(50)	Not Null	Issuer ID
chain_hash	varchar(64)	Not Null	Blockchain record hash
timestamp	timestamp	Not Null	Record timestamp
valid	boolean	Default true	Certificate validity
verification_count	int	Default 0	Total verification attempts



Relationships Summary
Relationship	Type
Admin → Schools	One to Many
School → Students	One to Many
School → Certificates	One to Many
Student → Certificates	One to Many
Certificate → CertificateChain	One to One
Certificate → Verifications	One to Many
Verifier → Verifications	One to Many
Verifier → Feedback	One to Many