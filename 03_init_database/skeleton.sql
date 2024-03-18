INSERT INTO workflow.pipe_data (line_id, line_pipe)
SELECT pipe_id, ST_CollectionExtract(ST_StraightSkeleton(pipe), 2)
FROM workflow.raw_pipe_data;