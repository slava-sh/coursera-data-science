REGISTER s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar;
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader AS (line:chararray);
ntriples = FOREACH raw GENERATE FLATTEN(myudfs.RDFSplit3(line)) AS (subject:chararray,predicate:chararray,object:chararray) PARALLEL 50;
ntriples_filtered = FILTER ntriples BY subject matches '.*rdfabout\\.com.*' PARALLEL 50;
ntriples_filtered2 = FOREACH ntriples_filtered GENERATE subject AS subject2, predicate AS predicate2, object AS object2 PARALLEL 50;
pairs = JOIN ntriples_filtered BY object, ntriples_filtered2 BY subject2 PARALLEL 50;
pairs_distinct = DISTINCT pairs PARALLEL 50;
answer = FOREACH (GROUP pairs_distinct ALL) GENERATE COUNT(pairs_distinct) PARALLEL 50;
STORE answer INTO '/user/hadoop/answer3b';
