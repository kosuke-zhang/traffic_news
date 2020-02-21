create schema if not exists news collate utf8mb4_unicode_ci;

use news;

create table if not exists cpd_news
(
	news_id varchar(50) not null primary key,
	title varchar(255) not null,
	category varchar(5) not null,
	source varchar(50) not null,
	date varchar(30) not null,
	page_total int not null,
	entry_time datetime not null default CURRENT_TIMESTAMP  comment '入库时间',
	constraint data_id_uindex
        unique (news_id)
);

create table if not exists cpd_news_content
(
	news_id varchar(40) not null primary key,
	request_id varchar(40) not null,
	url varchar(255) not null,
	content text not null,
	page int not null,
	constraint data_id_uindex
        unique (request_id),
	FOREIGN KEY fk_news(news_id)
    REFERENCES cpd_news(news_id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);
