REGISTER s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar;
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader AS (line:chararray);
ntriples = FOREACH raw GENERATE FLATTEN(myudfs.RDFSplit3(line)) AS (subject:chararray,predicate:chararray,object:chararray) PARALLEL 50;
objects = GROUP ntriples BY (object) PARALLEL 50;
count_by_object = FOREACH objects GENERATE FLATTEN($0), COUNT($1) AS count PARALLEL 50;
count_by_object_ordered = ORDER count_by_object BY (count) PARALLEL 50;
answer = FOREACH (GROUP count_by_object ALL) GENERATE COUNT(count_by_object) PARALLEL 50;
STORE answer INTO 's3n://slava-coursera-data-science/answer1';
