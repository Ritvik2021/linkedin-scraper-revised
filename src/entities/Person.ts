import { Column, Entity, ManyToMany, PrimaryColumn, PrimaryGeneratedColumn } from "typeorm";
import { MemorySearch } from "./Search";

@Entity()
export class Person {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column('varchar', {unique: true})
  linkedInId: string;

  @Column()
  name: string;

  @Column('varchar', {array: true, nullable: true})
  languages: string[] | null;

  @Column('varchar', {nullable: true})
  primaryInstitution: string | null;

  @Column('int', {nullable: true})
  yearsOfExperience: number | null;

  @Column('varchar', {nullable: true})
  internationalSchool: boolean | null;

  @Column('varchar', {nullable: true})
  schoolCountry: string | null;

  @Column('varchar', {nullable: true})
  schoolPrimaryCurriculum: string | null;

  @Column('boolean', {nullable: true})
  interestedInMentoring: boolean | null;

  @Column('varchar', {nullable: true})
  location: string | null;

  @Column('varchar', {nullable: true})
  linkedInUrl: string | null;

  @ManyToMany(() => MemorySearch, ms => ms.persons)
  searches: MemorySearch[];
}