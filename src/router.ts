import Router from '@koa/router';
import {spawn, spawnSync} from 'child_process';
import {nanoid} from 'nanoid';
import CancelablePromise from 'cancelable-promise';
import {notifyOnSlack} from './slack';
import {DB} from './db';
import {
  MemorySearch,
  QueueSearch,
  Search,
  SearchParams,
} from './entities/Search';
export const router = new Router();

router.get('/ping', async (ctx) => {
  ctx.body = 'pong';
});

// const runPython = (
//   file: string,
//   params: SearchParams,
//   stageCb: (state: 'AWAITING_PIN' | 'LOGGED_IN') => void,
// ) => {
//   let stdin: (str: string) => void = null!;
//   const cancelablePromise = new CancelablePromise((res, rej, onCancel) => {
//     let proc: any = null;
//     onCancel(() => {
//       console.log('cancel');
//       proc.kill('SIGINT');
//     });
//     try {
//       let stdout = '';
//       proc = spawn('python', [
//         file,
//         params.url,
//         '' + params.length,
//         params.email,
//         params.pw,
//       ]);
//       proc.stdin.setEncoding('utf-8');
//       stdin = (str) => {
//         proc.stdin.cork();
//         proc.stdin.write(str + '\n');
//         proc.stdin.uncork();
//       };
//       proc.stdout.on('data', (d) => {
//         const dStr = d.toString();
//         console.log(dStr);
//         stdout += dStr;
//         if (/AWAIT_PIN/.exec(dStr)) {
//           stageCb("AWAITING_PIN");
//         }
//         if (/LOGGED_IN/.exec(dStr)) {
//           stageCb("LOGGED_IN");
//         }
//       });
//       proc.stderr.on('data', (d) => {
//         console.log(d.toString());
//         rej(new Error(d.toString()));
//       });
//       proc.on('close', (...args) => {
//         console.log('on close', ...args);

//         const x = /DATA_START(.+)DATA_END/s.exec(stdout);
//         if (x && x[1].length) {
//           try {
//             res(JSON.parse(x[1].trim()));
//           } catch (err) {
//             rej(err);
//           }
//         } else {
//           rej(new Error('no data'));
//         }
//       });
//       proc.on('error', (...args) => {
//         console.log('on err', ...args);
//         rej();
//       });
//     } catch (err) {
//       proc.kill('SIGINT');
//       rej(err);
//     }
//   });
//   return {cancelablePromise, stdin};
// };

let currentSearch:
  | (QueueSearch & {cancel: () => void; stdin: (str: string) => void})
  | null = null;

// const notifyQueue = async () => {
//   const queue = await DB.getRepository(QueueSearch).find({
//     order: {queuedAt: 'DESC'},
//   });
//   if (queue.length && !queue.filter((x) => x.inProgress).length) {
//     const nextUp = queue[0];

//     nextUp.inProgress = true;
//     nextUp.startedAt = new Date();
//     nextUp.stage = 'LOGGING_IN';

//     await DB.getRepository(QueueSearch).save(nextUp);

//     const stageCb = async (stage) => {
//       nextUp.stage = stage;
//       await DB.getRepository(QueueSearch).save(nextUp);
//     };

//     const rp = runPython('main_script.py', nextUp.params, stageCb);

//     const p = rp.cancelablePromise
//       .then(async (results) => {
//         console.log('successful');
//         await DB.getRepository(QueueSearch).remove(nextUp);

//         const memoryItem = DB.getRepository(MemorySearch).create({
//           id: nextUp.id,
//           name: nextUp.name,
//           params: nextUp.params,
//           queuedAt: nextUp.queuedAt,
//           results,
//         });
//         await DB.getRepository(MemorySearch).save(memoryItem);

//         notifyQueue();

//         await notifyOnSlack(memoryItem);
//       })
//       .catch(async (error) => {
//         console.log('error', error);
//         await DB.getRepository(QueueSearch).remove(nextUp);

//         const memoryItem = DB.getRepository(MemorySearch).create({
//           id: nextUp.id,
//           name: nextUp.name,
//           params: nextUp.params,
//           queuedAt: nextUp.queuedAt,
//           error: error.toString(),
//         });
//         await DB.getRepository(MemorySearch).save(memoryItem);

//         notifyQueue();

//         await notifyOnSlack(memoryItem);
//       });
//     currentSearch = {
//       ...nextUp,
//       cancel: async () => {
//         p.cancel();
//         await DB.getRepository(QueueSearch).remove(nextUp);
//         notifyQueue();
//       },
//       stdin: rp.stdin,
//     };
//   }
// };

// router.post('/queue/add', async (ctx) => {
//   const id = nanoid();
//   const queueItem = DB.getRepository(QueueSearch).create({
//     name: ctx.request.body.name,
//     queuedAt: new Date(),
//     params: ctx.request.body.params,
//     inProgress: false,
//   });
//   await DB.getRepository(QueueSearch).save(queueItem);

//   notifyQueue();
//   ctx.body = id;
// });

// router.post('/queue/cancel', async (ctx) => {
//   const item = await DB.getRepository(QueueSearch).findOne({
//     where: {id: ctx.request.body.id},
//   });

//   if (!item) {
//     throw new Error('Item does not exist');
//   }
//   if (item.inProgress) {
//     currentSearch?.cancel();
//   }

//   await DB.getRepository(QueueSearch).remove(item);

//   ctx.body = 'ok';
// });

// router.get('/queue', async (ctx) => {
//   ctx.body = await DB.getRepository(QueueSearch).find({
//     order: {queuedAt: 'DESC'},
//   });
// });

router.get('/memory', async (ctx) => {
  ctx.body = await DB.getRepository(MemorySearch).find({
    select: [
      'endedAt',
      'error',
      'id',
      'name',
      'params',
      'queuedAt',
      'startedAt',
    ],
  });
});

router.get('/search/:id', async (ctx) => {
  const search = await DB.getRepository(QueueSearch).findOne({
    where: {id: ctx.params.id},
  });
  if (search) {
    ctx.body = {...search, type: 'QueueSearch'};
  } else {
    const search = await DB.getRepository(MemorySearch).findOne({
      where: {id: ctx.params.id},
      relations: {persons: true},
    });
    if (search) {
      ctx.body = {...search, type: 'MemorySearch'};
    } else {
      ctx.body = null;
    }
  }
});

// router.post('/submit-pin', async (ctx) => {
//   const {searchId, pin} = ctx.request.body;
//   if (!currentSearch) {
//     throw new Error('There is no ongoing search');
//   }
//   if (searchId !== currentSearch.id) {
//     throw new Error('Attempted to submit the pin of a non-ongoing search');
//   }
//   currentSearch.stdin('SUBMIT_PIN ' + pin);
//   ctx.body = 'ok';
// });

// router.post('/queue/reorder', async (ctx) => {

// });
