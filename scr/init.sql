create table if not exists TABLE_NAME (
    event_number int not null,
    round_number int not null,
    heat_number int not null,
    place varchar(255),
    athlete_id int not null,
    lane int,
    timing varchar(255),
    react_time decimal(7, 2),
    wind varchar(255),
    photo_file_name varchar(255),
    competition_id int not null,
    primary key (event_number, round_number, heat_number, athlete_id)
);
