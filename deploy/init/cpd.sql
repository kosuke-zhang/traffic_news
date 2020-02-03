create schema if not exists news collate utf8mb4_unicode_ci;

use news;

create table if not exists cpd_news
(
	id varchar(40) not null,
	url varchar(255) not null,
	title varchar(50) not null,
	content text not null,
	category varchar(5) not null,
	source varchar(50) not null,
	date varchar(30) not null,
	news_id varchar(50) not null,
	page int not null,
	constraint data_id_uindex
		unique (id)
);

alter table data
	add primary key (id);
