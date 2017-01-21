REGISTER s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar;
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-*' USING TextLoader AS (line:chararray);
ntriples = FOREACH raw GENERATE FLATTEN(myudfs.RDFSplit3(line)) AS (subject:chararray,predicate:chararray,object:chararray) PARALLEL 50;
subjects = GROUP ntriples BY (subject) PARALLEL 50;
count_by_subject = FOREACH subjects GENERATE FLATTEN($0), COUNT($1) AS count PARALLEL 50;
num_subjects_by_count = FOREACH (GROUP count_by_subject BY (count)) GENERATE FLATTEN($0) AS count, COUNT($1) AS num_subjects PARALLEL 50;
answer = FOREACH (GROUP num_subjects_by_count ALL) GENERATE COUNT(num_subjects_by_count) PARALLEL 50;
STORE answer INTO '/user/hadoop/answer4';
