import {DB} from './db';
import {MemorySearch, QueueSearch} from './entities/Search';

export const nukeRunningSearchOnStartup = async () => {
  const running = await DB.getRepository(QueueSearch).findOne({
    where: {inProgress: true},
  });

  if (!running) return;

  await DB.getRepository(QueueSearch).remove(running);

  const memoryItem = DB.getRepository(MemorySearch).create({
    id: running.id,
    name: running.name,
    params: running.params,
    queuedAt: running.queuedAt,
    error: 'nuked on startup',
  });
};
