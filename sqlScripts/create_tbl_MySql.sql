CREATE DATABASE if not EXISTS gpsmanager;

-- ------------begin schema-----------

 CREATE SCHEMA if not exists opt;
CREATE SCHEMA if not exists pro;
CREATE SCHEMA if not exists pub;

-- --------End SCHEMA-------


CREATE TABLE if not exists sec.tokens(
 id  INT  NOT NULL AUTO_INCREMENT key,
 userID INT not NULL,
 token Text,
 createdDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
 )





      CREATE TABLE if not exists sec.users(
         id INT  NOT NULL AUTO_INCREMENT key,
         personelID INT not NULL,
		 userName nvarchar(200),
		 email nvarchar(200),
         password  NVARCHAR(400),
         createdDateTime timestamp default current_timestamp);



      CREATE TABLE if not Exists sec.personel(
         id INT  NOT NULL AUTO_INCREMENT key,
         DisplayName nvarchar(100)  NULL,
         Name NVARCHAR(100),
         LastName NVARCHAR(100),
         createdDateTime timestamp default current_timestamp)


      CREATE TABLE if not exists sec.PersonelDetail(
         id INT  NOT NULL AUTO_INCREMENT key,
         PersonelID nvarchar(100)  NULL,
         BirthDay timestamp,
         fatherName NVARCHAR(50),
         createdDateTime timestamp default current_timestamp);
   




      CREATE TABLE if not exists opt.settings(
         id INT  NOT NULL AUTO_INCREMENT key,
         variable nvarchar(100)  not null,
         value NVARCHAR(200) null,
         systemID int ,
         Description nvarchar(400))


      CREATE TABLE if not exists opt.settingsMember(
         id INT  NOT NULL AUTO_INCREMENT key,
         settingID int  not null,
         value NVARCHAR(200) null,
         personelID int 
         )
   





CREATE TABLE pro.tblProducts(
	pid  INT  NOT NULL AUTO_INCREMENT key,
	pname  nvarchar (300) NOT NULL,
	pOwnerMobile  nvarchar (15) NULL,
	pOwnerPID  int  NULL,
	pMobile  nvarchar (15) NULL,
	ptype  int  NOT NULL,
	pimage  nvarchar (400) NULL,
	mimiSerial  nvarchar (6000) NULL,
	pcreateDate  timestamp default current_timestamp,
	pUpdateDate  timestamp default NULL,
	installerCode  nvarchar (20) NULL,
    expireDate   timestamp default current_timestamp,
    isActive   BIT  default 1);



      CREATE TABLE pro.lochis(
         lhid INT  NOT NULL AUTO_INCREMENT key,
         ProductID int not null,
		 AddressName nvarchar(300),
          DateTime   timestamp default current_timestamp,
		 IsDeleted bit default 0,
		 Longitude DECIMAL(12,9),
		 latitude DECIMAL(12,9)
         );


CREATE INDEX lochisIndex ON pro.lochis (DateTime);

go
insert into pro.lochis (ProductID,Longitude, latitude)
values(1,51.652395,32.625721),(1,51.652326,32.625347),(1,51.651891,32.625363),(1,51.651416,32.625340)
,(1,51.642125,32.625149),(1,51.642159,32.625629)

select * from pro.lochis
go

   CREATE TABLE if not  exists pro.services(
         servid INT  NOT NULL AUTO_INCREMENT key,
         serviceName nvarchar(100),
         DateTime timestamp default current_timestamp,
		 updateTime timestamp default current_timestamp,
		 IsDeleted bit default 0,
		 isSystem bit default 1);

go

CREATE TABLE if not exists pro.servicesDetail(
         sdId INT  NOT NULL AUTO_INCREMENT key,
          serviceId  int not null,
		  ProductId  int not null,
          DateTime timestamp default current_timestamp,
		  updateTime  timestamp default current_timestamp,
		 IsDeleted bit default 0,
		 maxValuee int default 0,
		  value  int default 0,
		 periodCounter int default 0
         );


   CREATE TABLE if not exists pro. ownerServices (
         oservid INT  NOT NULL AUTO_INCREMENT key,
          serviceName  nvarchar(100),
          DateTime  timestamp default current_timestamp,
		  updateTime  timestamp default current_timestamp,
		 IsDeleted bit default 0,
		  ownerID  int not null
         );


      CREATE TABLE pro. ownerServicesDetail (
         osdId INT  NOT NULL AUTO_INCREMENT key,
          serviceId  int not null,
		  ProductId  int not null,
          DateTime  timestamp default current_timestamp,
		  updateTime  timestamp default current_timestamp,
		 IsDeleted bit default 0,
		 maxValuee int default 0,
		  value  int default 0,
		 periodCounter int default 0
         );
         


-- CREATE TEMPORARY TABLE IF NOT EXISTS table2 AS (SELECT * FROM table1)



-- go


-- --produtre 
drop PROCEDURE if exists pro.uspModifyProduct;
DELIMITER &&  
create PROCEDURE pro.uspModifyProduct(jsonProductInput nvarchar(1000) )
begin
	drop table if exists tempJson;
 
	CREATE TABLE tempJson (
	ID INT NOT NULL AUTO_INCREMENT,
	POPULATION_JSON_DATA NVARCHAR(1000) NOT NULL,
	PRIMARY KEY (ID)
	);
 
	INSERT INTO tempJson (POPULATION_JSON_DATA) VALUES  ( jsonProductInput );
	select * from tempJson;
 /* SELECT JSON_EXTRACT(jsonProductInput , '$.pid','$.pname','$.pOwnerPID');*/
  /*create TEMPORARY TABLE IF NOT EXISTS pro.inputs(pid int ,pname nvarchar(300));*/





  
  update  pro.tblproducts set 
  	pname=JSON_EXTRACT(x.POPULATION_JSON_DATA , '$.pname'),
	pOwnerMobile =JSON_EXTRACT(x.POPULATION_JSON_DATA , '$.pownerMobile'), 
	pOwnerPID=JSON_EXTRACT(x.POPULATION_JSON_DATA , '$.pOwnerPID'),
	pMobile=JSON_EXTRACT(x.POPULATION_JSON_DATA , '$.pMobile'),
	ptype=JSON_EXTRACT(x.POPULATION_JSON_DATA , '$.ptype'),
	pimage=JSON_EXTRACT(x.POPULATION_JSON_DATA , '$.pimage'),
	mimiSerial =JSON_EXTRACT(x.POPULATION_JSON_DATA , '$.mimiSerial'),
	pUpdateDate = GETDATE(), 
	installerCode =JSON_EXTRACT(x.POPULATION_JSON_DATA , '$.installerCode') 
	from tempJson as x 
	where x.pid = pro.tblProducts.pid 



insert into pro.tblproducts ( pname, pOwnerPID, pOwnerMobile, pMobile, ptype, pimage, mimiSerial, pcreateDate, pUpdateDate, installerCode, expireDate, isActive)
	SELECT 
			JSON_EXTRACT(POPULATION_JSON_DATA , '$.pname') as pname,
            JSON_EXTRACT(POPULATION_JSON_DATA , '$.pOwnerPID') as pOwnerPID,
            JSON_EXTRACT(POPULATION_JSON_DATA , '$.pownerMobile') as pownerMobile,
            JSON_EXTRACT(POPULATION_JSON_DATA , '$.pMobile') as pMobile,
            JSON_EXTRACT(POPULATION_JSON_DATA , '$.ptype') as ptype,
            JSON_EXTRACT(POPULATION_JSON_DATA , '$.pimage') as pimage,
            JSON_EXTRACT(POPULATION_JSON_DATA , '$.mimiSerial') as mimiSerial,
            JSON_EXTRACT(POPULATION_JSON_DATA , '$.pcreateDate') as pcreateDate,
            JSON_EXTRACT(POPULATION_JSON_DATA , '$.pUpdateDate') as pUpdateDate,
            JSON_EXTRACT(POPULATION_JSON_DATA , '$.installerCode') as installerCode,
            JSON_EXTRACT(POPULATION_JSON_DATA , '$.expireDate') as expireDate,
            JSON_EXTRACT(POPULATION_JSON_DATA , '$.isActive') as isActive
	from tempJson as t where t.pid = 0 or not exists(select 1 from pro.tblProducts as tb  where t.pid=tb.pid );



END &&  
DELIMITER ;  

-- exec [pro].[uspModifyProduct] N'{
-- "pid": 2,
-- "pname": "تست 2",
-- "pOwnerPID": 1,
-- "pownerMobile": "9132120833",
-- "pMobile": "9132120832",
-- "ptype": 1,
-- "pimage": "",
-- "mimiSerial": "asd12345asda456a5s4das6d54ad456as4d5a4sd65asd",
-- "pcreateDate": "2022-02-12T21:52:20.583",
-- "pUpdateDate": null,
-- "installerCode": "0"
-- }'

-- GO

-- create  proc pro.uspGetLocations
-- @productID int=0,
-- @ownerUserID int = 0,
-- @sDate datetime =null,
-- @eDate Datetime =null
-- as 
-- SET NOCOUNT ON
-- declare @sqlStr nvarchar(max)='',@wereStr nvarchar(200)=''

-- --select Create
-- select @sqlStr +='select lh.lhid,lh.ProductID,lh.AddressName,lh.DateTime,lh.Longitude,lh.latitude 
-- from pro.tblProducts as p 
-- left join  pro.lochis as lh on p.pid=lh.ProductID 
-- where 1=1 and lh.IsDeleted<>1 and p.isActive = 1'



-- if (@ownerUserID<>0)
-- select @wereStr += ' and p.pOwnerPID = '+cast(@ownerUserID as nvarchar)

-- if (@productID<>0)
-- select @wereStr += ' and p.pid = '+cast(@productID as nvarchar)

-- if @sDate is not null 
-- select @wereStr += ' and lh.DateTime > ' +''''+convert (nvarchar, @sdate )+''''

-- if @eDate is not null 
-- select @wereStr += ' and lh.DateTime <' +''''+convert (nvarchar, @eDate )+''''

-- select @sqlStr+=@wereStr
-- print @sqlstr

-- EXECUTE sp_executesql @sqlStr


-- go 

-- declare @sdate dateTime=(select DATEADD(MONTH,-1, GETDATE() ))
-- declare @edate dateTime=(select DATEADD(MONTH,1, GETDATE() ))
-- exec pro.uspGetLocations @productID=1,@sDate= @sdate,@eDate=@edate

-- go

-- declare @sdate dateTime=(select DATEADD(MONTH,-1, GETDATE() ))
-- declare @edate dateTime=(select DATEADD(MONTH,1, GETDATE() ))
-- exec pro.uspGetLocations @ownerUserId = 1,@sDate= @sdate,@eDate=@edate


-- go

-- declare @sdate dateTime=(select DATEADD(MONTH,-1, GETDATE() ))
-- exec pro.uspGetLocations @ownerUserId = 1,@sDate= @sdate

-- go 



-- declare @edate dateTime=(select DATEADD(MONTH,1, GETDATE() ))
-- exec pro.uspGetLocations @ownerUserId = 1,@sDate= null,@eDate=@edate



-- GO
-- CREATE PROCEDURE [pro].[uspModifyLocation]
-- --declare
	
-- 	@ProductID int =null,
-- 	@jsonLocationInput nvarchar(max)--=  N'[{"AddressName":"","DateTime":"1650218858000","Longitude":-18.5303879109,"ProductID":1,"latitude":65.9798958978,"lhid":0},{"AddressName":"","DateTime":"1650218953000","Longitude":51.6664299228,"ProductID":1,"latitude":32.6654061513,"lhid":0},{"AddressName":"","DateTime":"1650218959000","Longitude":51.6647583579,"ProductID":1,"latitude":32.6657120605,"lhid":0},{"AddressName":"","DateTime":"1650218964000","Longitude":51.660797476,"ProductID":1,"latitude":32.6658956055,"lhid":0}]'

-- AS
-- BEGIN

-- --insert into dbo.bblbb(pro,inp) values(@ProductID,@jsonLocationInput)
-- --Create table #locations(prodID int, mLong bigint , mLatut bigint,mTime DATETIME2(3))

-- insert into pro.lochis(ProductID,Longitude,latitude,[DateTime],AddressName)
-- select distinct ProductID,Longitude,latitude,pub.ConvertUnixToDateTime([DateTime]),[AddressName] from OpenJson(@jsonLocationInput)
-- with (ProductID int,
-- 	  Longitude float,
-- 	  latitude float,
-- 	  [DateTime] bigint,
-- 	  [AddressName] nvarchar(300)
-- 	  )


-- END


-- go
-- --------begin function------------
-- CREATE FUNCTION pub.ConvertUnixToDateTime
-- (
-- 	-- Add the parameters for the function here
-- 	@unixDateTime  BIGINT
-- )
-- RETURNS DATETIME2(3)
-- AS
-- BEGIN
-- Declare @Result varchar(300)


-- SELECT @Result =  CAST(DATEADD(ms, CAST(RIGHT(@unixDateTime,3) AS SMALLINT), 
-- DATEADD(s, @unixDateTime / 1000, '1970-01-01')) AS DATETIME2(3))


-- 	-- Return the result of the function
-- 	RETURN @Result

-- END
-- GO


-- -------end function------------



-- create proc pro.[modifyOwnerService]
-- @ownerId int 

-- as




-- go

-- create proc pro.[uspGetServiceTitle]
-- @ownerID int

-- as

-- select servid, serviceName, [DateTime], updateTime, IsDeleted, isSystem from pro.[services]

-- go 

-- create proc pro.[uspgetOnerServices]
-- @ownerID int ,
-- @productID int = 0
-- as


-- if isnull(@productID,0) = 0
-- begin
-- 		select sdId, serviceId, ProductId, DateTime, updateTime, IsDeleted, maxValue, value, periodCounter from pro.[servicesDetail]
-- end
-- else
-- begin 
-- 		select sdId, serviceId, ProductId, DateTime, updateTime, IsDeleted, maxValue, value, periodCounter from pro.[servicesDetail] where ProductId= @productID
-- end
