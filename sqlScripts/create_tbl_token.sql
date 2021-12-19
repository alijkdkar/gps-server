------------schema-----------
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'sec')
BEGIN
EXEC('CREATE SCHEMA sec')
END



IF NOT EXISTS (SELECT 1
   FROM INFORMATION_SCHEMA.TABLES
   WHERE TABLE_SCHEMA = 'sec'
   AND TABLE_NAME = 'tokens')
   BEGIN
      CREATE TABLE sec.tokens(
id INT IDENTITY(1,1),
userID INT not NULL,
token NVARCHAR(100),
createdDateTime DATETIME
)
   END;




