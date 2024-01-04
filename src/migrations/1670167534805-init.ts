import { MigrationInterface, QueryRunner } from "typeorm";

export class init1670167534805 implements MigrationInterface {
    name = 'init1670167534805'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`CREATE TABLE "mentor_searcher"."person" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "firstName" character varying NOT NULL, "lastName" character varying NOT NULL, CONSTRAINT "PK_5fdaf670315c4b7e70cce85daa3" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "mentor_searcher"."search" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "name" character varying NOT NULL, "params" json NOT NULL, "queuedAt" TIMESTAMP WITH TIME ZONE NOT NULL, "startedAt" TIMESTAMP WITH TIME ZONE, "inProgress" boolean, "endedAt" TIMESTAMP WITH TIME ZONE, "results" json, "error" character varying, "type" character varying NOT NULL, CONSTRAINT "PK_0bdd0dc9f37fc71a6050de7ae7f" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE INDEX "IDX_450a67edd3dcde775c80c9655e" ON "mentor_searcher"."search" ("type") `);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`DROP INDEX "mentor_searcher"."IDX_450a67edd3dcde775c80c9655e"`);
        await queryRunner.query(`DROP TABLE "mentor_searcher"."search"`);
        await queryRunner.query(`DROP TABLE "mentor_searcher"."person"`);
    }

}
