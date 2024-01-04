import { MigrationInterface, QueryRunner } from "typeorm";

export class person1673143134124 implements MigrationInterface {
    name = 'person1673143134124'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."search" RENAME COLUMN "results" TO "stage"`);
        await queryRunner.query(`CREATE TABLE "mentor_searcher"."search_persons_person" ("searchId" uuid NOT NULL, "personId" uuid NOT NULL, CONSTRAINT "PK_7173d16851b103872b0b8e57c40" PRIMARY KEY ("searchId", "personId"))`);
        await queryRunner.query(`CREATE INDEX "IDX_99da4999d2a532090ef2066eb0" ON "mentor_searcher"."search_persons_person" ("searchId") `);
        await queryRunner.query(`CREATE INDEX "IDX_fe169b68b3c19e3a84157e2466" ON "mentor_searcher"."search_persons_person" ("personId") `);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "firstName"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "lastName"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "linkedInId" character varying NOT NULL`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD CONSTRAINT "UQ_707d5ec4544adb4a9231a3965de" UNIQUE ("linkedInId")`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "name" character varying NOT NULL`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "languages" character varying array`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "primaryInstitution" character varying`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "yearsOfExperience" integer`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "internationalSchool" boolean`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "schoolCountry" character varying`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "schoolPrimaryCurriculum" character varying`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "interestedInMentoring" boolean`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "location" character varying`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "linkedInUrl" character varying`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."search" DROP COLUMN "stage"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."search" ADD "stage" character varying`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."search_persons_person" ADD CONSTRAINT "FK_99da4999d2a532090ef2066eb0a" FOREIGN KEY ("searchId") REFERENCES "mentor_searcher"."search"("id") ON DELETE CASCADE ON UPDATE CASCADE`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."search_persons_person" ADD CONSTRAINT "FK_fe169b68b3c19e3a84157e2466a" FOREIGN KEY ("personId") REFERENCES "mentor_searcher"."person"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."search_persons_person" DROP CONSTRAINT "FK_fe169b68b3c19e3a84157e2466a"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."search_persons_person" DROP CONSTRAINT "FK_99da4999d2a532090ef2066eb0a"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."search" DROP COLUMN "stage"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."search" ADD "stage" json`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "linkedInUrl"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "location"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "interestedInMentoring"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "schoolPrimaryCurriculum"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "schoolCountry"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "internationalSchool"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "yearsOfExperience"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "primaryInstitution"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "languages"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "name"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP CONSTRAINT "UQ_707d5ec4544adb4a9231a3965de"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" DROP COLUMN "linkedInId"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "lastName" character varying NOT NULL`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."person" ADD "firstName" character varying NOT NULL`);
        await queryRunner.query(`DROP INDEX "mentor_searcher"."IDX_fe169b68b3c19e3a84157e2466"`);
        await queryRunner.query(`DROP INDEX "mentor_searcher"."IDX_99da4999d2a532090ef2066eb0"`);
        await queryRunner.query(`DROP TABLE "mentor_searcher"."search_persons_person"`);
        await queryRunner.query(`ALTER TABLE "mentor_searcher"."search" RENAME COLUMN "stage" TO "results"`);
    }

}
