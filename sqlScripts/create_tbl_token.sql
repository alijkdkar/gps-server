IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'gpsManager')
  BEGIN
    CREATE DATABASE [gpsManager]


END
go
use [gpsManager]
go

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
	[pOwnerPID] [int] NULL,
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








go


--produtre 
create  PROCEDURE [pro].[uspModifyProduct]
    @jsonProductInput nvarchar(max)=Null
AS 
    
BEGIN try

create table #inputs( pid INT, pname NVARCHAR(200), pOwnerPID int, pOwnerMobile NVARCHAR(15), pMobile NVARCHAR(15), ptype int, pimage nvarchar(300), mimiSerial nvarchar(200)
		, pcreateDate datetime, pUpdateDate datetime, installerCode int)

insert #inputs
SELECT *
FROM OPENJSON(@jsonProductInput ) 
  WITH (
    pid INT 'strict $.pid',
    pname NVARCHAR(200) N'$.pname',
    pOwnerPID int '$.pOwnerPID',
    pownerMobile NVARCHAR(15) '$.pownerMobile',
    pMobile NVARCHAR(15) '$.pMobile',
	ptype int '$.ptype',
	pimage nvarchar(300) '$.pimage',
	mimiSerial nvarchar(200) '$.mimiSerial',
	pcreateDate datetime '$.pcreateDate',
	pUpdateDate datetime '$.pUpdateDate',
	installerCode  int '$.installerCode'
  );


  
  
  update pro.tblProducts set pname=x.pname, pOwnerMobile =x.pOwnerMobile, pOwnerPID=x.pOwnerPID,pMobile=x. pMobile,ptype=x. ptype,pimage=x. pimage,mimiSerial =x. mimiSerial
  , pUpdateDate = GETDATE(), installerCode =x.installerCode from #inputs as x where x.pid = pro.tblProducts.pid 
  
  
  insert into pro.tblProducts(pname, pOwnerMobile, pOwnerPID, pMobile, ptype, pimage, mimiSerial, pcreateDate, pUpdateDate, installerCode)
  select pname, pOwnerMobile, pOwnerPID, pMobile, ptype, pimage, mimiSerial, pcreateDate, pUpdateDate, installerCode from #inputs as t
  where t.pid = 0 or not exists(select 1 from pro.tblProducts as tb  where t.pid=tb.pid )
 

END try
begin catch
select 1 as ID,100 as  'Message' 
end catch