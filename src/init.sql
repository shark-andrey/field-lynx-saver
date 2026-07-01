CREATE TABLE IF NOT EXISTS field_lynx (
    event_number int not null,
    round_number int not null,
    flight_number int,
    place int,
	attempt int,
    athlete_id int not null,
    mark decimal(7, 2),
    wind varchar(255),
	photo varchar(255),
    primary key (event_number, round_number, flight_number, attempt, athlete_id)
);

