------------schema-----------
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'sec')
BEGIN
EXEC('CREATE SCHEMA sec')
END

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'opt')
BEGIN
EXEC('CREATE SCHEMA opt')
END


IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'pro')
BEGIN
EXEC('CREATE SCHEMA pro')
END

---------------


IF NOT EXISTS (SELECT 1
   FROM INFORMATION_SCHEMA.TABLES
   WHERE TABLE_SCHEMA = 'sec'
   AND TABLE_NAME = 'tokens')
   BEGIN
      CREATE TABLE sec.tokens(
id INT IDENTITY(1,1),
userID INT not NULL,
token NVARCHAR(max),
createdDateTime DATETIME default getdate()
)
   END;




IF NOT EXISTS (SELECT 1  FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'sec' AND TABLE_NAME = 'users')
   BEGIN
      CREATE TABLE sec.users(
         id INT IDENTITY(1,1),
         personelID INT not NULL,
		 userName nvarchar(200),
		 email nvarchar(200),
         [password] NVARCHAR(400),
         createdDateTime DATETIME default getdate())
   END;


   IF NOT EXISTS (SELECT 1  FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'sec' AND TABLE_NAME = 'personel')
   BEGIN
      CREATE TABLE sec.personel(
         id INT IDENTITY(1,1),
         DisplayName nvarchar(100)  NULL,
         [Name] NVARCHAR(100),
         [LastName] NVARCHAR(100),
         createdDateTime DATETIME default getdate())
   END;


      IF NOT EXISTS (SELECT 1  FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'sec' AND TABLE_NAME = 'PersonelDetail')
   BEGIN
      CREATE TABLE sec.PersonelDetail(
         id INT IDENTITY(1,1),
         PersonelID nvarchar(100)  NULL,
         [BirthDay] Datetime,
         [fatherName] NVARCHAR(50),
         createdDateTime DATETIME default getdate())
   END;




      IF NOT EXISTS (SELECT 1  FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'opt' AND TABLE_NAME = 'settings')
   BEGIN
      CREATE TABLE opt.settings(
         id INT IDENTITY(1,1),
         variable nvarchar(100)  not null,
         [value] NVARCHAR(200) null,
         [systemID] int ,
         [Desc] nvarchar(400))
   END;


   IF NOT EXISTS (SELECT 1  FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'opt' AND TABLE_NAME = 'settingsMember')
   BEGIN
      CREATE TABLE opt.settingsMember(
         id INT IDENTITY(1,1),
         settingID int  not null,
         [value] NVARCHAR(200) null,
         personelID int 
         )
   END;








IF NOT EXISTS (SELECT 1
   FROM INFORMATION_SCHEMA.TABLES
   WHERE TABLE_SCHEMA = 'pro'
   AND TABLE_NAME = 'tblProducts')
   BEGIN
CREATE TABLE [pro].[tblProducts](
	[pid] [int] IDENTITY(1,1) NOT NULL,
	[pname] [nvarchar](300) NOT NULL,
	[pOwnerMobile] [nvarchar](15) NULL,
	[pMobile] [nvarchar](15) NULL,
	[ptype] [int] NOT NULL,
	[pimage] [nvarchar](400) NULL,
	[mimiSerial] [nvarchar](max) NULL,
	[pcreateDate] [datetime] default GetDate(),
	[pUpdateDate] [datetime] NULL,
	[installerCode] [nvarchar](20) NULL,
 CONSTRAINT [PK_tblProducts] PRIMARY KEY CLUSTERED 
(
	[pid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

END;