-- MySQL 8+ schema proposal for the future database-backed version.
-- The read-only prototype uses JSON files; this schema is not executed.

CREATE TABLE eras (
  id VARCHAR(20) NOT NULL PRIMARY KEY,
  title TEXT NOT NULL,
  start_year SMALLINT UNSIGNED NOT NULL,
  end_year SMALLINT UNSIGNED NOT NULL,
  display_order SMALLINT UNSIGNED NOT NULL UNIQUE,
  CONSTRAINT chk_era_years CHECK (end_year >= start_year)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE era_sections (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  era_id VARCHAR(20) NOT NULL,
  section_order SMALLINT UNSIGNED NOT NULL,
  kind ENUM('intro', 'narrative') NOT NULL,
  heading TEXT NULL,
  paragraphs JSON NOT NULL,
  UNIQUE KEY uq_era_section_order (era_id, section_order),
  CONSTRAINT fk_era_sections_era FOREIGN KEY (era_id)
    REFERENCES eras (id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE era_images (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  era_id VARCHAR(20) NOT NULL,
  image_order SMALLINT UNSIGNED NOT NULL,
  image_url TEXT NOT NULL,
  alt_text TEXT NOT NULL,
  caption TEXT NULL,
  credit TEXT NULL,
  license TEXT NULL,
  UNIQUE KEY uq_era_image_order (era_id, image_order),
  CONSTRAINT fk_era_images_era FOREIGN KEY (era_id)
    REFERENCES eras (id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE era_sources (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  era_id VARCHAR(20) NOT NULL,
  source_order SMALLINT UNSIGNED NOT NULL,
  title TEXT NOT NULL,
  source_type VARCHAR(80) NULL,
  citation TEXT NULL,
  source_url TEXT NULL,
  UNIQUE KEY uq_era_source_order (era_id, source_order),
  CONSTRAINT fk_era_sources_era FOREIGN KEY (era_id)
    REFERENCES eras (id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
