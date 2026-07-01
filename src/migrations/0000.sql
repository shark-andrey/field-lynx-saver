begin;
use `real-times`;
alter table field_lynx drop primary key;
alter table field_lynx add primary key (event_number, round_number, attempt, athlete_id);
commit;
