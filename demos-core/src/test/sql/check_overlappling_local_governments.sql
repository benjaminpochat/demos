select * from (
  select c.name, c.codification, o.overlapping_local_governments_id 
  from local_government c
  left outer join local_government_overlapping_local_governments o on c.id = o.local_government_id
  where c.type = 'FRANCE_COMMUNE') as t
where t.overlapping_local_governments_id is null;

