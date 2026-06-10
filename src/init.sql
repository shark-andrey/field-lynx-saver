create table if not exists TABLE_NAME (
    event_number int not null,
    round_number int not null,
    flight_number int not null,
    place int,
	attempt int,
    athlete_id int not null,
    mark decimal(7, 2),
    wind varchar(255),
    photo_file_name varchar(255),
    primary key (event_number, round_number, flight_number, athlete_id)
);

