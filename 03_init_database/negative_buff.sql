SELECT line_id , line_pipe  
FROM workflow.pipe_data,
(SELECT ST_Buffer(workflow.raw_pipe_data.pipe, (-1)::double precision) AS geom FROM workflow.raw_pipe_data) AS buff
WHERE NOT(ST_Crosses(workflow.pipe_data.line_pipe, buff.geom))
