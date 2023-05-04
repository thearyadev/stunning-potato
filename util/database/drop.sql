drop trigger if exists update_rating_average_trigger on rating cascade;


drop table if exists film_actress_rating cascade;

drop table if exists actress cascade;
drop table if exists rating cascade;





drop type if exists film_state cascade;
drop table if exists film cascade;

drop function if exists update_rating_average cascade;