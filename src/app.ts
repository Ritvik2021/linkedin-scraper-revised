process.env.NODE_ENV ??= 'development';
require('dotenv').config();
import Koa from 'koa';
import bodyParser from 'koa-bodyparser';
import {router} from './router';
import cors from '@koa/cors';
import {DB} from './db';
import {nukeRunningSearchOnStartup} from './utils';

(async () => {
  await DB.initialize();

  await nukeRunningSearchOnStartup();

  const koa = new Koa();

  koa.use(bodyParser());
  koa.use(cors());
  koa.use(async (ctx, next) => {
    try {
      await next();
    } catch (err) {
      console.log('in', ctx.URL.pathname);
      // console.log(err);
      throw err;
    }
  });
  // koa.use(async (ctx, next) => {
  //   // console.log(ctx.URL.pathname);
  //   await next();
  // });

  koa.use(router.routes()).use(router.allowedMethods());

  koa.listen(process.env.PORT || 3001);
  console.log('listening on ' + (process.env.PORT || 3001));
})();
