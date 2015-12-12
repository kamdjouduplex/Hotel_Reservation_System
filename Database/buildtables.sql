
DROP TABLE IF EXISTS Customer;

CREATE TABLE Customer (
  user_name varchar(50) NOT NULL DEFAULT '',
  password varchar(15) NOT NULL,
  email varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (user_name),
  UNIQUE KEY email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO Customer (user_name, password, email)
VALUES
	('C1','password','a@a.com'),
	('C10','password','j@j.com'),
	('C11','password','k@k.com'),
	('C12','password','l@l.com'),
	('C13','password','m@m.com'),
	('C14','password','n@n.com'),
	('C15','password','o@o.com'),
	('C16','password','p@p.com'),
	('C17','password','q@q.com'),
	('C18','password','r@r.com'),
	('C19','password','s@s.com'),
	('C2','password','b@b.com'),
	('C20','password','t@t.com'),
	('C3','password','c@c.com'),
	('C4','password','d@d.com'),
	('C5','password','e@e.com'),
	('C6','password','f@f.com'),
	('C7','password','g@g.com'),
	('C8','password','h@h.com'),
	('C9','password','i@i.com');

DROP TABLE IF EXISTS HotelReview;

CREATE TABLE HotelReview (
  review_number varchar(50) NOT NULL DEFAULT '',
  location varchar(9) NOT NULL DEFAULT '',
  rating varchar(10) NOT NULL DEFAULT '',
  comment varchar(200) DEFAULT NULL,
  user_name varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (review_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO HotelReview (review_number, location, rating, comment, user_name)
VALUES
	('1','Miami','Neutral','It was okay','C1'),
	('10','Atlanta','Excellent','It was fun for the whole family!','C2'),
	('11','Charlotte','Good','It was okay','C2'),
	('12','Savannah','Bad','Awful','C3'),
	('13','Orlando','Neutral','not too bad','C4'),
	('14','Miami','Very Bad','Wish I stayed anywhere else','C5'),
	('15','Atlanta','Neutral','very bland','C6'),
	('16','Charlotte','Bad','','C7'),
	('17','Savannah','Neutral','decent enough','C8'),
	('18','Orlando','Good','','C9'),
	('19','Miami','Neutral','','C10'),
	('2','Atlanta','Excellent','Great!','C1'),
	('20','Charlotte','Neutral','good enough','C2'),
	('21','Orlando','Neutral','','C3'),
	('22','Savannah','Excellent','Thoroughly enjoyable','C4'),
	('23','Miami','Very Bad','Hated it','C4'),
	('3','Atlanta','Neutral','very average','C5'),
	('4','Charlotte','Good','Average :/','C6'),
	('5','Orlando','Neutral','No comment','C7'),
	('6','Savannah','Bad','Terrible','C8'),
	('7','Orlando','Neutral','Nothing spectacular','C8'),
	('8','Miami','Excellent','Exceptional!','C9'),
	('9','Atlanta','Neutral','','C1');

DROP TABLE IF EXISTS Location;

CREATE TABLE Location (
  room_location varchar(9) NOT NULL DEFAULT '',
  PRIMARY KEY (room_location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO Location (room_location)
VALUES
	('Atlanta'),
	('Charlotte'),
	('Miami'),
	('Orlando'),
	('Savannah');

DROP TABLE IF EXISTS Manager;

CREATE TABLE Manager (
  user_name varchar(15) NOT NULL DEFAULT '',
  password varchar(15) NOT NULL DEFAULT '',
  PRIMARY KEY (user_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO Manager (user_name, password)
VALUES
	('M1','password'),
	('M2','password'),
	('M3','password'),
	('M4','password'),
	('M5','password');

DROP TABLE IF EXISTS PaymentInformation;

CREATE TABLE PaymentInformation (
  name_on_card varchar(30) NOT NULL DEFAULT '',
  card_number varchar(16) NOT NULL DEFAULT '',
  expiration_date date NOT NULL,
  cvv int(4) unsigned NOT NULL,
  user_name varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (card_number),
  KEY UserHasPaymentInfo (user_name),
  CONSTRAINT UserHasPaymentInfo FOREIGN KEY (user_name) REFERENCES Customer (user_name) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO PaymentInformation (name_on_card, card_number, expiration_date, cvv, user_name)
VALUES
	('Andy','1111111111111111','2015-12-04',314,'C1'),
	('Andy','1234567891234567','2015-12-04',122,'C1'),
	('NewBob','134252345','2015-12-17',332,'C4'),
	('OtherBob','146523','2015-12-05',433,'C5'),
	('Bob','2222222222222222','2015-12-04',123,'C2'),
	('NewBob','23461536','2016-01-13',233,'C4'),
	('Frankenstein','23462','2016-01-06',345,'C10'),
	('Bobber','235234','2015-12-18',244,'C9'),
	('OtherBob','238591','2015-12-18',323,'C5'),
	('NotSure','28502345','2015-12-11',338,'C7'),
	('Bob','3333333222222222','2015-12-05',344,'C2'),
	('AJ','822365','2016-01-13',245,'C8'),
	('Bobby','85234562','2015-12-04',332,'C3'),
	('Bobby','8884728275','2015-12-04',334,'C3'),
	('AJ','8923','2016-01-22',223,'C8'),
	('Frank','938245','2015-12-08',332,'C6');


DROP TABLE IF EXISTS Reservation;

CREATE TABLE Reservation (
  reservation_id varchar(50) NOT NULL DEFAULT '',
  start_date date NOT NULL,
  end_date date NOT NULL,
  user_name varchar(20) NOT NULL,
  is_cancelled tinyint(1) NOT NULL DEFAULT '0',
  card_number varchar(16) NOT NULL DEFAULT '',
  total_cost int(16) unsigned NOT NULL,
  PRIMARY KEY (reservation_id),
  KEY ReservationHasCustomer (user_name),
  KEY ReservationHasPaymentInfo (card_number),
  CONSTRAINT ReservationHasCustomer FOREIGN KEY (user_name) REFERENCES Customer (user_name),
  CONSTRAINT ReservationHasPaymentInfo FOREIGN KEY (card_number) REFERENCES PaymentInformation (card_number) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO Reservation (reservation_id, start_date, end_date, user_name, is_cancelled, card_number, total_cost)
VALUES
	('0e4f3514-00a6-4c25-8556-9203f9fba6a5','2015-11-18','2015-12-06','C3',0,'8884728275',6120),
	('0f33646d-0be0-4feb-8e67-5304479bb135','2015-09-23','2015-09-24','C5',0,'238591',170),
	('0feae7cb-39f4-4bc5-9826-9d0f5e1f21d0','2015-12-05','2015-12-06','C10',1,'23462',0),
	('13a2d720-e5a7-4a71-bdca-a91da5442bc2','2015-09-15','2015-09-17','C7',0,'28502345',680),
	('14ccde1a-0eb0-46a1-b03e-7feae82252a2','2015-09-22','2015-09-23','C3',0,'8884728275',170),
	('19e70db3-6cc2-4c49-aeed-f0fd003d2033','2015-12-17','2015-12-18','C5',0,'146523',170),
	('232bf1ee-4ce7-4ad9-be0e-550aa2ac912e','2016-01-07','2016-01-08','C8',0,'8923',250),
	('2d921ca9-7696-42cb-afce-7d1a4fc99d7c','2015-12-10','2015-12-11','C8',0,'822365',250),
	('30771cc0-6de5-47cf-93d1-af8dc38b1319','2015-08-06','2015-12-04','C1',0,'1111111111111111',340),
	('330af966-fea3-4e09-9f24-40683c857d69','2015-09-16','2015-12-09','C1',0,'1111111111111111',49560),
	('36b597dc-9ecd-400e-8362-a17087840d31','2015-09-16','2015-09-24','C2',0,'2222222222222222',5920),
	('38f2482e-52f8-4fe5-9891-4c354e8a27a3','2015-09-08','2016-01-14','C2',0,'3333333222222222',71680),
	('3a6fcefc-1842-43a2-86d7-dd42e5555d24','2015-11-26','2015-12-03','C7',0,'28502345',700),
	('3af87a5b-a553-40af-9e7d-20dce27f17b6','2015-12-05','2015-12-09','C10',0,'23462',1600),
	('42885545-148a-44a7-89fc-40c8426e29df','2016-01-02','2016-01-03','C10',0,'23462',390),
	('49f9180a-5a9a-4c4d-9d78-89db1d043b47','2015-12-06','2015-12-07','C10',0,'23462',350),
	('4f7f62c4-7b09-4743-beff-000f12921015','2015-09-08','2015-09-10','C6',1,'938245',340),
	('502fa9c0-e888-426f-8a0e-3c4e2f1818fa','2015-11-28','2015-12-06','C6',0,'938245',2000),
	('51945cf0-09f0-4a44-aff5-e1edff4a629d','2015-08-26','2015-08-27','C10',1,'23462',400),
	('5992afde-86ce-4164-a519-77a37574c7ac','2015-09-09','2015-09-17','C1',0,'1111111111111111',2160),
	('62c6f8d5-93b9-40f5-9434-0e96a633aec2','2015-08-25','2015-08-26','C8',0,'822365',420),
	('687cf9b8-ef83-4779-a5ca-ab7a12dd7e8e','2015-08-11','2015-08-12','C9',0,'235234',250),
	('753a56aa-570a-4c55-8101-a1cca454f774','2015-12-04','2015-12-05','C10',0,'23462',170),
	('75b8c64f-84fe-4c54-b1aa-d3f24930f735','2015-08-27','2015-08-28','C10',0,'23462',500),
	('7a4fb311-fed2-42b2-ae17-3bf99668afec','2015-12-03','2015-12-06','C7',1,'28502345',0),
	('7b01fbf8-37b0-4621-a2c2-e54797df1510','2015-08-05','2015-08-07','C5',0,'146523',640),
	('7c2bf312-bad3-49db-b776-7c6b232632d7','2015-08-11','2015-08-12','C7',0,'28502345',400),
	('7c889f25-553b-4c2c-8587-c097e2186529','2015-08-16','2015-08-19','C8',0,'822365',1260),
	('849701c7-35f3-41da-931a-8cc4279e1770','2016-01-01','2016-01-02','C9',0,'235234',100),
	('856e3082-2055-49a3-923f-c327e74cdeb5','2015-12-03','2015-12-04','C10',1,'23462',0),
	('89c63356-3997-497b-b006-7433e8d09065','2015-12-23','2015-12-25','C6',0,'938245',340),
	('8bceb025-7d53-4604-b8e9-e704714859a6','2015-09-24','2015-09-27','C9',1,'235234',1170),
	('8dff8dcc-80eb-4d18-8254-111f707597be','2015-10-15','2015-10-16','C10',0,'23462',350),
	('8f5dfaf3-b79b-42c9-9079-1e133952fe1a','2015-09-06','2015-12-20','C2',1,'3333333222222222',23100),
	('911d3453-cfe9-4c8e-8d13-fe4eec8591a6','2015-12-02','2015-12-07','C4',0,'134252345',850),
	('9554a0bc-4b80-4ea2-9049-c1528c64fdb2','2015-09-15','2015-09-16','C5',0,'146523',500),
	('96e0b50a-c0f6-484c-b47b-1d428fed0ba2','2016-01-18','2016-01-19','C10',0,'23462',470),
	('98247a04-c9ea-4097-9daf-c0ad1e1dcd94','2015-09-09','2015-09-11','C10',0,'23462',1300),
	('9c449b58-82c2-487f-b682-70783f619ed9','2015-08-11','2015-08-12','C4',0,'23461536',170),
	('a3e8f9df-1eff-4607-a4d7-3c830e4f6eb8','2015-12-08','2015-12-23','C1',0,'1234567891234567',8850),
	('a4dbf87c-9fa0-4b2f-85e8-a15b4010c147','2015-08-01','2015-08-03','C1',0,'1234567891234567',340),
	('ac8138ab-c78e-466a-b284-f727368bef11','2015-11-25','2015-12-07','C5',1,'146523',2040),
	('af7714cc-f117-4e72-8252-f7f74103b0c7','2016-01-01','2016-01-03','C10',0,'23462',840),
	('b4df9536-9602-4192-8782-b638d7fe4a18','2015-12-09','2015-12-10','C3',0,'8884728275',250),
	('b85a04c8-a3f4-4653-a806-37aa540d1b2a','2015-10-06','2015-10-08','C10',0,'23462',680),
	('bb8f7c19-a46f-472d-bd49-af5d589a9d14','2016-01-07','2016-01-08','C3',1,'8884728275',0),
	('bd8a344b-6307-4acd-a5f6-a79ed2b477c1','2015-11-28','2015-12-07','C4',1,'134252345',3600),
	('bf69414f-80e3-474c-ac03-991a6b562956','2015-09-16','2015-09-17','C4',0,'134252345',170),
	('c5b0cc32-dbec-425c-a357-29339574e5c3','2015-08-02','2015-08-05','C1',1,'1111111111111111',1170),
	('d5bbd467-c0cb-4f9e-ac76-42d26d079233','2015-12-09','2015-12-17','C2',0,'2222222222222222',7280),
	('dd87f155-4e36-442f-9c3b-25c2e8a3ddd6','2015-08-19','2015-09-10','C4',0,'23461536',8800),
	('de036f08-a02d-4a23-a913-62e74a29c9fb','2015-08-11','2015-08-13','C3',0,'8884728275',940),
	('de801bb9-cd47-492c-9b8c-a9f6af9c09f3','2015-08-11','2015-08-12','C6',0,'938245',270),
	('e165c2c2-f1c9-409f-8768-02cd341cd813','2015-08-19','2015-08-20','C9',1,'235234',400),
	('e5c88ccf-fc77-4473-bb19-bbb51b72f7c0','2016-01-01','2016-01-06','C6',0,'938245',2100),
	('ebbf9e64-18a5-456e-9178-ae6ba256a20f','2015-12-03','2015-12-05','C10',1,'23462',0),
	('ed83a384-d2b8-4918-b714-cf29f71b2bc1','2015-12-12','2015-12-13','C8',0,'822365',220),
	('f5cb890c-a1bd-493d-a880-d7cb02d78a8f','2016-01-29','2016-01-31','C10',0,'23462',1000),
	('fa1b62d7-1c07-43cb-9bba-55751bc94f3a','2016-01-13','2016-01-20','C7',0,'28502345',2940),
	('fb1f43b8-3186-461c-a71c-ae540890aaa0','2015-12-05','2015-12-06','C10',0,'23462',250),
	('fc68b804-0386-4611-a346-18ba52d09f56','2015-09-30','2015-12-03','C10',0,'23462',20480),
	('fd4d2076-b9bb-4fe3-bab0-c15afd3af428','2015-08-12','2015-08-20','C2',0,'3333333222222222',4480);


DROP TABLE IF EXISTS ReservationHasRooms;

CREATE TABLE ReservationHasRooms (
  reservation_id varchar(50) NOT NULL DEFAULT '',
  room_location varchar(9) NOT NULL DEFAULT '',
  room_number int(3) unsigned NOT NULL DEFAULT '0',
  has_extra_bed tinyint(4) DEFAULT NULL,
  PRIMARY KEY (reservation_id,room_location,room_number),
  KEY ReservationHasRoomNumbers (room_number),
  CONSTRAINT ReservationHasID FOREIGN KEY (reservation_id) REFERENCES Reservation (reservation_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT ReservationHasRoomNumbers FOREIGN KEY (room_number) REFERENCES Room (room_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO ReservationHasRooms (reservation_id, room_location, room_number, has_extra_bed)
VALUES
	('0e4f3514-00a6-4c25-8556-9203f9fba6a5','Orlando',111,0),
	('0e4f3514-00a6-4c25-8556-9203f9fba6a5','Orlando',555,1),
	('0f33646d-0be0-4feb-8e67-5304479bb135','Orlando',888,1),
	('0feae7cb-39f4-4bc5-9826-9d0f5e1f21d0','Atlanta',0,1),
	('0feae7cb-39f4-4bc5-9826-9d0f5e1f21d0','Atlanta',1,0),
	('13a2d720-e5a7-4a71-bdca-a91da5442bc2','Charlotte',777,0),
	('13a2d720-e5a7-4a71-bdca-a91da5442bc2','Charlotte',888,1),
	('14ccde1a-0eb0-46a1-b03e-7feae82252a2','Charlotte',555,1),
	('19e70db3-6cc2-4c49-aeed-f0fd003d2033','Miami',888,1),
	('232bf1ee-4ce7-4ad9-be0e-550aa2ac912e','Atlanta',660,0),
	('2d921ca9-7696-42cb-afce-7d1a4fc99d7c','Savannah',660,0),
	('30771cc0-6de5-47cf-93d1-af8dc38b1319','Miami',888,1),
	('330af966-fea3-4e09-9f24-40683c857d69','Savannah',333,0),
	('330af966-fea3-4e09-9f24-40683c857d69','Savannah',777,0),
	('330af966-fea3-4e09-9f24-40683c857d69','Savannah',888,1),
	('36b597dc-9ecd-400e-8362-a17087840d31','Savannah',222,1),
	('36b597dc-9ecd-400e-8362-a17087840d31','Savannah',444,0),
	('36b597dc-9ecd-400e-8362-a17087840d31','Savannah',660,1),
	('38f2482e-52f8-4fe5-9891-4c354e8a27a3','Atlanta',444,1),
	('38f2482e-52f8-4fe5-9891-4c354e8a27a3','Atlanta',555,1),
	('38f2482e-52f8-4fe5-9891-4c354e8a27a3','Atlanta',777,0),
	('3a6fcefc-1842-43a2-86d7-dd42e5555d24','Savannah',555,0),
	('3af87a5b-a553-40af-9e7d-20dce27f17b6','Savannah',999,1),
	('42885545-148a-44a7-89fc-40c8426e29df','Savannah',444,1),
	('42885545-148a-44a7-89fc-40c8426e29df','Savannah',555,1),
	('49f9180a-5a9a-4c4d-9d78-89db1d043b47','Orlando',333,0),
	('49f9180a-5a9a-4c4d-9d78-89db1d043b47','Orlando',555,0),
	('4f7f62c4-7b09-4743-beff-000f12921015','Miami',0,0),
	('502fa9c0-e888-426f-8a0e-3c4e2f1818fa','Savannah',660,0),
	('51945cf0-09f0-4a44-aff5-e1edff4a629d','Atlanta',0,1),
	('5992afde-86ce-4164-a519-77a37574c7ac','Atlanta',222,0),
	('5992afde-86ce-4164-a519-77a37574c7ac','Atlanta',888,1),
	('62c6f8d5-93b9-40f5-9434-0e96a633aec2','Atlanta',660,0),
	('62c6f8d5-93b9-40f5-9434-0e96a633aec2','Atlanta',888,1),
	('687cf9b8-ef83-4779-a5ca-ab7a12dd7e8e','Atlanta',999,0),
	('753a56aa-570a-4c55-8101-a1cca454f774','Miami',111,0),
	('75b8c64f-84fe-4c54-b1aa-d3f24930f735','Savannah',555,0),
	('75b8c64f-84fe-4c54-b1aa-d3f24930f735','Savannah',660,1),
	('7a4fb311-fed2-42b2-ae17-3bf99668afec','Atlanta',0,0),
	('7b01fbf8-37b0-4621-a2c2-e54797df1510','Atlanta',111,1),
	('7b01fbf8-37b0-4621-a2c2-e54797df1510','Atlanta',555,0),
	('7c2bf312-bad3-49db-b776-7c6b232632d7','Miami',660,1),
	('7c889f25-553b-4c2c-8587-c097e2186529','Orlando',222,1),
	('7c889f25-553b-4c2c-8587-c097e2186529','Orlando',660,0),
	('849701c7-35f3-41da-931a-8cc4279e1770','Charlotte',555,0),
	('856e3082-2055-49a3-923f-c327e74cdeb5','Orlando',0,1),
	('89c63356-3997-497b-b006-7433e8d09065','Atlanta',222,1),
	('8bceb025-7d53-4604-b8e9-e704714859a6','Charlotte',0,0),
	('8bceb025-7d53-4604-b8e9-e704714859a6','Charlotte',1,1),
	('8dff8dcc-80eb-4d18-8254-111f707597be','Charlotte',222,0),
	('8dff8dcc-80eb-4d18-8254-111f707597be','Charlotte',999,0),
	('8f5dfaf3-b79b-42c9-9079-1e133952fe1a','Savannah',0,1),
	('911d3453-cfe9-4c8e-8d13-fe4eec8591a6','Miami',222,1),
	('9554a0bc-4b80-4ea2-9049-c1528c64fdb2','Charlotte',222,0),
	('9554a0bc-4b80-4ea2-9049-c1528c64fdb2','Charlotte',333,1),
	('96e0b50a-c0f6-484c-b47b-1d428fed0ba2','Charlotte',111,1),
	('96e0b50a-c0f6-484c-b47b-1d428fed0ba2','Charlotte',333,0),
	('98247a04-c9ea-4097-9daf-c0ad1e1dcd94','Savannah',333,0),
	('98247a04-c9ea-4097-9daf-c0ad1e1dcd94','Savannah',999,1),
	('9c449b58-82c2-487f-b682-70783f619ed9','Savannah',555,1),
	('a3e8f9df-1eff-4607-a4d7-3c830e4f6eb8','Orlando',111,0),
	('a3e8f9df-1eff-4607-a4d7-3c830e4f6eb8','Orlando',333,0),
	('a3e8f9df-1eff-4607-a4d7-3c830e4f6eb8','Orlando',555,1),
	('a4dbf87c-9fa0-4b2f-85e8-a15b4010c147','Savannah',777,0),
	('ac8138ab-c78e-466a-b284-f727368bef11','Savannah',0,0),
	('af7714cc-f117-4e72-8252-f7f74103b0c7','Savannah',777,0),
	('af7714cc-f117-4e72-8252-f7f74103b0c7','Savannah',999,0),
	('b4df9536-9602-4192-8782-b638d7fe4a18','Miami',660,0),
	('b85a04c8-a3f4-4653-a806-37aa540d1b2a','Orlando',444,0),
	('b85a04c8-a3f4-4653-a806-37aa540d1b2a','Orlando',888,1),
	('bb8f7c19-a46f-472d-bd49-af5d589a9d14','Savannah',0,1),
	('bb8f7c19-a46f-472d-bd49-af5d589a9d14','Savannah',1,0),
	('bd8a344b-6307-4acd-a5f6-a79ed2b477c1','Charlotte',0,1),
	('bf69414f-80e3-474c-ac03-991a6b562956','Savannah',555,1),
	('c5b0cc32-dbec-425c-a357-29339574e5c3','Charlotte',0,1),
	('c5b0cc32-dbec-425c-a357-29339574e5c3','Charlotte',1,0),
	('d5bbd467-c0cb-4f9e-ac76-42d26d079233','Miami',111,0),
	('d5bbd467-c0cb-4f9e-ac76-42d26d079233','Miami',333,0),
	('d5bbd467-c0cb-4f9e-ac76-42d26d079233','Miami',444,1),
	('d5bbd467-c0cb-4f9e-ac76-42d26d079233','Miami',555,1),
	('d5bbd467-c0cb-4f9e-ac76-42d26d079233','Miami',888,0),
	('dd87f155-4e36-442f-9c3b-25c2e8a3ddd6','Atlanta',333,1),
	('de036f08-a02d-4a23-a913-62e74a29c9fb','Atlanta',111,1),
	('de036f08-a02d-4a23-a913-62e74a29c9fb','Atlanta',333,0),
	('de801bb9-cd47-492c-9b8c-a9f6af9c09f3','Orlando',111,0),
	('de801bb9-cd47-492c-9b8c-a9f6af9c09f3','Orlando',222,0),
	('e165c2c2-f1c9-409f-8768-02cd341cd813','Atlanta',0,1),
	('e5c88ccf-fc77-4473-bb19-bbb51b72f7c0','Charlotte',222,1),
	('e5c88ccf-fc77-4473-bb19-bbb51b72f7c0','Charlotte',660,0),
	('ebbf9e64-18a5-456e-9178-ae6ba256a20f','Savannah',0,0),
	('ed83a384-d2b8-4918-b714-cf29f71b2bc1','Miami',777,1),
	('f5cb890c-a1bd-493d-a880-d7cb02d78a8f','Savannah',333,1),
	('f5cb890c-a1bd-493d-a880-d7cb02d78a8f','Savannah',888,0),
	('fa1b62d7-1c07-43cb-9bba-55751bc94f3a','Orlando',111,0),
	('fa1b62d7-1c07-43cb-9bba-55751bc94f3a','Orlando',333,0),
	('fb1f43b8-3186-461c-a71c-ae540890aaa0','Orlando',999,0),
	('fc68b804-0386-4611-a346-18ba52d09f56','Atlanta',111,1),
	('fc68b804-0386-4611-a346-18ba52d09f56','Atlanta',888,0),
	('fd4d2076-b9bb-4fe3-bab0-c15afd3af428','Charlotte',444,1),
	('fd4d2076-b9bb-4fe3-bab0-c15afd3af428','Charlotte',777,0),
	('fd4d2076-b9bb-4fe3-bab0-c15afd3af428','Charlotte',888,1);

DROP TABLE IF EXISTS Room;

CREATE TABLE Room (
  room_number int(3) unsigned NOT NULL DEFAULT '0',
  room_category varchar(15) NOT NULL DEFAULT '',
  room_location varchar(9) NOT NULL DEFAULT '',
  PRIMARY KEY (room_number,room_location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO Room (room_number, room_category, room_location)
VALUES
	(111,'Family','Atlanta'),
	(111,'Family','Charlotte'),
	(111,'Family','Miami'),
	(111,'Family','Orlando'),
	(111,'Family','Savannah'),
	(222,'Standard','Atlanta'),
	(222,'Standard','Charlotte'),
	(222,'Standard','Miami'),
	(222,'Standard','Orlando'),
	(222,'Standard','Savannah'),
	(333,'Suite','Atlanta'),
	(333,'Suite','Charlotte'),
	(333,'Suite','Miami'),
	(333,'Suite','Orlando'),
	(333,'Suite','Savannah'),
	(444,'Family','Atlanta'),
	(444,'Family','Charlotte'),
	(444,'Family','Miami'),
	(444,'Family','Orlando'),
	(444,'Family','Savannah'),
	(555,'Standard','Atlanta'),
	(555,'Standard','Charlotte'),
	(555,'Standard','Miami'),
	(555,'Standard','Orlando'),
	(555,'Standard','Savannah'),
	(660,'Suite','Atlanta'),
	(660,'Suite','Charlotte'),
	(660,'Suite','Miami'),
	(660,'Suite','Orlando'),
	(660,'Suite','Savannah'),
	(777,'Family','Atlanta'),
	(777,'Family','Charlotte'),
	(777,'Family','Miami'),
	(777,'Family','Orlando'),
	(777,'Family','Savannah'),
	(888,'Standard','Atlanta'),
	(888,'Standard','Charlotte'),
	(888,'Standard','Miami'),
	(888,'Standard','Orlando'),
	(888,'Standard','Savannah'),
	(999,'Suite','Atlanta'),
	(999,'Suite','Charlotte'),
	(999,'Suite','Miami'),
	(999,'Suite','Orlando'),
	(999,'Suite','Savannah');


DROP TABLE IF EXISTS RoomType;

CREATE TABLE RoomType (
  room_category varchar(15) NOT NULL DEFAULT '',
  number_people int(1) DEFAULT NULL,
  cost int(3) DEFAULT NULL,
  cost_extra_bed int(3) DEFAULT NULL,
  PRIMARY KEY (room_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO RoomType (room_category, number_people, cost, cost_extra_bed)
VALUES
	('Family',4,170,50),
	('Standard',2,100,70),
	('Suite',4,250,150);

