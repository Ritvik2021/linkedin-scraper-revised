import {DataSource} from 'typeorm';
import {Person} from './entities/Person';
import {MemorySearch, QueueSearch, Search} from './entities/Search';
import { init1670167534805 } from './migrations/1670167534805-init';
import { person1673143134124 } from './migrations/1673143134124-person';

export const DB = new DataSource({
  type: 'postgres',
  url: process.env.DB_URL,
  synchronize: process.env.NODE_ENV === 'development',
  schema: 'mentor_searcher',
  // logging: true,
  entities: [Person, Search, QueueSearch, MemorySearch],
  migrations: [init1670167534805, person1673143134124],
  subscribers: [],
});
