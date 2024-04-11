begin;
use `ekb.real-times`;
alter table finish_lynx add column competition_id int not null default 0;
alter table finish_lynx drop primary key;
alter table finish_lynx add primary key (event_number, round_number, heat_number, athlete_id, competition_id);
commit;
