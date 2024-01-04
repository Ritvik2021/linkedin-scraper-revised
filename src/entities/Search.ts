import {
  ChildEntity,
  Column,
  Entity,
  JoinTable,
  ManyToMany,
  PrimaryGeneratedColumn,
  TableInheritance,
} from 'typeorm';
import { Person } from './Person';

export type SearchParams = {
  url: string;
  length: number;
  email: string;
  pw: string;
};

@Entity()
@TableInheritance({column: {type: 'varchar', name: 'type'}})
export class Search {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  name: string;

  @Column('json')
  params: SearchParams;

  @Column('timestamp with time zone')
  queuedAt: Date;

  @Column('timestamp with time zone', {nullable: true})
  startedAt: Date | null;
}

@ChildEntity()
export class QueueSearch extends Search {
  @Column()
  inProgress: boolean;

  @Column("varchar")
  stage: 'LOGGING_IN' | 'AWAITING_PIN' | 'SCRAPING';
}

@ChildEntity()
export class MemorySearch extends Search {
  @Column('timestamp with time zone')
  endedAt: Date;

  @Column('varchar', {nullable: true})
  error: string | null;

  @JoinTable()
  @ManyToMany(() => Person, p => p.searches)
  persons: Person[];
}
