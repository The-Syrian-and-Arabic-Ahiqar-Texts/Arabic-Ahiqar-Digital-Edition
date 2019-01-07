/*
 Navicat Premium Data Transfer

 Source Server         : brown-devost.com AWS
 Source Server Type    : PostgreSQL
 Source Server Version : 90512
 Source Host           : localhost:5432
 Source Catalog        : ahiqar
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 90512
 File Encoding         : 65001

 Date: 21/05/2018 23:17:37
*/


-- ----------------------------
-- Sequence structure for col_col_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."col_col_id_seq";
CREATE SEQUENCE "public"."col_col_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for line_line_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."line_line_id_seq";
CREATE SEQUENCE "public"."line_line_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for manuscript_manuscript_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."manuscript_manuscript_id_seq";
CREATE SEQUENCE "public"."manuscript_manuscript_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for page_page_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."page_page_id_seq";
CREATE SEQUENCE "public"."page_page_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for parallel_group_parallel_group_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."parallel_group_parallel_group_id_seq";
CREATE SEQUENCE "public"."parallel_group_parallel_group_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for url_url_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."url_url_id_seq";
CREATE SEQUENCE "public"."url_url_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for col
-- ----------------------------
DROP TABLE IF EXISTS "public"."col";
CREATE TABLE "public"."col" (
  "col_name" text COLLATE "pg_catalog"."default",
  "col_id" int4 NOT NULL DEFAULT nextval('col_col_id_seq'::regclass),
  "page_id" int4 NOT NULL
)
;
ALTER TABLE "public"."col" OWNER TO "postgres";

-- ----------------------------
-- Table structure for line
-- ----------------------------
DROP TABLE IF EXISTS "public"."line";
CREATE TABLE "public"."line" (
  "line_name" text COLLATE "pg_catalog"."default",
  "line_id" int4 NOT NULL DEFAULT nextval('line_line_id_seq'::regclass),
  "col_id" int4
)
;
ALTER TABLE "public"."line" OWNER TO "postgres";

-- ----------------------------
-- Table structure for manuscript
-- ----------------------------
DROP TABLE IF EXISTS "public"."manuscript";
CREATE TABLE "public"."manuscript" (
  "manuscript_name" text COLLATE "pg_catalog"."default" NOT NULL,
  "manuscript_id" int4 NOT NULL DEFAULT nextval('manuscript_manuscript_id_seq'::regclass)
)
;
ALTER TABLE "public"."manuscript" OWNER TO "postgres";

-- ----------------------------
-- Table structure for page
-- ----------------------------
DROP TABLE IF EXISTS "public"."page";
CREATE TABLE "public"."page" (
  "page_name" text COLLATE "pg_catalog"."default",
  "page_id" int4 NOT NULL DEFAULT nextval('page_page_id_seq'::regclass),
  "manuscript_id" int4 NOT NULL,
  "url_id" int4,
  "filename" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."page" OWNER TO "postgres";

-- ----------------------------
-- Table structure for parallel_group
-- ----------------------------
DROP TABLE IF EXISTS "public"."parallel_group";
CREATE TABLE "public"."parallel_group" (
  "parallel_group_id" int4 NOT NULL DEFAULT nextval('parallel_group_parallel_group_id_seq'::regclass)
)
;
ALTER TABLE "public"."parallel_group" OWNER TO "postgres";

-- ----------------------------
-- Table structure for parallel_group_to_parallel_group
-- ----------------------------
DROP TABLE IF EXISTS "public"."parallel_group_to_parallel_group";
CREATE TABLE "public"."parallel_group_to_parallel_group" (
  "parallel_group_id_1" int4 NOT NULL,
  "parallel_group_id_2" int4 NOT NULL
)
;
ALTER TABLE "public"."parallel_group_to_parallel_group" OWNER TO "postgres";

-- ----------------------------
-- Table structure for url
-- ----------------------------
DROP TABLE IF EXISTS "public"."url";
CREATE TABLE "public"."url" (
  "url_id" int4 NOT NULL DEFAULT nextval('url_url_id_seq'::regclass),
  "url" text COLLATE "pg_catalog"."default" NOT NULL
)
;
ALTER TABLE "public"."url" OWNER TO "postgres";

-- ----------------------------
-- Table structure for word
-- ----------------------------
DROP TABLE IF EXISTS "public"."word";
CREATE TABLE "public"."word" (
  "word_address" char(255) COLLATE "pg_catalog"."default" NOT NULL DEFAULT NULL::bpchar,
  "surface" text COLLATE "pg_catalog"."default" NOT NULL,
  "parallel_group_id" int4,
  "position_in_document" int4,
  "line_id" int4
)
;
ALTER TABLE "public"."word" OWNER TO "postgres";

-- ----------------------------
-- Table structure for word_to_word
-- ----------------------------
DROP TABLE IF EXISTS "public"."word_to_word";
CREATE TABLE "public"."word_to_word" (
  "word_address" char(255) COLLATE "pg_catalog"."default" NOT NULL DEFAULT NULL::bpchar,
  "parallel_address" char(255) COLLATE "pg_catalog"."default" NOT NULL DEFAULT NULL::bpchar
)
;
ALTER TABLE "public"."word_to_word" OWNER TO "postgres";

-- ----------------------------
-- Function structure for parallel_groups_by_manuscript_id
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."parallel_groups_by_manuscript_id"("ms_id" int4);
CREATE OR REPLACE FUNCTION "public"."parallel_groups_by_manuscript_id"("ms_id" int4)
  RETURNS SETOF "public"."parallel_group" AS $BODY$BEGIN
  RETURN QUERY SELECT parallel_group.*
		FROM parallel_group
			JOIN (
				SELECT DISTINCT parallel_group_id, min(position_in_document) AS min_position_in_document, min(line_id) AS min_line_id
				FROM word
				GROUP BY parallel_group_id
			) word_filtered 
				ON word_filtered.parallel_group_id = parallel_group.parallel_group_id
			JOIN line ON word_filtered.min_line_id = line.line_id
			JOIN col USING(col_id)
			JOIN page USING(page_id)
			JOIN manuscript USING(manuscript_id)
		WHERE manuscript_id = ms_id
		ORDER BY word_filtered.min_position_in_document ASC;
END
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100
  ROWS 1000;

-- ----------------------------
-- Function structure for parallel_groups_by_page_id
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."parallel_groups_by_page_id"("pid" int4);
CREATE OR REPLACE FUNCTION "public"."parallel_groups_by_page_id"("pid" int4)
  RETURNS SETOF "public"."parallel_group" AS $BODY$BEGIN
  RETURN QUERY SELECT DISTINCT parallel_group.*
		FROM parallel_group
			JOIN word USING(parallel_group_id)
			JOIN line USING(line_id)
			JOIN col USING(col_id)
			JOIN page USING(page_id)
		WHERE page_id = pid;
END
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100
  ROWS 1000;

-- ----------------------------
-- Function structure for word_by_position_in_document
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."word_by_position_in_document"("pid" int4);
CREATE OR REPLACE FUNCTION "public"."word_by_position_in_document"("pid" int4)
  RETURNS SETOF "public"."word" AS $BODY$BEGIN
  RETURN QUERY SELECT * FROM word WHERE position_in_document = pid;
END
$BODY$
  LANGUAGE plpgsql STABLE
  COST 100
  ROWS 1000;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."col_col_id_seq"
OWNED BY "public"."col"."col_id";
SELECT setval('"public"."col_col_id_seq"', 236, true);
ALTER SEQUENCE "public"."line_line_id_seq"
OWNED BY "public"."line"."line_id";
SELECT setval('"public"."line_line_id_seq"', 4190, true);
ALTER SEQUENCE "public"."manuscript_manuscript_id_seq"
OWNED BY "public"."manuscript"."manuscript_id";
SELECT setval('"public"."manuscript_manuscript_id_seq"', 6, true);
ALTER SEQUENCE "public"."page_page_id_seq"
OWNED BY "public"."page"."page_id";
SELECT setval('"public"."page_page_id_seq"', 236, true);
ALTER SEQUENCE "public"."parallel_group_parallel_group_id_seq"
OWNED BY "public"."parallel_group"."parallel_group_id";
SELECT setval('"public"."parallel_group_parallel_group_id_seq"', 3, false);
ALTER SEQUENCE "public"."url_url_id_seq"
OWNED BY "public"."url"."url_id";
SELECT setval('"public"."url_url_id_seq"', 2, true);

-- ----------------------------
-- Primary Key structure for table col
-- ----------------------------
ALTER TABLE "public"."col" ADD CONSTRAINT "col_pkey" PRIMARY KEY ("col_id");

-- ----------------------------
-- Primary Key structure for table line
-- ----------------------------
ALTER TABLE "public"."line" ADD CONSTRAINT "line_pkey" PRIMARY KEY ("line_id");

-- ----------------------------
-- Primary Key structure for table manuscript
-- ----------------------------
ALTER TABLE "public"."manuscript" ADD CONSTRAINT "manuscript_pkey" PRIMARY KEY ("manuscript_id");

-- ----------------------------
-- Primary Key structure for table page
-- ----------------------------
ALTER TABLE "public"."page" ADD CONSTRAINT "page_pkey" PRIMARY KEY ("page_id");

-- ----------------------------
-- Primary Key structure for table parallel_group
-- ----------------------------
ALTER TABLE "public"."parallel_group" ADD CONSTRAINT "parallel_group_pkey" PRIMARY KEY ("parallel_group_id");

-- ----------------------------
-- Primary Key structure for table parallel_group_to_parallel_group
-- ----------------------------
ALTER TABLE "public"."parallel_group_to_parallel_group" ADD CONSTRAINT "parallel_group_to_parallel_group_pkey" PRIMARY KEY ("parallel_group_id_1", "parallel_group_id_2");

-- ----------------------------
-- Uniques structure for table url
-- ----------------------------
ALTER TABLE "public"."url" ADD CONSTRAINT "unique_url" UNIQUE ("url");

-- ----------------------------
-- Primary Key structure for table url
-- ----------------------------
ALTER TABLE "public"."url" ADD CONSTRAINT "url_pkey" PRIMARY KEY ("url_id");

-- ----------------------------
-- Uniques structure for table word
-- ----------------------------
ALTER TABLE "public"."word" ADD CONSTRAINT "unique_word_to_word_group" UNIQUE ("word_address", "parallel_group_id");

-- ----------------------------
-- Primary Key structure for table word
-- ----------------------------
ALTER TABLE "public"."word" ADD CONSTRAINT "word_pkey" PRIMARY KEY ("word_address");

-- ----------------------------
-- Primary Key structure for table word_to_word
-- ----------------------------
ALTER TABLE "public"."word_to_word" ADD CONSTRAINT "word_to_word_pkey" PRIMARY KEY ("word_address", "parallel_address");

-- ----------------------------
-- Foreign Keys structure for table col
-- ----------------------------
ALTER TABLE "public"."col" ADD CONSTRAINT "col_to_page" FOREIGN KEY ("page_id") REFERENCES "public"."page" ("page_id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table line
-- ----------------------------
ALTER TABLE "public"."line" ADD CONSTRAINT "line_to_col" FOREIGN KEY ("col_id") REFERENCES "public"."col" ("col_id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table page
-- ----------------------------
ALTER TABLE "public"."page" ADD CONSTRAINT "page_to_manuscript" FOREIGN KEY ("manuscript_id") REFERENCES "public"."manuscript" ("manuscript_id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."page" ADD CONSTRAINT "page_to_url_id" FOREIGN KEY ("url_id") REFERENCES "public"."url" ("url_id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table parallel_group_to_parallel_group
-- ----------------------------
ALTER TABLE "public"."parallel_group_to_parallel_group" ADD CONSTRAINT "parallel_group_1_to_parallel_group" FOREIGN KEY ("parallel_group_id_1") REFERENCES "public"."parallel_group" ("parallel_group_id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "public"."parallel_group_to_parallel_group" ADD CONSTRAINT "parallel_group_2_to_parallel_group" FOREIGN KEY ("parallel_group_id_2") REFERENCES "public"."parallel_group" ("parallel_group_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- ----------------------------
-- Foreign Keys structure for table word
-- ----------------------------
ALTER TABLE "public"."word" ADD CONSTRAINT "word_to_line" FOREIGN KEY ("line_id") REFERENCES "public"."line" ("line_id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."word" ADD CONSTRAINT "word_to_parallel_group_id" FOREIGN KEY ("parallel_group_id") REFERENCES "public"."parallel_group" ("parallel_group_id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table word_to_word
-- ----------------------------
ALTER TABLE "public"."word_to_word" ADD CONSTRAINT "parallel_to_word_address" FOREIGN KEY ("parallel_address") REFERENCES "public"."word" ("word_address") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "public"."word_to_word" ADD CONSTRAINT "word_to_word_address" FOREIGN KEY ("word_address") REFERENCES "public"."word" ("word_address") ON DELETE CASCADE ON UPDATE CASCADE;
